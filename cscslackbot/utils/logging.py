from __future__ import print_function

import sys
import time

from cscslackbot.config import config


def log_info(message):
    print(time.strftime(config['time_format'], time.gmtime()) + "  " + message)


def log_error(message):
    print(time.strftime(config['time_format'], time.gmtime()) + "  " + message, file=sys.stderr)
