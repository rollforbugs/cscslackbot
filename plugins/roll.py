from __future__ import unicode_literals

import math
import re
from random import randint, gauss

import cscslackbot.slack as slack
from cscslackbot.plugins import Command

MAX_COUNT = 1e4
REASONABLE_COUNT = 1e3
MAX_FACES = 1e10
REASONABLE_FACES = 1e5
XDY_REGEX = re.compile(r'([0-9]+)?d([0-9]+)', re.IGNORECASE)


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
            xdy = XDY_REGEX.search(args)
            if not xdy:
                slack.send_message(
                    event['channel'],
                    "What did you want me to roll?"
                )
                return

            # Extract count and faces
            count, faces = xdy.groups()
            if count:
                count = int(count)
            else:
                count = 1
            faces = int(faces)

            # Prevent abuse
            msg = None
            if count > MAX_COUNT or faces > MAX_FACES:
                msg = "Jesus christ calm your shit"
            elif faces > REASONABLE_FACES:
                msg = "What do you picture these dice even look like?"
            elif count > REASONABLE_COUNT:
                msg = "There's a limit to the number of dice I can fit in my hand"
            elif count == 0 or faces in (0, 1):
                msg = "What possible use would rolling that have?"
            elif count < 0 or faces < 0:
                msg = "No."
            if msg:
                slack.send_message(event['channel'], msg)
                return

            # Roll!
            rolls = [randint(1, faces) for i in range(count)]

            message = template.format(count, faces, sum(rolls))
            # Show specific rolls if it wouldn't take up too much space
            # Setting a max count would be more performant
            roll_rep = str(rolls)
            if count > 1 and len(roll_rep) < 150:
                message += ' {}'.format(roll_rep)

            slack.send_message(event['channel'], message)


def approximate_roll(m, n):
    """
    Approximates the value of rolling m n-sided die.

    Reference http://math.stackexchange.com/questions/406192/probability-distribution-of-rolling-multiple-dice

    Args:
        m (int): number of dice [1, inf)
        n (int): number of faces [2, inf)

    Returns:
        (int) A random value based on the distribution of dice.

    """
    if m < 1 or n < 2:
        return 0

    if m == 1:
        return randint(1, n)
    # Properties of a single n-faced die
    mean = (n + 1) / 2.0
    variance = (n * n - 1) / 12.0
    # Properties of the distribution
    mu = m * mean
    sigma = math.sqrt(m * variance)

    v = int(gauss(mu, sigma))
    v = clamp(v, m, m * n)
    return v


def clamp(x, lower, upper):
    return lower if x < lower else upper if x > upper else x
