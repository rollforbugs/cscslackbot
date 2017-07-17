#!/usr/bin/env python
from __future__ import print_function

import argparse
import os

from cscslackbot import Slackbot


def valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error('Cannot find file: `{}`'.format(arg))
    else:
        return os.path.realpath(arg)


def valid_path(parser, arg):
    if not os.path.exists(arg):
        parser.error('Cannot find file or directory: `{}`'.format(arg))
    else:
        return os.path.realpath(arg)


def main():
    """
    Run a copy of the Slack bot.

    Usage: run.py [-h] [-i | -s SCRIPT]
      Run normally:       python run.py
      Display help:       python run.py -h
      Test interactively: python run.py -i
      Test with a script: python run.py -s script.txt
    """

    parser = argparse.ArgumentParser(description='A Slack bot')
    parser.add_argument('-c', '--config', type=lambda f: valid_file(parser, f),
                        help='path to config file or directory')
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('-i', '--interactive', action='store_true',
                            help='provide fake events interactively for testing')
    mode_group.add_argument('-s', '--script', type=lambda f: valid_file(parser, f),
                            help='a script of fake events for testing')
    args = parser.parse_args()

    config_path = None
    if args.config:
        config_path = args.config
    else:
        # Try default paths
        if os.path.isfile('config.yml'):
            config_path = 'config.yml'
        elif os.path.isdir('config'):
            config_path = 'config'

    bot = Slackbot(config_path=config_path)
    bot.run()


if __name__ == "__main__":
    main()
