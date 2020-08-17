import logging
from logging.handlers import RotatingFileHandler


class Log(object):
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self.error_filename = kwargs.get('error_filename')
        self.error_level = kwargs.get('error_level')
        self.info_level = kwargs.get('info_level')
        self.formatter = kwargs.get('formatter')
        self.logger = logging.getLogger(__name__)
        self.generateErrorFileHandler()
        self.generateInfoFileHandler()

    def generateErrorFileHandler(self):
        error_handler = RotatingFileHandler(self.error_filename, backupCount=0)
        error_handler.setLevel(self.error_level)
        error_handler.setFormatter(self.formatter)
        self.logger.addHandler(error_handler)

    def generateInfoFileHandler(self):
        info_handler = RotatingFileHandler(self.filename, backupCount=0)
        info_handler.setLevel(self.info_level)
        info_handler.setFormatter(self.formatter)
        self.logger.addHandler(info_handler)
