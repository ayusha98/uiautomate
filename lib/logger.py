# -*- coding: utf-8 -*-
import os
import logging
import datetime as dt


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):

        # Only create an instance if not already created
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object, metaclass=SingletonType):
    _logger = None
    # __metaclass__ = SingletonType     # python 2 style

    def __init__(self, file_name=''):
        self._logger = logging.getLogger("robocop")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s|'
                                      '<%(process)d>| -- %(message)s')

        now = dt.datetime.now()
        current_path = os.getcwd()
        dirname = os.path.join(current_path[:current_path.find('uiautomate')], 'uiautomate', 'logs')

        if not os.path.isdir(dirname):
            os.mkdir(dirname)
        if not file_name:
            file_name = os.path.join(dirname, "z_{0}.log".format(now.strftime("%y-%m-%d")))
        fileHandler = logging.FileHandler(file_name)

        if os.path.isfile(file_name):
            try:
                os.chmod(file_name, 0o777)
            except OSError:
                pass

        # also create a stream handler, logging is also displayed on console output
        streamHandler = logging.StreamHandler()

        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)
        streamHandler.setLevel(logging.INFO)
        logging.getLogger('chardet.charsetprober').setLevel(logging.INFO)

    def get_logger(self):
        return self._logger


def logged(func):

    # this function can be used as decorator,
    # where we want to see the transaction details,
    # basic details can be easily captured from logs itself

    log = Logger.__call__().get_logger()

    def run(*args, **kwargs):
        log.info("trans_start|{0}".format(func.__name__))
        out = func(*args, **kwargs)
        log.info("trans_end|{0}".format(func.__name__))
        return out

    return run
