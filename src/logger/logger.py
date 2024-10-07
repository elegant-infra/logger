import logging
import os
from typing import Optional

from termcolor import colored


class ColorFormatter(logging.Formatter):
    prefix_fmt = colored("[%(asctime)s %(name)s] ", "green") + colored(
        "(%(filename)s %(lineno)d): ", "grey")
    FORMATS = {
        logging.DEBUG: prefix_fmt + colored("[%(levelname)s] %(message)s", "blue"),
        logging.INFO: prefix_fmt + "[%(levelname)s] %(message)s",
        logging.WARNING: prefix_fmt + colored("[%(levelname)s] %(message)s", "yellow"),
        logging.ERROR: prefix_fmt + colored("[%(levelname)s] %(message)s", "red"),
        logging.CRITICAL: prefix_fmt + colored("[%(levelname)s] %(message)s", "red"),
    }

    def __init__(self, datefmt: str):
        super().__init__()
        self._datefmt = datefmt
        self._formatters = {level: logging.Formatter(fmt, datefmt=self._datefmt) 
                            for level, fmt in self.FORMATS.items()}

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self._datefmt)
        return formatter.format(record)


def get_log_level():
    level_name = os.getenv("LOG_LEVEL", "").upper()
    return getattr(logging, level_name, logging.INFO)


def setup_logger(
    name: Optional[str] = None,
    path: Optional[str] = None,
    level: int = logging.INFO,
    stdout_level: int = logging.INFO,
    disable_stdout: bool = False,
    custom_stdout_formatter: logging.Formatter = None,
    custom_file_formatter: logging.Formatter = None,
    handler_filter: logging.FileHandler = None,
    propagate: bool = False,
) -> logging.Logger:
    logger = logging.getLogger(name)

    datefmt = "%Y-%m-%d %H:%M:%S"
    handlers = []

    if not disable_stdout:
        formatter = ColorFormatter(
            datefmt=datefmt) if custom_stdout_formatter is None else custom_stdout_formatter
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(stdout_level)
        if handler_filter:
            stream_handler.addFilter(handler_filter)
        handlers.append(stream_handler)

    if path is not None:
        fmt = "[%(asctime)s %(name)s] (%(filename)s %(lineno)d): [%(levelname)s] %(message)s"
        formatter = logging.Formatter(
            fmt, datefmt=datefmt) if custom_file_formatter is None else custom_file_formatter
        file_handler = logging.FileHandler(path)
        file_handler.setFormatter(formatter)
        if handler_filter:
            file_handler.addFilter(handler_filter)
        handlers.append(file_handler)

    logger.setLevel(level=level)
    logger.handlers = handlers
    logger.propagate = propagate
    return logger
