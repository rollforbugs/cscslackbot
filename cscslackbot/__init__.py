from __future__ import print_function
from __future__ import unicode_literals

import config
import cscslackbot.plugins as plugins
import cscslackbot.slack as slack
from cscslackbot.utils.logging import log_info, log_error


def parse_command(event):
    plugins.plugins_process_event(event)


def run():
    if not slack.connect():
        log_error('Cannot connect to Slack. Please verify your token in the config.')
        return

    plugins.load_plugins()

    if config.debug_mode:
        slack.client.api_call('chat.postMessage',
                              channel='#bottesting',
                              text='{} is now testing.'.format(slack.authed_user))

    try:
        while True:
            events = slack.get_event()
            for event in events:
                log_info(str(event))

                if config.debug_mode:
                    # Whitelist #bottesting
                    if 'channel' not in event:
                        continue
                    if event['channel'] not in ['C494WSTUL', '#bottesting']:
                        continue
                    # Only respond to the developer when in debug mode
                    if 'user' not in event or event['user'] != slack.authed_user_id:
                        continue

                parse_command(event)
    except KeyboardInterrupt:
        if config.debug_mode:
            slack.send_message('#bottesting', 'I\'m dead! (SIGINT)')


if __name__ == '__main__':
    run()
