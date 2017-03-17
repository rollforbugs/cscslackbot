from __future__ import print_function
from __future__ import unicode_literals

import logging.config
import os.path

import yaml


config = {}
secrets = {}


def _dict_merge(merged, source, overwrite=False):
    for k in source.keys():
        if k not in merged:
            merged[k] = source[k]
        elif overwrite:
            merged[k] = source[k]


def load_config(config_file, defaults_file=None, section=None):
    global config
    load_config_defaults(defaults_file=defaults_file, section=section)

    open(config_file, 'a').close()
    with open(config_file, 'r') as f:
        loaded = yaml.safe_load(f)

    if not loaded:
        loaded = {}

    if section is None:
        _dict_merge(config, loaded, overwrite=True)
    elif section in config:
        _dict_merge(config[section], loaded, overwrite=True)
    else:
        config[section] = loaded


def load_config_defaults(defaults_file=None, section=None):
    global config

    if defaults_file is None:
        # Create an empty configuration section
        loaded = {}
    else:
        # Create a config section using the spec file
        with open(defaults_file, 'r') as f:
            loaded = yaml.safe_load(f)

    if section is None:
        # Merge into base config
        _dict_merge(config, loaded, overwrite=False)
    elif section in config:
        _dict_merge(config[section], loaded, overwrite=False)
    else:
        config[section] = loaded


def load_secrets(secrets_file):
    global secrets
    with open(secrets_file, 'r') as f:
        secrets = yaml.safe_load(f)


_cannot_load_config = False
# config.ini is created if it doesn't exist
if not os.path.exists('defaults.yml'):
    logging.critical("Please make sure 'defaults.yml' exists.")
    _cannot_load_config = True
if not os.path.exists('secrets.yml'):
    logging.critical("Please make sure 'secrets.yml' exists.")
    _cannot_load_config = True
if _cannot_load_config:
    logging.critical("Could not load configuration files!")
    exit()

load_config('config.yml', 'defaults.yml')
load_secrets('secrets.yml')
