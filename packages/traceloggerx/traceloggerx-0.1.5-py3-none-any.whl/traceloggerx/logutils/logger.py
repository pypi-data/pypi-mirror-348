import io
import logging
import os
import sys
import traceback

from .handlers import get_file_handler, get_stream_handler

ROOT_PKG = "default"

class ContextualLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        context = self.extra.copy() if self.extra else {}
        context.update(kwargs.pop("extra", {}))
        kwargs["extra"] = context
        return msg, kwargs

def set_logger(pkg: str, log_dir: str = "./logs", level: str | None = None, stream_only=False, json_format=False, extra: dict | None = None):
    logger = logging.getLogger(pkg)
    level = level or os.getenv("LOG_LEVEL", "INFO")
    logger.setLevel(level)

    if not logger.handlers:
        logger.addHandler(get_stream_handler())
        if not stream_only:
            logger.addHandler(get_file_handler(pkg, log_base_dir=log_dir, json_format=json_format))

    # apply contextual adapter
    if extra is None:
        extra = {}
    return ContextualLoggerAdapter(logger, extra)

def handle_exception(exc_type, exc_value, exc_traceback):
    logger = logging.getLogger(ROOT_PKG)
    formatted = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger.error("Unhandled exception occurred:\n%s", formatted)

def init_logger():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    sys.excepthook = handle_exception
    set_logger(ROOT_PKG)