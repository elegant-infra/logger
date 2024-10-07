import logging

from termcolor import colored


class LogFormatter(logging.Formatter):
    prefix_fmt = colored("[%(asctime)s %(name)s] ", "green") + colored(
        "(%(filename)s %(lineno)d): ", "grey"
    )
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
        self._formatters = {
            level: logging.Formatter(fmt, datefmt=self._datefmt)
            for level, fmt in self.FORMATS.items()
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self._datefmt)
        return formatter.format(record)
