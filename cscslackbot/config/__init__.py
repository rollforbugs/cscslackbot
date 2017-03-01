from __future__ import unicode_literals
from __future__ import print_function

import os.path
import sys

from configobj import ConfigObj
from validate import Validator

_validator = Validator()
config = ConfigObj(encoding='UTF8')
secrets = ConfigObj(encoding='UTF8')


def load_config(config_file, spec_file=None, section=None):
    global config
    load_config_defaults(spec_file=spec_file, section=section)

    loaded = ConfigObj(config_file, configspec=spec_file, encoding='UTF8', create_empty=True)
    loaded.validate(_validator)

    if section is None:
        config.merge(loaded)
    else:
        config[section].merge(loaded)


def load_config_defaults(spec_file=None, section=None):
    global config
    if spec_file is None:
        # Create an empty configuration section
        loaded = ConfigObj(encoding='UTF8')
    else:
        # Create a config section using the spec file
        loaded = ConfigObj(configspec=spec_file, encoding='UTF8')
        loaded.validate(_validator)

    if section is None:
        # Merge into base config
        config.merge(loaded)
    else:
        # Merge old entries if applicable then set section
        if section in config:
            loaded.merge(config[section])
        config[section] = loaded


def load_secrets(secrets_file):
    global secrets
    secrets = ConfigObj(secrets_file, encoding='UTF8')


cannot_load_config = False
# config.ini is created if it doesn't exist
if not os.path.exists('defaults.ini'):
    print("Please make sure 'defaults.ini' exists.", file=sys.stderr)
    cannot_load_config = True
if not os.path.exists('secrets.ini'):
    print("Please make sure 'secrets.ini' exists.", file=sys.stderr)
    cannot_load_config = True
if cannot_load_config:
    exit()

load_config('config.ini', 'defaults.ini')
load_secrets('secrets.ini')
