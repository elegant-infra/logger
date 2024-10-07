import logging

from .utils import create_stream_handler, create_file_handler, get_log_level


class Logger:
    def __init__(
        self,
        name: str = None,
        path: str = None,
        level: int = logging.INFO,
        stdout_level: int = logging.INFO,
        disable_stdout: bool = False,
        custom_stdout_formatter: logging.Formatter = None,
        custom_file_formatter: logging.Formatter = None,
        handler_filter: logging.Filter = None,
        propagate: bool = False,
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level or get_log_level())

        self._setup_handlers(
            path,
            level,
            stdout_level,
            disable_stdout,
            custom_stdout_formatter,
            custom_file_formatter,
            handler_filter,
        )
        self.logger.propagate = propagate

    def _setup_handlers(
        self,
        path,
        level,
        stdout_level,
        disable_stdout,
        custom_stdout_formatter,
        custom_file_formatter,
        handler_filter,
    ):
        datefmt = "%Y-%m-%d %H:%M:%S"
        handlers = []
        if not disable_stdout:
            handlers.append(
                create_stream_handler(
                    stdout_level, datefmt, custom_stdout_formatter, handler_filter
                )
            )

        if path is not None:
            handlers.append(
                create_file_handler(
                    path, level, datefmt, custom_file_formatter, handler_filter
                )
            )

        self.logger.handlers.clear()
        self.logger.handlers.extend(handlers)

    def __getattr__(self, name):
        return getattr(self.logger, name)
