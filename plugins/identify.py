from __future__ import unicode_literals

from cscslackbot.plugins import Plugin

plugin = Plugin(__name__, 'Identify a running bot')


@plugin.command('identify')
def identify(event, args):
    """
    Causes the running bot to identify itself
    """
    plugin.slack.send_message(
        event['channel'],
        '{}\'s bot, reporting in'.format(plugin.slack.authed_user))
