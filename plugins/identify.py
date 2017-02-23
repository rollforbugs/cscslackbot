from __future__ import unicode_literals

import cscslackbot.slack as slack
from cscslackbot.plugins import Command, register_plugin
from cscslackbot.utils.logging import log_info


class IdentifyCommand(Command):
    def process_command(self, event, args=None):
        slack.send_message(event['channel'],
                           '{}\'s bot, reporting in'.format(slack.authed_user))
        log_info('Responding to identify')

register_plugin(IdentifyCommand())
