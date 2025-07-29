import logging
import traceback
import os
from types import FrameType
from typing import cast
from loguru import logger as base_logger


class Logger:
    def __init__(self):
        self.logger = base_logger

    def set_log_path(self, log_path):
        os.makedirs(log_path, exist_ok=True)
        self.logger.add(
            log_path.joinpath("{time:YYYY-MM-DD}.log"),
            rotation="50 MB",  # 设置单个日志文件大小达到50MB时进行轮转（切割）
            encoding="utf-8",
            enqueue=True,
            retention='1 days',
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
            filter=lambda record: record["level"].name != "INFO"  # 过滤INFO级别日志不写入文件
        )
    @staticmethod
    def handle(*args, **kwargs):
        message = ' '.join(map(str, args))
        kw_message = " ".join([f"{key} = {val}" for key, val in kwargs.items()])
        if kw_message:
            message = message + "\n" + kw_message
        return message

    def log(self, *args, **kwargs):
        depth = int(kwargs.pop("depth", 1))
        message = self.handle(*args, **kwargs)
        self.logger.opt(depth=depth).info(message)

    def info(self, *args, **kwargs):
        depth = int(kwargs.pop("depth", 1))
        message = self.handle(*args, **kwargs)
        self.logger.opt(depth=depth).info(message)

    def debug(self, *args, **kwargs):
        depth = int(kwargs.pop("depth", 1))
        message = self.handle(*args, **kwargs)
        self.logger.opt(depth=depth).debug(message)

    def warn(self, *args, **kwargs):
        depth = int(kwargs.pop("depth", 1))
        message = self.handle(*args, **kwargs)
        self.logger.opt(depth=depth).warning(message)

    def warning(self, *args, **kwargs):
        depth = int(kwargs.pop("depth", 1))
        message = self.handle(*args, **kwargs)
        self.logger.opt(depth=depth).warning(message)

    def error(self, *args, **kwargs):
        error_info = traceback.format_exc()
        depth = int(kwargs.pop("depth", 1))
        message = self.handle(error_info, *args, **kwargs)
        self.logger.opt(depth=depth).error(message)

    def init_config(self):
        LOGGER_NAMES = ("uvicorn.asgi", "uvicorn.access", "uvicorn")

        # change handler for default uvicorn _logger
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in LOGGER_NAMES:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler()]


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = base_logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        base_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage(),
        )


logger = Logger()
