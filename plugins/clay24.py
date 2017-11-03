import re

from cscslackbot.plugins import Plugin

plugin = Plugin(__name__, 'Converts 24-hour time for Clayton')
TIME_REGEX = re.compile(r'[0-9]{2}:[0-9]{2}(:[0-9]{2})?')


@plugin.on('message')
def parse24to12(event):
    try:
        message = event['text']
    except KeyError:
        return

    matches = TIME_REGEX.search(message)
    if not matches:
        return

    time = matches.group(0)
    split = [int(x) for x in time.split(':')]
    if split[0] not in range(13, 24) and split[0] != 0:
        # Either not a valid hour or not 24-hour time
        return
    if split[1] not in range(0, 60):
        # Not a valid time
        return

    if len(split) == 2:
        hour, minute = split
        second = None
    elif len(split) == 3:
        hour, minute, second = split
    else:
        # One of the above should be true, but play it safe
        return

    # Adjust to 12-hour time
    hour = 12 if hour == 0 else hour - 12
    period = 'am' if hour == 0 else 'pm'

    if second is None:
        time = '{}:{} {}'.format(hour, minute, period)
    else:
        time = '{}:{}:{} {}'.format(hour, minute, second, period)

    plugin.slack.send_message(event['channel'], "That's {} for Clayton".format(time))
