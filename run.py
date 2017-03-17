#!/usr/bin/env python
import cscslackbot
import cscslackbot.slack as slack
from sys import argv

if __name__ == "__main__":
    # Args: mode
    if len(argv) > 1:
        v = argv[1]
        if v not in slack.MODE_OPTIONS:
            slack.mode = slack.MODE_NORMAL
        else:
            slack.mode = v
    else:
        slack.mode = slack.MODE_NORMAL
    cscslackbot.run()
