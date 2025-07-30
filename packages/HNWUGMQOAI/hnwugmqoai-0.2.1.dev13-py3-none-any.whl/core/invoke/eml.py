import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import loguru
from core.invoke.result_slice import split_sum_res

from core.config import Master
from kink import di
from tqdm import tqdm

from core.eml.eml_reader import parse_eml_file
from core.llm.agent_eml import agent_eml
from core.llm.old.report_sum import sec_report_writer
from core.scheduler.core.init import global_llm


def process_sum_res(
        sum_res,
        output_report_path,
        sec_report_writer,
        MAX_REPORT_WRITER_CONTEXT_LENGTH,
        encoding="utf-8"
):
    """
    处理分组后的 sum_res，生成带序号的报告文件。

    参数：
        sum_res: 可 str 调用的结构体列表
        output_report_path: 输出报告文件的路径
        sec_report_writer: 用于生成报告的函数，接受 reports 参数
        MAX_REPORT_WRITER_CONTEXT_LENGTH: 每组字符串最大总长度
        encoding: 文件编码，默认 utf-8
    """
    groups = split_sum_res(sum_res, MAX_REPORT_WRITER_CONTEXT_LENGTH)

    for idx, group in enumerate(groups, start=1):
        # 生成报告内容
        sum_reports = sec_report_writer(reports=group)
        if "</think>" in sum_reports:
            sum_reports = sum_reports.split("</think>")[-1]
        loguru.logger.info(f"Final report: {sum_reports[:64]}...")

        # 构建文件路径
        if idx == 1:
            current_output_path = output_report_path
        else:
            dir_name = os.path.dirname(output_report_path)
            base_name = os.path.basename(output_report_path)
            file_name, ext = os.path.splitext(base_name)
            current_output_path = os.path.join(dir_name, f"{file_name}_{idx}{ext}")

        # 写入文件
        with open(current_output_path, "w", encoding=encoding) as f:
            f.write(sum_reports)


def invoke(input_eml_folder: str, output_report_path: str, encoding="utf-8", INVOKE_THREADS=20):
    """
    最终的做题函数，根据输入的eml文件夹处理，并在对应路径输出报告
    :param INVOKE_THREADS:
    :param encoding:
    :param input_eml_folder: folder
    :param output_report_path: *.md
    :return:
    """
    assert os.path.exists(input_eml_folder), f"Input folder {input_eml_folder} does not exist"
    assert output_report_path.endswith(".md"), "Output file must be a markdown file"

    eml_raws = []
    # 将input_eml_folder下所有的.eml文件读取到eml_raws中
    for root, dirs, files in os.walk(input_eml_folder):
        for file in files:
            if file.endswith(".eml"):
                path = os.path.join(root, file)
                eml_raws.append(parse_eml_file(path))

    sum_res = []
    with global_llm():

        def process_eml(eml_content):
            """
            单个 eml content 的处理函数
            """
            try:
                reports_sum = agent_eml(eml_raw=eml_content)
                loguru.logger.debug(f"raw reports: {reports_sum}")
                valid_reports = []

                for reports in reports_sum:
                    for report in reports.mail_analysis:
                        loguru.logger.debug(f"report: {report}")
                        if hasattr(report, "attack_info") and hasattr(report.attack_info, "is_attack"):
                            loguru.logger.debug(f"report.attack_info: {report.attack_info}")
                            if report.attack_info.is_attack:
                                valid_reports.append(report)
                        else:
                            loguru.logger.warning(f"Invalid report format: {report}")

                return valid_reports
            except Exception as e:
                loguru.logger.error(f"Error processing {eml_content}: {e}")
                return None
            return None

        with ThreadPoolExecutor(max_workers=INVOKE_THREADS) as executor:
            future_to_log = {
                executor.submit(process_eml, eml_raw): eml_raw
                for eml_raw in eml_raws
            }

            with tqdm(desc="总进度", total=len(eml_raws)) as pbar:
                for future in as_completed(future_to_log):
                    eml = future_to_log[future]
                    result = future.result()
                    current_log = eml[:32]

                    if result is not None:
                        sum_res.append(result)

                    # 更新进度条
                    pbar.update(1)
                    pbar.set_postfix(current_log=current_log)
    process_sum_res(
        sum_res,
        output_report_path,
        sec_report_writer=sec_report_writer,
        MAX_REPORT_WRITER_CONTEXT_LENGTH=12000,
        encoding=Master.get("encoding", "utf-8")
    )
