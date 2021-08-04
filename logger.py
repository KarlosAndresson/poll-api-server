import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from django.conf import settings


class AppLogger(logging.Logger):
    def __init__(self, filename: str, sub_dir: str = None, file_log_level: int = logging.DEBUG,
                 console_log_level: int = logging.INFO):
        super().__init__(__name__)
        full_log_dir = os.path.join(settings.LOG_DIR, sub_dir) if sub_dir else settings.LOG_DIR
        self.create_log_dir(full_log_dir)

        self.__file_handler = TimedRotatingFileHandler(filename=os.path.join(full_log_dir, filename), when='midnight',
                                                       backupCount=30, encoding='utf-8')
        self.__stout_handler = logging.StreamHandler(sys.stdout)
        # DEBUG, INFO, WARNING, ERROR, CRITICAL
        self.__file_handler.setLevel(file_log_level)
        self.__stout_handler.setLevel(console_log_level)

        sep = settings.LOG_SEP
        # https://docs.python.org/3/library/logging.html#logrecord-attributes
        self.__file_formatter = logging.Formatter(
            fmt=f'%(asctime)s{sep}%(levelname)s{sep}%(process)d{sep}%(thread)d{sep}%(pathname)s{sep}%(funcName)s{sep}%(message)s',
            datefmt='%Y.%m.%d %H:%M:%S')

        self.__stout_formatter = logging.Formatter(
            fmt=f'%(asctime)s{sep}%(levelname)s{sep}%(filename)s{sep}%(message)s',
            datefmt='%Y.%m.%d %H:%M:%S')

        self.__file_handler.setFormatter(self.__file_formatter)
        self.__stout_handler.setFormatter(self.__stout_formatter)

        self.addHandler(self.__file_handler)
        self.addHandler(self.__stout_handler)

    def create_log_dir(self, full_path):
        if not os.path.exists(full_path):
            try:
                os.makedirs(full_path, exist_ok=True)
                return True
            except Exception as e:
                self.exception(f'Error while trying to create directory for logging {e}', exc_info=True)
            return False

    def __repr__(self):
        return f'<Logger obj {self}>'