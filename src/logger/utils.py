import logging
import os

from .log_formatter import LogFormatter


def get_log_level(default=logging.INFO):
    level_name = os.getenv("LOG_LEVEL", "").upper()
    return getattr(logging, level_name, default)


def create_stream_handler(level, datefmt, custom_formatter=None, handler_filter=None):
    formatter = (
        LogFormatter(datefmt=datefmt) if custom_formatter is None else custom_formatter
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(level)
    if handler_filter:
        stream_handler.addFilter(handler_filter)
    return stream_handler


def create_file_handler(
    path, level, datefmt, custom_formatter=None, handler_filter=None
):
    fmt = (
        "[%(asctime)s %(name)s] (%(filename)s %(lineno)d): [%(levelname)s] %(message)s"
    )
    formatter = (
        logging.Formatter(fmt, datefmt=datefmt)
        if custom_formatter is None
        else custom_formatter
    )
    file_handler = logging.FileHandler(path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    if handler_filter:
        file_handler.addFilter(handler_filter)
    return file_handler
