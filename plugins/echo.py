from __future__ import unicode_literals

import cscslackbot.slack as slack
from cscslackbot.plugins import Command


class EchoCommand(Command):
    name = 'echo'
    help_text = 'Echoes a message back'

    def process_command(self, event, args):
        self.slack.send_message(event['channel'], args)
