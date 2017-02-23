from __future__ import unicode_literals

import cscslackbot.slack as slack
from cscslackbot.plugins import Command, register_plugin
from cscslackbot.utils.logging import log_info
from random import randint


class SlapCommand(Command):
    def process_command(self, event, args=None):
        name = args
        if name == '':
            return
        slapped = '{} was slapped! Hit {} times!'.format(name, randint(2, 5))
        slack.send_message(event['channel'], slapped)
        log_info('Responding to slap')

register_plugin(SlapCommand(
    help_text='Slaps a user'
))
