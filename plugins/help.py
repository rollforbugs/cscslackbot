from __future__ import unicode_literals

import config
import cscslackbot.slack as slack
from cscslackbot.plugins import Command, register_plugin, plugins
from cscslackbot.utils.logging import log_info


class HelpCommand(Command):
    def process_command(self, event, args=None):
        help_text = ''
        if args == '':
            help_text = 'Right now, I support the following commands:\n'
            for plugin in plugins:
                # All commands have help text
                if hasattr(plugin, 'command'):
                    help_text += '`{}{}` '.format(config.prefix, plugin.command)
                    help_text += plugin.help_text
                    help_text += '\n'
        else:
            for plugin in plugins:
                if plugin.name == args and hasattr(plugin, 'help_text'):
                    help_text = plugin.help_text

        slack.send_message(event['channel'], help_text)
        log_info('Responding to help')

register_plugin(HelpCommand(
    help_text='Displays help to a user'
))
