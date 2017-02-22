from __future__ import print_function
import config
import sys
import time


def log_info(message):
    print(time.strftime(config.time_format, time.gmtime()) + "  " + message)


def log_error(message):
    print(time.strftime(config.time_format, time.gmtime()) + "  " + message, file=sys.stderr)
