import json
import os
from email.header import decode_header
from email.parser import Parser

import loguru

from core.config import Master


def decode_email_header(header):
    """
    解码邮件头字段（Subject, From, To 等）
    """
    if header is None:
        return ""
    decoded_str = ""
    for part, charset in decode_header(header):
        if isinstance(part, bytes):
            if charset:
                decoded_str += part.decode(charset, errors='replace')
            else:
                decoded_str += part.decode('utf-8', errors='replace')
        else:
            decoded_str += part
    return decoded_str


def extract_email_body(email_message):
    """
    提取邮件正文内容（优先 text/plain）
    """
    body = ""
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))

            if content_type == "text/plain" and "attachment" not in content_disposition:
                charset = part.get_content_charset() or 'utf-8'
                payload = part.get_payload(decode=True)
                if payload:
                    body = payload.decode(charset, errors='replace')
                break
    else:
        charset = email_message.get_content_charset() or 'utf-8'
        payload = email_message.get_payload(decode=True)
        if payload:
            body = payload.decode(charset, errors='replace')
    return body


@loguru.logger.catch
def parse_eml_file(file_path):
    """
    解析 .eml 文件，返回结构化信息的 JSON 字符串
    """
    result = {}

    if not os.path.isfile(file_path):
        result['error'] = 'File not found'
        return json.dumps(result, ensure_ascii=False)

    try:
        with open(file_path, 'r', encoding=Master.get("encoding", 'utf-8'), errors="ignore") as f:
            email_message = Parser().parse(f)

        # 解码邮件头
        subject = decode_email_header(email_message.get('Subject'))
        from_ = decode_email_header(email_message.get('From'))
        to = decode_email_header(email_message.get('To'))
        # 提取邮件正文
        body = extract_email_body(email_message)[:2048]

        result.update({
            'subject': subject,
            'from': from_,
            'to': to,
            'body': body
        })

    except Exception as e:
        raise e

    return json.dumps(result, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    result = parse_eml_file("../../datasets/31b65013.eml")
    print(result)
