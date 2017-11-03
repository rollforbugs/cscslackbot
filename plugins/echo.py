from __future__ import unicode_literals

from cscslackbot.plugins import Plugin

plugin = Plugin(__name__, 'Echoes back messages')
"""
A plugin to echo back messages.

This is a very simple plugin that provides a command to echo back messages
to the user. It isn't terribly useful in practice, but is great for testing.
"""


@plugin.command('echo')
def echo(event, args):
    """
    Echo a message back.
    """
    plugin.slack.send_message(event['channel'], args)
