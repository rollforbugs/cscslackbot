from __future__ import unicode_literals

import cscslackbot.slack as slack
from cscslackbot.plugins import Command, register_plugin
from cscslackbot.utils.logging import log_info


class HelloCommand(Command):
    def process_command(self, event, args=None):
        greeting = 'Hey! :partyparrot:'
        if 'user' in event:
            user = event['user']
            greeting = 'Hey <@{}>! :partyparrot:'.format(user)
        slack.send_message(event['channel'], greeting)
        log_info('Responding to hello')

register_plugin(HelloCommand(
    help_text='Sends you a friendly welcome!'
))
