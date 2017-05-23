from __future__ import unicode_literals

import os
from importlib import import_module
from logging import getLogger

from six import with_metaclass

from cscslackbot.config import Configuration, dict_merge


logger = getLogger(__name__)
active_loader = None
loaded_plugins = []


class PluginLoader:
    def __init__(self, config, slack, bot):
        self.config = config
        self.slack = slack
        self.bot = bot

    def load_plugins(self, plugins, plugin_dir):
        global active_loader
        active_loader = self

        plugin_module = plugin_dir.replace('/', '.')
        for plugin in plugins:
            # Try to load config defaults
            defaults_file = '{}/{}/defaults.yml'.format(plugin_dir, plugin)
            defaults = Configuration()
            if os.path.exists(defaults_file):
                defaults.load_defaults(defaults_file)
            else:
                self.config.load_defaults()

            if plugin not in active_loader.config['plugins']:
                active_loader.config['plugins'][plugin] = defaults
            else:
                dict_merge(active_loader.config['plugins'][plugin], defaults, overwrite=False)

            # Load the module
            import_module('{}.{}'.format(plugin_module, plugin))

        # Restore original state of global variables
        loaded = []
        while len(loaded_plugins) > 0:
            loaded.append(loaded_plugins.pop(0))
        active_loader = None

        return loaded


class PluginType(type):
    def __init__(cls, name, bases, attrs):
        if hasattr(cls, 'name'):
            logger.info('Loading plugin {}'.format(cls.name))
            loaded_plugins.append(cls(config=active_loader.config,
                                      slack=active_loader.slack,
                                      bot=active_loader.bot))
        else:
            logger.info('Loading plugin template {}'.format(cls.__name__))


class Plugin(with_metaclass(PluginType, object)):
    # A plugin is expected to provide the following attributes:
    # name:          A short name for the plugin (module name if not given)
    # help_text:     [optional] A short string describing use of the plugin
    # help_para:     [optional] A full description of how to use the plugin
    #
    # process_event: [optional] A function to be called when a Slack event occurs
    def __init__(self, config, slack, bot):
        super(Plugin, self).__init__()

        self.config = config
        self.slack = slack
        self.bot = bot

        if not hasattr(self, 'name'):
            self.name = self.__module__

    def process_event(self, event):
        pass


class Command(Plugin):
    # A plugin is expected to provide the following *additional* attributes:
    # command:         [optional] The command to respond to (copies name if not given)
    #
    # process_command: [optional] A function to be called when the command is given
    def __init__(self, config, slack, bot):
        super(Command, self).__init__(config, slack, bot)

        if not hasattr(self, 'command'):
            self.command = self.name

    def process_event(self, event):
        # Validate event
        if event['type'] != 'message':
            return
        if 'text' not in event:
            return
        if not self.config['debug_mode']:
            if self.slack.is_own_event(event):
                return

        # Get the message
        message = event['text'].strip()

        # Check if the message is calling this command
        command_prefix = self.config['command_prefix'] + self.command.lower()
        if not message.lower().startswith(command_prefix):
            return

        # Call the command handler
        args = message[len(command_prefix):].strip()
        self.process_command(event, args=args)

    def process_command(self, event, args):
        pass
