from __future__ import print_function
from __future__ import unicode_literals

import logging
import time

import cscslackbot.logconfig as logconfig
import cscslackbot.plugins as plugins
import cscslackbot.slack as slack
from cscslackbot.config import config, load_config, load_secrets

logger = logging.getLogger(__name__)


def process_event(event):
    if 'type' not in event:
        logger.error('Received message without type key: {}'.format(event))
        return
    plugins.plugins_process_event(event)


def run():
    # Configure logger
    if 'logging' in config:
        logconfig.configure(config['logging'])

    logger.info('Starting bot')

    if not slack.connect():
        logger.error('Cannot connect to Slack. Please verify your token in the config.')
        return
    else:
        logger.info('Connected to Slack as {} ({})'.format(slack.authed_user, slack.authed_user_id))

    plugins.load_plugins()

    try:
        while True:
            events = slack.get_events()
            for event in events:
                logger.debug(str(event))

                if config['debug_mode']:
                    # Whitelist #bottesting
                    if 'channel' not in event:
                        continue
                    if event['channel'] not in ['C494WSTUL', '#bottesting']:
                        continue
                    # Only respond to the developer when in debug mode
                    if 'user' not in event or event['user'] != slack.authed_user_id:
                        continue

                process_event(event)

            # Don't hog the CPU busy-waiting
            if slack.mode == slack.SlackState.MODE_NORMAL:
                time.sleep(0.1)
            # INTERACTIVE calls input which blocks
            elif slack.mode == slack.SlackState.MODE_SCRIPT:
                logger.info("End of script")
                break
    except KeyboardInterrupt:
        logger.info('Shutting down')
    except Exception as ex:
        logger.critical('Uncaught exception! ({})'.format(type(ex).__name__),
                        exc_info=True)
        if event:
            logger.critical('Last event: {}'.format(event))
        exit(-1)


