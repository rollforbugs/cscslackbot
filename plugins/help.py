from __future__ import unicode_literals

import config
import cscslackbot.slack as slack
from cscslackbot.plugins import Command
from cscslackbot.utils.logging import log_info


class HelpCommand(Command):
    name = 'help'
    help_text = 'Displays help for plugins'
    help_para = '''Displays short help for all command plugins when run without arguments.
Displays long help for a specific plugin when given that plugin as an argument.'''

    def process_command(self, event, args):
        help_text = ''
        if args == '':
            help_text = 'I support the following commands:\n'
            for plugin in Command.plugins:
                if hasattr(plugin, 'command'):
                    help_text += '`{}{}` '.format(config.prefix, plugin.command)
                    if hasattr(plugin, 'help_text'):
                        help_text += plugin.help_text
                    else:
                        help_text += 'Help is missing for this command.'
                    help_text += '\n'
        else:
            help_text = 'No extended help for `{}`'.format(args)
            for plugin in Command.plugins:
                if plugin.name == args:
                    if hasattr(plugin, 'help_para'):
                        help_text = '`{}`:\n{}'.format(plugin.name, plugin.help_para)
                    break

        slack.send_message(event['channel'], help_text)
        log_info('Responding to help')
