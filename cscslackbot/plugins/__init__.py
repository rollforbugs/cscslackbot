from __future__ import unicode_literals

from importlib import import_module
from cscslackbot.utils.logging import log_info

import config


# http://martyalchin.com/2008/jan/10/simple-plugin-framework/
class PluginLoader(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            if hasattr(cls, 'name'):
                log_info('Loading plugin {}'.format(cls.name))
                cls.plugins.append(cls())
            else:
                log_info('Loading plugin template {}'.format(cls.__name__))


class Plugin(object):
    # A plugin is expected to provide the following attributes:
    # name:          A short name for the plugin (module name if not given)
    # help_text:     [optional] A short string describing use of the plugin
    # help_para:     [optional] A full description of how to use the plugin
    #
    # process_event: [optional] A function to be called when a Slack event occurs
    __metaclass__ = PluginLoader


class Command(Plugin):
    # A plugin is expected to provide the following *additional* attributes:
    # command:         [optional] The command to respond to (copies name if not given)
    #
    # process_command: [optional] A function to be called when the command is given
    def __init__(self):
        super(Command, self).__init__()

        if not hasattr(self, 'command'):
            self.command = self.name

    def process_event(self, event):
        # Validate event
        if 'type' not in event:
            return
        if event['type'] != 'message':
            return
        if 'text' not in event:
            return

        # Get the message
        message = event['text'].strip()

        # Check if the message is calling this command
        command_prefix = config.prefix + self.command
        if not message.startswith(command_prefix):
            return

        # Call the command handler
        args = message[len(command_prefix):].strip()
        self.process_command(event, args=args)

    def process_command(self, event, args):
        pass


def load_plugins():
    plugin_module = config.plugin_dir.replace('/', '.')
    for plugin in config.plugins:
        import_module('{}.{}'.format(plugin_module, plugin))


def plugins_process_event(event):
    for p in Plugin.plugins:
        if hasattr(p, 'process_event'):
            p.process_event(event)
