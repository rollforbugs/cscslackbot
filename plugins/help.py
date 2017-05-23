from __future__ import unicode_literals

from cscslackbot.plugins import Command


class HelpCommand(Command):
    name = 'help'
    help_text = 'Displays help for plugins in DM'
    help_para = '''Displays short help for all command plugins when run without arguments.
Displays long help for a specific plugin when given that plugin as an argument.'''

    def make_help_string(self, plugin):
        if isinstance(plugin, Command):
            if hasattr(plugin, 'help_text'):
                string = 'Command: `{}{}` {}'.format(
                    self.config['command_prefix'],
                    plugin.command,
                    plugin.help_text
                )
            else:
                string = 'Command: `{}{}` {}'.format(
                    self.config['command_prefix'],
                    plugin.command,
                    'Help is missing for this command.'
                )
        else:
            if hasattr(plugin, 'help_text'):
                string = 'Plugin: `{}` {}'.format(
                    plugin.name,
                    plugin.help_text
                )
            else:
                string = 'Plugin: `{}` {}'.format(
                    plugin.name,
                    'Help is missing for this plugin.'
                )

        return string

    def process_command(self, event, args):
        if args == '':
            help_text = 'I have the following plugins enabled:'
            help_text += '\n'.join([self.make_help_string(plugin) for plugin in self.bot.plugins])
        else:
            help_text = 'No extended help for `{}`'.format(args)
            for plugin in self.bot.plugins:
                if plugin.name == args:
                    if hasattr(plugin, 'help_para'):
                        help_text = '`{}`:\n{}'.format(plugin.name, plugin.help_para)
                    break

        self.slack.send_message(event['user'], help_text)
