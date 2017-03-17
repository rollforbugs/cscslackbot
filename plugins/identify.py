from __future__ import unicode_literals

import cscslackbot.slack as slack
from cscslackbot.plugins import Command


class IdentifyCommand(Command):
    name = 'identify'
    help_text = 'Identifies the responding bot'

    def process_command(self, event, args):
        slack.send_message(event['channel'],
                           '{}\'s bot, reporting in'.format(slack.authed_user))
