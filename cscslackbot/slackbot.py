from __future__ import unicode_literals

import logging
import time

import cscslackbot.logconfig as logconfig
from cscslackbot.plugins import PluginLoader
from cscslackbot.slack import Slack, PseudoSlackScripted, PseudoSlackInteractive, SlackMode


class Slackbot:
    def __init__(self, config, slack_mode=SlackMode.NORMAL, slack_script=None):
        self.config = config
        if 'logging' in self.config:
            logconfig.configure(self.config['logging'])

        # Set up Slack
        self.slack_mode = slack_mode
        if slack_mode == SlackMode.NORMAL:
            self.slack = Slack(config)
        elif slack_mode == SlackMode.SCRIPTED:
            self.slack = PseudoSlackScripted(config, slack_script)
        elif slack_mode == SlackMode.INTERACTIVE:
            self.slack = PseudoSlackInteractive(config)

        self.logger = logging.getLogger(__name__)
        self.plugins = []

    def load_plugins(self):
        loader = PluginLoader(self.config, self.slack, self)
        to_load = self.config['enabled_plugins']
        plugin_dir = self.config['plugin_dir']
        self.plugins = loader.load_plugins(to_load, plugin_dir)

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

        self.load_plugins()

        # Always parse events at least once
        self.process_events()
        # If we're not scripted, keep going
        if self.slack_mode in (SlackMode.NORMAL, SlackMode.INTERACTIVE):
            while True:
                self.process_events()

                # Don't hog the CPU busy-waiting
                time.sleep(0.1)
