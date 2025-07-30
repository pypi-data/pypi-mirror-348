import glob
import os
import random
import subprocess

from tqdm import tqdm


def call_zeek(pcap_path: str, keep_rate=1.0) -> list[str]:
    """
    Call Zeek to process a pcap file and return the contents of the generated log files.

    :param keep_rate: The rate at which to keep packets (default is 1.0, meaning all packets are kept)
    :param pcap_path: Path to the pcap file (relative to the mounted volume in the Docker container)
    :return: A list of strings, where each string is the content of a Zeek log file
    """

    subprocess.run(
        [
            "docker", "run", "-v", ".:/data", "zeek/zeek", "sh", "-c",
            f"zeek -C -r /data/{pcap_path} && cp *.log /data"
        ],
    )

    log_files = glob.glob("*.log")
    # 去除app.log
    log_files = [file for file in log_files if file != "app.log"]

    file_contents = []
    for file_path in tqdm(log_files, desc="Processing log files"):
        with open(file_path, 'r', encoding='utf-8') as file:
            while True:
                chunk = file.read(2048)
                if not chunk:
                    break
                if random.random() < keep_rate:
                    file_contents.append(chunk)
        # Remove the log file after reading its contents
        os.remove(file_path)
    return file_contents
