from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import time

import cscslackbot.slack as slack

from cscslackbot.config import get_config, load_config, save_config
from cscslackbot.plugins import Plugin
from cscslackbot.utils.path import list_files


class Slackbot:
    def __init__(self, config_path=None):
        self.config_path = config_path
        self.load_config()
        self.config = get_config(namespace='core')
        self.slack = slack
        self.logger = logging.getLogger(__name__)
        self.plugins = Plugin.plugins

    def load_config(self):
        if os.path.isfile(self.config_path):
            print('Flat config file: {}'.format(self.config_path))
            load_config(self.config_path)
        elif os.path.isdir(self.config_path):
            print('Config directory: {}'.format(self.config_path))
            for f in list_files(self.config_path):
                rel = os.path.relpath(f, self.config_path)
                print('Loading config file: {}'.format(rel))
                namespace, ext = os.path.splitext(rel)
                namespace = namespace.replace(os.path.sep, '.')
                load_config(f, namespace=namespace)

    def process_events(self):
        events = self.slack.get_events()
        for event in events:
            self.logger.debug(str(event))

            if self.config['debug_mode']:
                # Whitelist #bottesting
                if 'channel' not in event:
                    continue
                if event['channel'] not in ['C494WSTUL', '#bottesting']:
                    continue
                # Only respond to the developer when in debug mode
                if 'user' not in event or event['user'] != self.slack.authed_user_id:
                    continue

            if 'type' not in event:
                self.logger.error('Received message without type key: {}'.format(event))
                continue

            for p in self.plugins:
                if hasattr(p, 'process_event'):
                    p.process_event(event)

    def run(self):
        self.logger.info('Starting bot')

        if not self.slack.connect():
            self.logger.error('Cannot connect to Slack. Please verify your token in the config.')
            return
        else:
            self.logger.info('Connected to Slack as {} ({})'.format(self.slack.authed_user, self.slack.authed_user_id))

        while True:
            self.process_events()

            # Don't hog the CPU busy-waiting
            time.sleep(0.1)
