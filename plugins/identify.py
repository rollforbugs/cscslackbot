from __future__ import unicode_literals

from cscslackbot.plugins import Command


class IdentifyCommand(Command):
    name = 'identify'
    help_text = 'Identifies the responding bot'

    def process_command(self, event, args):
        self.slack.send_message(event['channel'],
                                '{}\'s bot, reporting in'.format(self.slack.authed_user))
