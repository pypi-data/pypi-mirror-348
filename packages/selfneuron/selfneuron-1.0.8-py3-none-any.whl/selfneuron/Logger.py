from loguru import logger

class Logger():
    def get_logger(self):
        logger.remove()
        logger.add("logfile.log",
                format="{time} {level} {thread} {module} -- {file}:{function}::{line} {message}",
                colorize=True,
                rotation="10 MB",
                # retention="",
        )
        return logger