from __future__ import unicode_literals

from logging import getLogger

from builtins import input
from slackclient import SlackClient
from websocket import WebSocketConnectionClosedException

from cscslackbot.config import config, secrets

logger = getLogger(__name__)

###

mode = None
script_file = ''


class SlackState(object):
    MODE_NORMAL = 'NORMAL'
    MODE_INTERACTIVE = 'INTERACTIVE'
    MODE_SCRIPT = 'SCRIPT'

    MODE_OPTIONS = {MODE_NORMAL, MODE_INTERACTIVE, MODE_SCRIPT}


###

authed_user = ''
authed_user_id = ''
authed_team = ''
authed_team_id = ''
authed_team_url = ''
channels = []
client = SlackClient(secrets['SLACK_API_KEY'])


def connect():
    global client
    global authed_user, authed_user_id
    global authed_team, authed_team_id, authed_team_url
    global channels

    # Try to connect to Slack
    test_result = client.api_call('auth.test', token=secrets['SLACK_API_KEY'])
    if not test_result['ok']:
        logger.error('Could not connect to Slack! ({})'.format(test_result['error']))
        return False

    if not client.rtm_connect():
        logger.error('Could not connect to RTM API!')
        return False

    # Connected - set global variables for connection
    authed_user = test_result['user']
    authed_user_id = test_result['user_id']
    authed_team = test_result['team']
    authed_team_id = test_result['team_id']
    authed_team_url = test_result['url']
    channels = client.api_call('channels.list', exclude_archived=1)
    return True


def send_message(channel, message, **kwargs):
    if mode == SlackState.MODE_NORMAL:
        return client.api_call('chat.postMessage',
                               channel=channel,
                               text=message,
                               as_user=not config['debug_mode'],
                               **kwargs)
    elif mode == SlackState.MODE_INTERACTIVE or mode == SlackState.MODE_SCRIPT:
        print(message)


def get_events():
    try:
        if mode == SlackState.MODE_NORMAL:
            return client.rtm_read()
        elif mode == SlackState.MODE_INTERACTIVE:
            text = input("> ")
            return [mock_event(text)]
        elif mode == SlackState.MODE_SCRIPT:
            # pass
            with open("dev/scripts/" + script_file) as f:
                lines = f.readlines()
                return [mock_event(l) for l in lines]

        else:
            print ("Unhandled case!")
            return

    except WebSocketConnectionClosedException:
        logger.error('WebSocket connection for RTM API was closed!')
        if client.rtm_connect():
            return get_events()
        logger.critical('Could not reconnect!')


def mock_event(text):
    return {'type': 'message', 'channel': 'C494WSTUL', 'user': authed_user_id,
            'text': text}


def is_own_event(event):
    if 'user' in event:
        if event['user'] in (authed_user, authed_user_id):
            return True
    return False
