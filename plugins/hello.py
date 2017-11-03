from __future__ import unicode_literals

from cscslackbot.plugins import Plugin


plugin = Plugin(__name__, 'Sends you a friendly welcome')


@plugin.command('hello')
def greet(event, args):
    """
    Make a little friendly conversation
    """
    greeting = 'Hey! :partyparrot:'
    if 'user' in event:
        user = event['user']
        greeting = 'Hey <@{}>! :partyparrot:'.format(user)
    plugin.slack.send_message(event['channel'], greeting)
