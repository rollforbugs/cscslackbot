from __future__ import unicode_literals

from datetime import datetime

from cscslackbot.plugins import Plugin

plugin = Plugin(__name__, 'Track bot uptime')
start_time = datetime.now()


@plugin.command('uptime')
def uptime(event, args):
    """
    Displays the amount of time the bot has been running
    """
    now = datetime.now()
    diff = now - start_time

    resp = "Bot has been up since {} ({})"\
        .format(start_time.strftime(plugin.config['time_format']), str(diff).split(".")[0])
    plugin.slack.send_message(event['channel'], resp)
