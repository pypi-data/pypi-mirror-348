from Logger import Logger

logger = Logger().get_logger()
class CustomException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        logger.critical(self.message)
