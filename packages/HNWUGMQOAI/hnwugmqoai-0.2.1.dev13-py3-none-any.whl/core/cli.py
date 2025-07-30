from typing import List

import loguru
import pypandoc
import typer

from core.config import Master

import core.invoke.pcap
from core.invoke.eml import invoke

app = typer.Typer(
    name="某比赛的核心cli",
    no_args_is_help=True,
)


@app.command()
def convert_md_to_pdf(
        input_path: str = typer.Argument(..., help="Input file path of .md."),
        output_path: str = typer.Argument(..., help="Output file path of .pdf."),
):
    assert input_path.endswith(".md"), "Input file must be a .md file"
    assert output_path.endswith(".pdf"), "Output file must be a .pdf file"
    output = pypandoc.convert_file(input_path, 'pdf', outputfile=output_path)
    loguru.logger.success(f"Markdown to PDF conversion successful: {input_path} -> {output_path}")


@app.command()
def pcap(
        input_path: str = typer.Argument(..., help="Input file path of .pcap."),
        output_path: str = typer.Argument(..., help="Output report path"),
        api_endpoint: str = typer.Option("https://www.gptapi.us/v1", help="Openai api endpoint"),
        api_key: str = typer.Option("sk-gnZfIx337omYX3bd30B1C95a0f1047Ee86CaD8925177AbEa", help="Openai api key"),
        default_model: str = typer.Option("o1-preview", help="Openai model"),
        INVOKE_THREADS: int = typer.Option(20, help="Number of threads for invoke"),
        KEEP_RATE: float = typer.Option(1, help="∈ [0,1]; 保留率，越接近1，保留的包越多，越接近0，保留的包越少"),

):
    """
    解析pcap文件，生成报告
    :param KEEP_RATE: 保留率，越接近1，保留的包越多，越接近0，保留的包越少
    :param INVOKE_THREADS:
    :param default_model:
    :param api_key:
    :param api_endpoint:
    :param input_path: 输入的pcap文件路径
    :param output_path: 输出的报告路径
    :return:
    """
    Master['openai_api_endpoint'] = api_endpoint
    Master['openai_api_key'] = api_key
    Master['default_model'] = default_model
    core.invoke.pcap.invoke(
        input_pcap_path=input_path
        , output_report_path=output_path
        , INVOKE_THREADS=INVOKE_THREADS,
        KEEP_RATE=KEEP_RATE
    )


@app.command()
def binary(
        input_path: str = typer.Argument(..., help="Input folder of binary."),
        output_path: str = typer.Argument(..., help="Output report path"),
):
    """
    解析二进制文件，生成报告
    :param default_model:
    :param api_key:
    :param api_endpoint:
    :param input_path: 输入的二进制文件路径
    :param output_path: 输出的报告路径
    :return:
    """
    ...


@app.command()
def eml(
        input_path: str = typer.Argument(..., help="Input folder of .eml."),
        output_path: str = typer.Argument(..., help="Output report path"),
        api_endpoint: str = typer.Option("https://www.gptapi.us/v1", help="Openai api endpoint"),
        api_key: str = typer.Option("sk-gnZfIx337omYX3bd30B1C95a0f1047Ee86CaD8925177AbEa", help="Openai api key"),
        default_model: str = typer.Option("o1-preview", help="Openai model"),
        INVOKE_THREADS: int = typer.Option(20, help="Number of threads for invoke"),
        ENCODING: str = typer.Option("utf-8", help="Encoding for .eml files"),
):
    """
    解析.eml文件，生成报告
    :param INVOKE_THREADS:
    :param ENCODING:
    :param default_model:
    :param api_key:
    :param api_endpoint:
    :param input_path: 输入的.eml文件路径
    :param output_path: 输出的报告路径
    :return:
    """
    Master['openai_api_endpoint'] = api_endpoint
    Master['openai_api_key'] = api_key
    Master['default_model'] = default_model
    invoke(input_eml_folder=input_path, output_report_path=output_path, encoding=ENCODING,
           INVOKE_THREADS=INVOKE_THREADS)


def main():
    app()


if __name__ == "__main__":
    main()
