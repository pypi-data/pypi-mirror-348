from enum import Enum
from typing import Optional

from pydantic import BaseModel


class attack_info(BaseModel):
    is_attack: bool = False
    attack_type: str = ""


class pcap_analysis(BaseModel):
    """
    pcap分析结构
    """
    attack_info: attack_info
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int


class multi_pcap_analysis(BaseModel):
    multi_pcap_analysis: list[pcap_analysis]
