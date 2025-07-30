import logging
import os

from .formatter import LOG_COLORS_CONFIG, CustomColoredFormatter, JSONFormatter

STREAM_HANDLER_FORMAT = (
    "%(white_asctime)s | %(log_color)s%(levelname)-8s | %(name)s "
    "[%(filename)s:%(funcName)s:%(lineno)d] >> %(message)s"
)

FILE_HANDLER_FORMAT = (
    "[%(asctime)s] | %(levelname)-8s | %(name)s "
    "[%(filename)s:%(funcName)s:%(lineno)d] >> %(message)s"
)

def get_stream_handler():
    handler = logging.StreamHandler()
    handler.setFormatter(CustomColoredFormatter(
        STREAM_HANDLER_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors=LOG_COLORS_CONFIG
    ))
    return handler

def get_file_handler(pkg: str, log_base_dir: str = "./logs", json_format: bool = False):
    os.makedirs(log_base_dir, exist_ok=True)
    file_path = os.path.join(log_base_dir, f"{pkg}.log")
    handler = logging.FileHandler(file_path, encoding="utf-8")
    formatter = JSONFormatter(datefmt="%Y-%m-%d %H:%M:%S") if json_format else logging.Formatter(FILE_HANDLER_FORMAT)
    handler.setFormatter(formatter)
    return handler