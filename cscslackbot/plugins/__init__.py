from __future__ import unicode_literals

from importlib import import_module

import config

plugins = []


class Plugin(object):
    def __init__(self, name=None):
        self.name = name
        self.plugin_path = __file__

        if self.name is None:
            self.name = type(self).__module__.rsplit('.', 1)[1]

    def process_event(self, event):
        pass


class Command(Plugin):
    def __init__(self, command=None, help_text=None):
        super(Command, self).__init__()

        self.command = command
        self.help_text = help_text

        if self.command is None:
            self.command = self.name

        if self.help_text is None:
            self.help_text = 'There is no help for `{}`'.format(self.command)

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

    def process_command(self, event, args=None):
        pass


def register_plugin(plugin):
    plugins.append(plugin)


def load_plugins():
    for plugin in config.plugins:
        cls = import_module(plugin)


def plugins_process_event(event):
    for p in plugins:
        p.process_event(event)
