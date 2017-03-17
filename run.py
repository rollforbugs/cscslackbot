#!/usr/bin/env python
import cscslackbot
import cscslackbot.slack as slack
from sys import argv

if __name__ == "__main__":
    # Args: [mode [script_name]]
    # python run.py
    # python run.py INTERACTIVE
    # python run.py SCRIPT tracked/quick_test_all.txt

    # TODO clean
    if len(argv) > 1:
        v = argv[1]
        if v == slack.MODE_SCRIPT:
            if len(argv) > 2:
                slack.script_file = argv[2]
            else:
                print ("file name needed")
                exit(1)
        if v not in slack.MODE_OPTIONS:
            slack.mode = slack.MODE_NORMAL
        else:
            slack.mode = v
    else:
        slack.mode = slack.MODE_NORMAL
    cscslackbot.run()
