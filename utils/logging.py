import config
import time


def log_info(message):
    print(time.strftime(config.time_format, time.gmtime()) + "  " + message)
