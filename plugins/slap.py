from __future__ import unicode_literals

import cscslackbot.slack as slack
from cscslackbot.plugins import Command
from cscslackbot.utils.logging import log_info
from random import randint


class SlapCommand(Command):
    name = 'slap'
    help_text = 'Slaps a user'

    def process_command(self, event, args):
        name = args
        if name == '':
            return
        slapped = '{} was slapped! Hit {} times!'.format(name, randint(2, 5))
        slack.send_message(event['channel'], slapped)
        log_info('Responding to slap')
