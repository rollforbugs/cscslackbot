from __future__ import unicode_literals

import cscslackbot.slack as slack
from cscslackbot.plugins import Command, register_plugin
from cscslackbot.utils.logging import log_info


class HelpCommand(Command):
    def process_command(self, event, args=None):
        slack.send_message(event['channel'],
                           'Right now, I support the following commands:\n'
                           + '`!help`\n`!hello`\n`!slap`\n`!identify`\n'
                           + 'This help is also literally just a string right now.\n'
                           + 'A more robust architecture would be nice.')
        log_info('Responding to help')

register_plugin(HelpCommand())
