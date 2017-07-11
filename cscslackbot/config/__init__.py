from __future__ import unicode_literals

import os.path

import yaml

from cscslackbot.utils.path import list_files


CONFIG_PATH = 'config'

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


def reload_config_files(config_path):
    if os.path.isfile(config_path):
        load_config(config_path)
    elif os.path.isdir(config_path):
        for f in list_files(config_path):
            rel = os.path.relpath(f, config_path)
            namespace, ext = os.path.splitext(rel)
            namespace = namespace.replace(os.path.sep, '.')
            load_config(f, namespace=namespace)


reload_config_files(CONFIG_PATH)
