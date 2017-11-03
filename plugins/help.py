from __future__ import unicode_literals

from six import iteritems

from cscslackbot.config import get_config
from cscslackbot.plugins import Plugin

help_plugin = Plugin(__name__, 'Displays help for plugins and commands')

core_config = get_config(namespace='core')
command_prefix = core_config['commands']['prefix']


def first_line(s):
    if not s:
        return None

    for line in s.splitlines():
        if line:
            return line

    return None


def make_help_string(plugin):
    help = ['*{}*: {}'.format(plugin.name, plugin.description)]
    command_help = []
    for command, obj in iteritems(plugin._commands):
        command_help.append(
            '    `{}{}` {}'.format(
                command_prefix,
                command,
                first_line(obj.__doc__) or 'No help available'
            ))

    if command_help:
        help.append('Commands:')
        help.extend(command_help)

    return '\n'.join(help)


@help_plugin.command('help')
def show_help(event, args):
    if not args:
        help = 'I have the following plugins enabled:\n'
        help += '\n\n'.join([make_help_string(plugin) for plugin in help_plugin.bot.plugins.values()])
    else:
        if args.startswith(command_prefix):
            empty, command = args.split(command_prefix, 1)
            if command in help_plugin.bot.commands:
                help = help_plugin.bot.commands[command].__doc__
            else:
                help = 'Unknown command'

            help = '\n'.join([args, help])
        else:
            if args in help_plugin.bot.plugins:
                # TODO: Figure out extended help for plugins
                help = help_plugin.bot.plugins[args]
            else:
                help = "I'm not sure what that is"

    help_plugin.slack.send_message(event['user'], help)
