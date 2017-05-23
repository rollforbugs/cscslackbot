from __future__ import unicode_literals

import logging
import os

from cscslackbot.config import Configuration
from cscslackbot.slackbot import Slackbot
from cscslackbot.slack import SlackMode

CONFIG_FILE = 'config.yml'
DEFAULTS_FILE = 'defaults.yml'
SECRETS_FILE = 'secrets.yml'
logger = logging.getLogger(__name__)


def load_config(config_file=None, defaults_file=None, secrets_file=None):
    conf = Configuration()
    cannot_load_config = False

    if defaults_file and not os.path.isfile(defaults_file):
        logger.critical("Please make sure '{}' exists.".format(defaults_file))
        cannot_load_config = True
    if secrets_file and not os.path.exists(secrets_file):
        logger.critical("Please make sure '{}' exists.".format(secrets_file))
        cannot_load_config = True

    if cannot_load_config:
        logger.critical("Could not load configuration files!")
    else:
        conf.load(config_file, defaults_file)
        conf.load_secrets(secrets_file)

    return conf


def run(slack_mode=SlackMode.NORMAL, slack_script=None):
    try:
        conf = load_config(CONFIG_FILE, DEFAULTS_FILE, SECRETS_FILE)
        print(conf)
        bot = Slackbot(conf, slack_mode=slack_mode, slack_script=slack_script)
        bot.run()
    except KeyboardInterrupt:
        logger.info('Shutting down')
    except:
        logger.critical('Uncaught exception!', exc_info=True)
        exit(-1)
