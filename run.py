#!/usr/bin/env python
from __future__ import print_function
import cscslackbot
import cscslackbot.slack as slack
from sys import argv, stderr


def main():
    # Args: [mode [script_name]]
    # python run.py
    # python run.py INTERACTIVE
    # python run.py SCRIPT tracked/quick_test_all.txt

    # TODO help?

    argc = len(argv)
    if argc == 1:
        slack.mode = slack.SlackState.MODE_NORMAL
    else:
        state = argv[1]
        if state not in slack.SlackState.MODE_OPTIONS:
            print("Invalid parameter", file=stderr)
            exit(1)

        slack.mode = state

        if state == slack.SlackState.MODE_SCRIPT:
            if argc == 3:
                slack.script_file = argv[2]
            else:
                print("file name needed", file=stderr)
                exit(1)
    ##

    cscslackbot.run()


if __name__ == "__main__":
    main()
