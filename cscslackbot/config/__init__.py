from __future__ import unicode_literals

import logging
import logging.config
import logging.handlers
import os.path
import sys

import yaml

from cscslackbot.utils import from_human_readable
from cscslackbot.utils.path import list_files


logger = logging.getLogger(__name__)

config_path = None

_config = {}
namespaces = []


def _dict_merge(merged, source, overwrite=False):
    for k in source.keys():
        if k not in merged:
            merged[k] = source[k]
        elif isinstance(merged[k], dict) and isinstance(source[k], dict):
            _dict_merge(merged[k], source[k], overwrite=overwrite)
        elif overwrite:
            merged[k] = source[k]


def _configure_logging():
    config = get_config(namespace='logging')

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


def get_config(namespace=None):
    config = _config
    if namespace is None:
        return config

    namespaces.append(namespace)
    components = namespace.split('.')
    for component in components:
        if component not in config:
            config[component] = {}
        config = config[component]

    return config


def get_value(key, default=None, namespace=None):
    config = get_config(namespace)
    try:
        return config[key]
    except KeyError:
        return default


def set_value(key, value, namespace=None):
    config = get_config(namespace)
    config[key] = value


def load_config(filename, namespace=None, overwrite=True):
    config = get_config(namespace)
    with open(filename, 'r') as f:
        loaded = yaml.safe_load(f)

    if not loaded:
        loaded = {}

    _dict_merge(config, loaded, overwrite=overwrite)


def load_defaults(filename, namespace=None):
    return load_config(filename, namespace=namespace, overwrite=False)


def save_config(filename, namespace=None):
    config = get_config(namespace)
    with open(filename, 'w') as f:
        yaml.safe_dump(config, f)


def reload_config_files():
    if os.path.isfile(config_path):
        print('Flat config file: {}'.format(config_path))
        load_config(config_path)
    elif os.path.isdir(config_path):
        print('Config directory: {}'.format(config_path))
        for f in list_files(config_path):
            rel = os.path.relpath(f, config_path)
            print('Loading config file: {}'.format(rel))
            namespace, ext = os.path.splitext(rel)
            namespace = namespace.replace(os.path.sep, '.')
            load_config(f, namespace=namespace)

    _configure_logging()


if not config_path:
    config_path = os.getenv('SLACKBOT_CONFIG', None)
if not config_path:
    if os.path.isfile('config.yml'):
        config_path = 'config.yml'
    elif os.path.isdir('config'):
        config_path = 'config'

if config_path:
    reload_config_files()
