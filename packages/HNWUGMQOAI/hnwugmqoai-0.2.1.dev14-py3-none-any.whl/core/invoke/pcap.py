import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import loguru

from core.config import Master
from tqdm import tqdm

from core.docker_call.zeek_call import call_zeek
from core.invoke.result_slice import split_sum_res
from core.llm.agent_pcap import agent_pcap
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


def invoke(input_pcap_path: str, output_report_path: str, INVOKE_THREADS=20, KEEP_RATE=1.0):
    """
    最终的做题函数，根据输入的pcap文件路径处理，并在对应路径输出报告
    :param KEEP_RATE: 保留率
    :param INVOKE_THREADS:
    :param input_pcap_path: *.pcap
    :param output_report_path: *.md
    :return:
    """
    assert input_pcap_path.endswith(".pcap"), "Input file must be a pcap file"
    assert output_report_path.endswith(".md"), "Output file must be a markdown file"
    assert 0 <= KEEP_RATE <= 1, "KEEP_RATE must be between 0 and 1"

    zeek_res = call_zeek(input_pcap_path, keep_rate=KEEP_RATE)  # [str...]
    sum_res = []
    with global_llm():

        def process_pcap(pcap_log):
            """
            单个 pcap_log 的处理函数
            """
            try:
                reports_sum = agent_pcap(pcap_log=pcap_log)
                loguru.logger.debug(f"raw reports: {reports_sum}")
                valid_reports = []
                for reports in reports_sum:
                    for report in reports.multi_pcap_analysis:
                        loguru.logger.debug(f"report: {report}")
                        if hasattr(report, "attack_info") and hasattr(report.attack_info, "is_attack"):
                            loguru.logger.debug(f"attack_info: {report.attack_info}")
                            if report.attack_info.is_attack:
                                valid_reports.append(report)
                        else:
                            loguru.logger.warning(f"Invalid report structure: {report}")

                return valid_reports
            except Exception as e:
                loguru.logger.error(f"Error processing {e}")
                return None

        with ThreadPoolExecutor(max_workers=INVOKE_THREADS) as executor:
            future_to_log = {
                executor.submit(process_pcap, pcap_log): pcap_log
                for pcap_log in zeek_res
            }

            with tqdm(desc="总进度", total=len(zeek_res)) as pbar:
                for future in as_completed(future_to_log):
                    pcap_log = future_to_log[future]
                    result = future.result()
                    current_log = pcap_log[:32]

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
