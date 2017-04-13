from __future__ import unicode_literals

from logging import getLogger

from slackclient import SlackClient

from cscslackbot.config import config, secrets


logger = getLogger(__name__)

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
    return client.api_call('chat.postMessage',
                           channel=channel,
                           text=message,
                           as_user=not config['debug_mode'],
                           **kwargs)


def get_event():
    try:
        return client.rtm_read()
    except WebSocketConnectionClosedException:
        logger.error('WebSocket connection for RTM API was closed!')
        if client.rtm_connect():
            return get_event()
        logger.critical('Could not reconnect!')

