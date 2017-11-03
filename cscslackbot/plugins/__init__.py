from __future__ import unicode_literals

import os
from collections import defaultdict
from logging import getLogger

from cscslackbot.config import get_config
from cscslackbot.slack import is_own_event

core_config = get_config('core')
logger = getLogger(__name__)


class Plugin(object):
    """
    A plugin for the Slack bot.

    The plugin will be initialized with a handle to the bot itself,
    the Slack object associated with the bot, and a configuration
    dictionary for the plugin to access its own configuration.
    """
    def __init__(self, name, description=''):
        if ''.endswith('.py'):
            name = os.path.split(name)[-1]
            name, ext = os.path.splitext(name)
        self.name = name
        self.description = description

        self._load_handler = None
        self._unload_handler = None
        self._event_handlers = defaultdict(lambda: list())
        self._commands = {}

        self.bot = None
        self.slack = None
        self.config = None
        self.logger = getLogger(name)

    def _load(self, bot, slack, config):
        """
        Initializes the plugin. This function should only be used internally by
        the Slackbot. After initializing basic state, __load calls the function
        specified with the on_load decorator.

        Args:
            bot (Slackbot): the Slackbot instance this plugin is registered to.
            slack: the Slack instance this plugin should use.
            config: the configuration dictionary for this plugin.
        """
        self.bot = bot
        self.slack = slack
        self.config = config

        self._event_handlers['message'].append(self._handle_command)
        if self._load_handler is not None:
            self._load_handler()

    def _unload(self):
        """
        Performs cleanup for the plugin. This function is internally used by
        the Slackbot and calls the function specified with on_unload.
        """
        if self._unload_handler is not None:
            self._unload_handler()

    def _handle_command(self, event):
        if 'text' not in event:
            return
        if not core_config['debug_mode']:
            if is_own_event(event):
                return

        # Get the message
        message = event['text'].strip()

        # Check that the message is calling this command
        prefix = core_config['commands']['prefix']
        if not message.startswith(prefix):
            return

        split = message.split(None, 1)
        if len(split) > 1:
            command, args = split
            args = args.strip()
        else:
            command, = split
            args = None

        empty, command = command.split(core_config['commands']['prefix'])
        if empty or command not in self._commands:
            return

        handler = self._commands[command]
        handler(event, args)

    def on_load(self):
        """
        A decorator that registers a function to be called when the plugin
        is loaded.

        All initialization for the plugin should be handled in a function
        with this decorator applied.
        """
        def decorator(f):
            self._load_handler = f
            return f
        return decorator

    def on_unload(self):
        """
        A decorator that registers a function to be called when the plugin
        is unloaded.

        All cleanup for the plugin should be handled in a function with
        this decorator applied.
        """
        def decorator(f):
            self._unload_handler = f
            return f
        return decorator

    def on(self, event_type):
        """
        A decorator that registers a function as a plugin event handler.

        :param event_type: The event type to handle, e.g., 'message'
        """
        def decorator(f):
            self._event_handlers[event_type].append(f)
            return f
        return decorator

    def command(self, command):
        """
        A decorator that registers a function as a plugin command.

        :param command: The command to respond to.
        """
        def decorator(f):
            self._commands[command] = f
            return f
        return decorator
