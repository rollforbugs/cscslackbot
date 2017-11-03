from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import time
from collections import defaultdict
from importlib import import_module
from six import iteritems

import cscslackbot.slack as slack
from cscslackbot.config import get_config, load_config, save_config
from cscslackbot.plugins import Plugin
from cscslackbot.slack import is_own_event
from cscslackbot.utils.path import list_files


class Slackbot:
    def __init__(self, config_path=None):
        self.config_path = config_path
        self.load_config()
        self.config = get_config(namespace='core')
        self.event_handlers = defaultdict(lambda: list())
        self.commands = {}

        self.slack = slack
        self.logger = logging.getLogger(__name__)

        self.plugins = {}
        for plugin in self.config['plugins']:
            self.load_plugin(plugin)

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

    def load_plugin(self, p):
        module_name = '{}.{}'.format(
            self.config['plugin_dir'].replace('/', '.'), p)

        # Load configuration
        namespace = 'plugins.{}'.format(p)
        defaults_file = '{}/{}/defaults.yml'.format(self.config['plugin_dir'], p)
        if os.path.exists(defaults_file):
            config.load_defaults(defaults_file, namespace=namespace)
        module_config = get_config(namespace=namespace)

        # Load the module
        mod = import_module(module_name)
        # Locate and register the Plugin object
        for objname, obj in iteritems(mod.__dict__):
            if isinstance(obj, Plugin):
                self.logger.info('Loading plugin: {}'.format(module_name))
                obj._load(bot=self, slack=self.slack, config=module_config)
                self.plugins[p] = obj
                for event_type, handlers in iteritems(obj._event_handlers):
                    self.event_handlers[event_type].extend(handlers)
                for command, handler in iteritems(obj._commands):
                    self.commands[command] = handler
                break

    def unload_plugin(self, p):
        self.logger.info('Unloading plugin: {}'.format(p))
        plugin = self.plugins[p]
        for command in plugin._commands:
            if command in self.commands:
                del self.commands[command]
        for event_type, handlers in iteritems(plugin._event_handlers):
            for handler in handlers:
                self.event_handlers[event_type].remove(handler)
            if not self.event_handlers[event_type]:
                del self.event_handlers[event_type]

        plugin.__unload()
        del self.plugins[p]

    def process_events(self):
        events = self.slack.get_events()
        if events is None:
            return
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

            for handler in self.event_handlers[event['type']]:
                handler(event)

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
