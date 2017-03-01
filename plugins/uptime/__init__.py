from datetime import datetime

import cscslackbot.slack as slack
from cscslackbot.plugins import Command

start_time = datetime.now()


class UptimeCommand(Command):
    name = 'uptime'
    help_text = 'Provides the ammount of time the bot has been running'

    def process_command(self, event, args):
        now = datetime.now()
        diff = now - start_time

        resp = "Bot has been up since {} ({})"\
            .format(start_time.strftime(self.config['time_format']), str(diff).split(".")[0])
        slack.send_message(event['channel'], resp)
