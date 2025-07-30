import os
import sys
from pathlib import Path

from loguru import logger


class LoggerManager:
    def __init__(self):
        self.logger = logger
        self.terminal_logger_id: int = 0
        self.jsonl_logger_id: int = 0
        self.file_logger_id: int = 0
        self.logger.remove()  # 清除默认的Logger=

    def get_logger(self):
        return self.logger

    def add_terminal_logger(self, level: str = "INFO", is_output_name: bool = False,
                            is_output_function: bool = False, enqueue=True) -> 'LoggerManager':
        self.logger.level("TRACE", color="<cyan>", icon=f"🤔 __TRACE")
        self.logger.level("DEBUG", color="<blue>", icon=f"🚧 __DEBUG")
        self.logger.level("INFO", color="<white>", icon=f"ℹ️ ___INFO")
        self.logger.level("SUCCESS", color="<green>", icon=f"✅ SUCCESS")
        self.logger.level("WARNING", color="<yellow>", icon=f"🤯 WARNING")
        self.logger.level("ERROR", color="<red>", icon=f"😡 __ERROR")

        default_format: str = (
                "<g>{time:MM-DD HH:mm:ss}</g> " +
                "[<lvl>{level.icon}</lvl>] " +
                ("<c><u>{name}</u></c> " if is_output_name else "") +
                ("<c>{function}:{line}</c> " if is_output_function else "") +
                "|| <lvl>{message}</lvl>"
        )
        self.terminal_logger_id = self.logger.add(
            sys.stdout,
            level=level,
            diagnose=False,
            format=default_format,
            enqueue=enqueue,
        )

        return self

    def add_jsonl_logger(self, log_dir: os.PathLike = Path("./logs/"), level: str = "INFO", enqueue=True,
                         rotation="100 MB",
                         retention="10 days") -> 'LoggerManager':
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.jsonl_logger_id = self.logger.add(
            Path(log_dir).joinpath("log-{time}.jsonl"),
            level=level,
            enqueue=enqueue,
            serialize=True,
            rotation=rotation,
            retention=retention,
        )

        return self

    def add_file_logger(self, log_dir: os.PathLike = Path("./logs/"), level: str = "INFO", enqueue=True,
                        rotation="100 MB",
                        retention="10 days") -> 'LoggerManager':
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.file_logger_id = self.logger.add(
            Path(log_dir).joinpath("log-{time}.log"),
            level=level,
            enqueue=enqueue,
            rotation=rotation,
            retention=retention,
        )

        return self

    def remove_terminal_logger(self) -> 'LoggerManager':
        self.logger.remove(self.terminal_logger_id)
        return self

    def remove_jsonl_logger(self) -> 'LoggerManager':
        self.logger.remove(self.jsonl_logger_id)
        return self

    def remove_file_logger(self) -> 'LoggerManager':
        self.logger.remove(self.file_logger_id)
        return self


# 简单的 logger 使用示例
if __name__ == '__main__':
    lm = LoggerManager().add_jsonl_logger().add_file_logger()
    logger = lm.get_logger()
    logger.trace('trace message')
    logger.debug('debug message')
    logger.info('info message')
    logger.success('success message')
    logger.warning('warning message')
    logger.error('error message')
