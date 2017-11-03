from __future__ import unicode_literals

import math
import re
from random import randint, gauss

from builtins import range

from cscslackbot.plugins import Plugin
from cscslackbot.utils import clamp

XDY_REGEX = re.compile(r'([0-9]+)?d([0-9]+)', re.IGNORECASE)


plugin = Plugin(__name__, 'Rolls dice')


lastdice = None
lastfaces = None


@plugin.command('roll')
def roll(event, args):
    """
    Roll dice in XdY format.

    If X is low enough, the individual rolls will be displayed.
    """
    template = 'Rolled {}d{} and got {}'

    if not args:
        dice = 1
        faces = 6
        message = template.format(dice, faces, _roll(dice, faces)[0])
    else:
        # Get number of dice and faces in XdY notation
        xdy = XDY_REGEX.search(args)
        if not xdy:
            plugin.slack.send_message(
                event['channel'],
                "What did you want me to roll?"
            )
            return

        # Extract count and faces
        dice, faces = xdy.groups()
        if dice:
            dice = int(dice)
        else:
            dice = 1
        faces = int(faces)

        # Prevent abuse
        message = None
        if dice > plugin.config['max_count'] or faces > plugin.config['max_faces']:
            message = "Jesus christ calm your shit"
        elif faces > plugin.config['reasonable_faces']:
            message = "What do you picture these dice even look like?"
        elif dice > plugin.config['reasonable_count']:
            message = "There's a limit to the number of dice I can fit in my hand"
        elif dice == 0 or faces in (0, 1):
            message = "What possible use would rolling that have?"
        elif dice < 0 or faces < 0:
            message = "No."
        else:
            # Actually roll the dice!
            global lastdice, lastfaces
            lastdice = dice
            lastfaces = faces

            value, rolls = _roll(dice, faces)
            if rolls and len(rolls) > 1:
                message = (template + ' {}').format(dice, faces, value, rolls)
            else:
                message = template.format(dice, faces, value)

    plugin.slack.send_message(event['channel'], message)


@plugin.command('reroll')
def reroll(event, args):
    """
    Rerolls the last set of dice rolled.
    """
    if lastdice is None or lastfaces is None:
        plugin.slack.send_message(event['channel'], "You have to roll in the first place!")
        return

    template = 'Rolled {}d{} and got {}'
    value, rolls = _roll(lastdice, lastfaces)
    if rolls:
        message = (template + ' {}').format(lastdice, lastfaces, value, rolls)
    else:
        message = template.format(lastdice, lastfaces, value)

    plugin.slack.send_message(event['channel'], message)


def _roll(dice=1, faces=6):
    if dice == 1:
        # Only roll one die
        value = randint(1, faces)
        rolls = [value]
    elif dice <= plugin.config['displayable_count']:
        # Consider individual rolls
        rolls = [randint(1, faces) for x in range(dice)]
        value = sum(rolls)
    else:
        # Use probability distribution
        value = approximate_roll(dice, faces)
        rolls = None

    return value, rolls


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
