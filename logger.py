# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json
import logging
import sys
from logentries import LogentriesHandler
import warnings
warnings.filterwarnings("ignore")
reload(sys)
sys.setdefaultencoding('utf8')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(object):
    __metaclass__ = Singleton
    __LOGGER = 'logentries'
    __LOG_TOKEN = os.environ.get('LOGENTRIES_TOKEN', '')

    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET

    def __init__(self):
        self.log_now = False
        self.to_log = {}
        self._default_params = {}
        self.log_entity = logging.getLogger(Logger.__LOGGER)
        self.log_entity.addHandler(LogentriesHandler(Logger.__LOG_TOKEN, verbose=False))
    def log(self, log_type=INFO, log_now=False, **params):
        self.log_now = log_now
        self.to_log.update(params)
        if self.log_now:
            output = dict(self.to_log.items() + self._default_params.items())
            try:
                output = json.dumps(output, ensure_ascii=False, encoding='UTF-8', default=str)
            except Exception:
                output = str(output.encode("utf-8"))
            if os.environ.get('C_ENVIRONMENT', False):
                self.log_entity.setLevel(log_type)
                self.log_entity.log(self.log_entity.level, output.encode("utf-8"))
            else:
                print(output.encode("utf-8"))
                print('-------------------------------------')
            self.log_now = False
            self.clean_logs()

    def clean_logs(self):
        self.to_log = {}

    def set_default_params(self, **kwargs):
        self._default_params = {'Info': dict(kwargs)}

    def update_default_params(self, **kwargs):
        self._default_params['Info'].update(kwargs)

    def clear_default_params(self):
        self._default_params = {}