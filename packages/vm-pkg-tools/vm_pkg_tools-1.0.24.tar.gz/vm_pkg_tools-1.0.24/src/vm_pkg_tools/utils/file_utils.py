import os
import chardet
import logging


def detect_encoding(file_path):
    with open(file_path, "rb") as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    logging.info(f"Detected encoding for {file_path}: {result}")
    return result.get("encoding", "utf-8")


def read_scout_file(file_path, encoding=None):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    encoding = encoding or detect_encoding(file_path)
    with open(file_path, "r", encoding=encoding, errors="replace") as file:
        content = file.read()
    return content
