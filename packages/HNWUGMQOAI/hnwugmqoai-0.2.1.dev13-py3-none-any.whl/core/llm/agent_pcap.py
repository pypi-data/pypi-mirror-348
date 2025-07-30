import loguru
from kink import di, inject
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from core.llm.data_structure.pcap_analysis import pcap_analysis, multi_pcap_analysis
from core.llm.front_layer.slice import section
from core.scheduler.core.schemas.works.PydanticSafetyParser import ChatWithSafetyPydanticOutputParser

PYDANTIC_OBJECT = multi_pcap_analysis


@section
def agent_pcap(pcap_log: str) -> multi_pcap_analysis:
    """
    通过LLM分析pcap日志
    :param pcap_log:
    :return:
    """
    parser = PydanticOutputParser(pydantic_object=PYDANTIC_OBJECT)
    promptTemplate = ChatPromptTemplate.from_messages([
        ("system", "{format_instructions};"
                   "你是一名网络安全专家，请根据用户提供的流量日志进行分析，若含有高置信度的攻击流量，则需要提取出来并返回结果"
         ),
        ("user", "pcap_zeek_log: {pcap_zeek_log};")
    ])
    input_args = {"pcap_zeek_log": pcap_log,
                  "format_instructions": parser.get_format_instructions(),
                  }
    res = ChatWithSafetyPydanticOutputParser(model=di['llm'], input_args=input_args,
                                             promptTemplate=promptTemplate,
                                             schemas_model=PYDANTIC_OBJECT)
    loguru.logger.info(f"Pydantic 转换结果: {res}")
    return res
