from __future__ import unicode_literals

from random import randint

from cscslackbot.plugins import Plugin

plugin = Plugin(__name__, 'Slap people!')


@plugin.command('slap')
def slap(event, args):
    name = args
    if not name:
        return
    slapped = '{} was slapped! Hit {} times!'.format(name, randint(2, 5))
    plugin.slack.send_message(event['channel'], slapped)
