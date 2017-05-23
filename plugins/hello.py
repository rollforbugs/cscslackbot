from __future__ import unicode_literals

from cscslackbot.plugins import Command


class HelloCommand(Command):
    name = 'hello'
    help_text = 'Sends you a friendly welcome'

    def process_command(self, event, args):
        greeting = 'Hey! :partyparrot:'
        if 'user' in event:
            user = event['user']
            greeting = 'Hey <@{}>! :partyparrot:'.format(user)
        self.slack.send_message(event['channel'], greeting)
