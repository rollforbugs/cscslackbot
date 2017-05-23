from datetime import datetime

from cscslackbot.plugins import Command

start_time = datetime.now()


class UptimeCommand(Command):
    name = 'uptime'
    help_text = 'Provides the ammount of time the bot has been running'

    def process_command(self, event, args):
        now = datetime.now()
        diff = now - start_time

        resp = "Bot has been up since {} ({})"\
            .format(start_time.strftime(self.config['plugins']['uptime']['time_format']), str(diff).split(".")[0])
        self.slack.send_message(event['channel'], resp)
