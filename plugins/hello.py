from __future__ import unicode_literals

import cscslackbot.slack as slack
from cscslackbot.plugins import Command
from cscslackbot.utils.logging import log_info


class HelloCommand(Command):
    name = 'hello'
    help_text = 'Sends you a friendly welcome'

    def process_command(self, event, args):
        greeting = 'Hey! :partyparrot:'
        if 'user' in event:
            user = event['user']
            greeting = 'Hey <@{}>! :partyparrot:'.format(user)
        slack.send_message(event['channel'], greeting)
        log_info('Responding to hello')
