import logging
import logging.config
import logging.handlers
import sys

from ..utils import from_human_readable


def configure(config):
    format = config.get('format', None)
    datefmt = config.get('datefmt', None)
    formatter = logging.Formatter(format, datefmt)
    handlers = []

    # Console handler
    h = logging.StreamHandler(sys.stdout)
    h.setLevel(config['console']['level'])
    h.setFormatter(formatter)
    handlers.append(h)

    # File handlers
    for f in config['files']:
        file_config = config['files'][f]
        maxsize = file_config.get('maxsize', '1M')
        maxsize = from_human_readable(str(maxsize))
        count = file_config.get('count', 1)

        h = logging.handlers.RotatingFileHandler(f, maxBytes=maxsize, backupCount=count)
        h.setLevel(file_config['level'])
        h.setFormatter(formatter)

        handlers.append(h)

    logging.getLogger().setLevel(logging.DEBUG)
    for h in handlers:
        logging.getLogger().addHandler(h)
