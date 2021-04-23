# -*- coding: utf-8 -*-

from django.conf import settings
from blueapps.utils.logger import logger as bk_logger

ISDEV = settings.RUN_MODE == "DEVELOP"


class Logger:
    def __init__(self):
        pass

    @staticmethod
    def debug(msg, *args, **kwargs):
        bk_logger.debug(msg, *args, **kwargs)
        if ISDEV:
            print(msg, *args)

    @staticmethod
    def info(msg, *args, **kwargs):
        bk_logger.info(msg, *args, **kwargs)
        if ISDEV:
            print(msg, *args)

    @staticmethod
    def warning(msg, *args, **kwargs):
        bk_logger.warning(msg, *args, **kwargs)
        if ISDEV:
            print(msg, *args)

    @staticmethod
    def error(msg, *args, **kwargs):
        bk_logger.error(msg, *args, **kwargs)
        if ISDEV:
            print(msg, *args)

    @staticmethod
    def exception(msg, *args, **kwargs):
        bk_logger.exception(msg, *args, **kwargs)
        if ISDEV:
            print(msg, *args)

    @staticmethod
    def critical(msg, *args, **kwargs):
        bk_logger.critical(msg, *args, **kwargs)
        if ISDEV:
            print(msg, *args)

    @staticmethod
    def fatal(msg, *args, **kwargs):
        bk_logger.fatal(msg, *args, **kwargs)
        if ISDEV:
            print(msg, *args)


logger = Logger()
