from __future__ import unicode_literals

import cscslackbot.slack as slack
from cscslackbot.plugins import Command, register_plugin
from cscslackbot.utils.logging import log_info


class EchoCommand(Command):
    def process_command(self, event, args=None):
        slack.send_message(event['channel'], args)
        log_info('Responding to echo')

register_plugin(EchoCommand())
