from __future__ import unicode_literals

import cscslackbot.slack as slack
from cscslackbot.plugins import Command
from random import randint

MAX_COUNT = 1e4
REASONABLE_COUNT = 1e3
MAX_FACES = 1e10
REASONABLE_FACES = 1e5


class HelloCommand(Command):
    name = 'roll'
    help_text = 'Rolls a die'

    def process_command(self, event, args):
        template = 'Rolled {}d{} and got {}'
        if args == '':
            slack.send_message(
                event['channel'],
                template.format(1, 6, randint(1, 6))
            )
            return
        else:
            # Get number of dice and faces in XdY notation
            count, d, faces = args.partition('d')
            if count == '':
                count = '1'
            if not (count.isdigit() and faces.isdigit()):
                slack.send_message(
                    event['channel'],
                    "I don't know how to roll a {}".format(args)
                )
                return

            # Convert to numbers
            count = int(count)
            faces = int(faces)
            # Prevent abuse
            if count > MAX_COUNT or faces > MAX_FACES:
                slack.send_message(
                    event['channel'],
                    "Jesus christ calm your shit"
                )
                return
            if faces > REASONABLE_FACES:
                slack.send_message(
                    event['channel'],
                    "What do you picture these dice even look like?"
                )
                return
            if count > REASONABLE_COUNT:
                slack.send_message(
                    event['channel'],
                    "There's a limit to the number of dice I can fit in my hand"
                )
                return
            if count == 0 or faces in (0, 1):
                slack.send_message(
                    event['channel'],
                    "What possible use would rolling that have?"
                )
                return
            if count < 0 or faces < 0:
                slack.send_message(
                    event['channel'],
                    "No."
                )
                return

            # Roll!
            rolls = []
            for i in range(count):
                rolls.append(randint(1, faces))

            message = template.format(count, faces, sum(rolls))
            # Show specific rolls if it wouldn't take up too much space
            if count > 1 and len(str(rolls)) < 150:
                message += ' ({})'.format(str(rolls))

            slack.send_message(event['channel'], message)
