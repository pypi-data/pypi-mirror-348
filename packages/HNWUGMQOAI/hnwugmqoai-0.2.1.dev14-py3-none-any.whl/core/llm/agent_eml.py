import loguru
from kink import di, inject
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from core.llm.data_structure.eml_analysis import mail_analysis
from core.llm.data_structure.pcap_analysis import pcap_analysis, multi_pcap_analysis
from core.llm.front_layer.slice import section
from core.scheduler.core.schemas.works.PydanticSafetyParser import ChatWithSafetyPydanticOutputParser

PYDANTIC_OBJECT = mail_analysis


@section
def agent_eml(eml_raw: str) -> PYDANTIC_OBJECT:
    """
    通过LLM分析eml文件
    :param eml_raw:
    :return:
    """
    parser = PydanticOutputParser(pydantic_object=PYDANTIC_OBJECT)
    promptTemplate = ChatPromptTemplate.from_messages([
        ("system", "{format_instructions};"
                   "你是一名网络安全专家，请根据用户提供的eml原文进行分析，若含有高置信度的攻击或钓鱼内容，则需要提取出来并返回结果"
         ),
        ("user", "eml_raw: {eml_raw};")
    ])
    input_args = {"eml_raw": eml_raw,
                  "format_instructions": parser.get_format_instructions(),
                  }
    res = ChatWithSafetyPydanticOutputParser(model=di['llm'], input_args=input_args,
                                             promptTemplate=promptTemplate,
                                             schemas_model=PYDANTIC_OBJECT)
    return res
