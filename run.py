#!/usr/bin/env python
from __future__ import print_function

import argparse
import os

import cscslackbot
from cscslackbot.slack import SlackMode


def valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error('The script file `{}` does not exist!'.format(arg))
    else:
        return os.path.realpath(arg)


def main():
    # Usage: run.py [-h] [-i | -s SCRIPT]
    #   Run normally:       python run.py
    #   Display help:       python run.py -h
    #   Test interactively: python run.py -i
    #   Test with a script: python run.py -s dev/scripts/tracked/quick_test_all.txt

    parser = argparse.ArgumentParser(description='A Slack bot')
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('-i', '--interactive', action='store_true',
                            help='provide fake events interactively for testing')
    mode_group.add_argument('-s', '--script', type=lambda f: valid_file(parser, f))
    args = parser.parse_args()

    slack_mode = SlackMode.NORMAL
    slack_script = None
    if args.interactive:
        slack_mode = SlackMode.INTERACTIVE
    if args.script:
        slack_mode = SlackMode.SCRIPTED
        slack_script = args.script

    cscslackbot.run(slack_mode=slack_mode, slack_script=slack_script)


if __name__ == "__main__":
    main()
