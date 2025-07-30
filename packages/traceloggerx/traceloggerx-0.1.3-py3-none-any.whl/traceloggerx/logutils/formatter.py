import json
import logging

from colorlog import ColoredFormatter

LOG_COLORS_CONFIG = {
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'bold_red',
}

class CustomColoredFormatter(ColoredFormatter):
    def format(self, record):
        record.white_asctime = f"\033[37m{self.formatTime(record, self.datefmt)}\033[0m"
        return super().format(record)

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "filename": record.filename,
            "funcName": record.funcName,
            "lineNo": record.lineno,
            "process": record.process,
            "thread": record.threadName
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)