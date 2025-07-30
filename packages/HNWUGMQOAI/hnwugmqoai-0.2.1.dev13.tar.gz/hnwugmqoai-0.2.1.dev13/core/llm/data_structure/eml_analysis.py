from enum import Enum
from typing import Optional

from pydantic import BaseModel


class attack_info(BaseModel):
    is_attack: bool = False
    attack_type: str = ""


class eml_analysis(BaseModel):
    """
    pcap分析结构
    """
    attack_info: attack_info
    sender: str = ""
    receiver: str = ""
    subject: str = ""


class mail_analysis(BaseModel):
    mail_analysis: list[eml_analysis]
