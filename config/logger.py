import logging
import sys
from pathlib import Path


def create_logger(name: str, file: Path = None):
    logger = logging.getLogger(name)
    formatter = get_formatter()
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    if logger.handlers:
        return logger
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    if file:
        if not file.parent.exists():
            file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


def get_formatter():
    return logging.Formatter(
        "%(asctime)s | [%(filename)s:%(lineno)d] | %(levelname)s | %(message)s",
        "%Y-%m-%d %H:%M",
    )


logger = create_logger("app_logger", None)
