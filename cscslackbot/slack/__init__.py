from __future__ import unicode_literals

from logging import getLogger

from six.moves import input
from slackclient import SlackClient
from websocket import WebSocketConnectionClosedException


class SlackMode(object):
    NORMAL = 0
    SCRIPTED = 1
    INTERACTIVE = 2


class Slack(object):
    def __init__(self, config):
        self.config = config
        self.api_key = config.get('secrets/SLACK_API_KEY')
        self.client = SlackClient(self.api_key)
        self.logger = getLogger(__name__)

        self.authed_user = ''
        self.authed_user_id = ''
        self.authed_team = ''
        self.authed_team_id = ''
        self.authed_team_url = ''

        self.mode = SlackMode.NORMAL

    def connect(self):
        # Try to connect to Slack
        test_result = self.client.api_call('auth.test', token=self.api_key)
        if not test_result['ok']:
            self.logger.error('Could not connect to Slack! ({})'.format(test_result['error']))
            return False

        if not self.client.rtm_connect():
            self.logger.error('Could not connect to RTM API!')
            return False

        self.authed_user = test_result['user']
        self.authed_user_id = test_result['user_id']
        self.authed_team = test_result['team']
        self.authed_team_id = test_result['team_id']
        self.authed_team_url = test_result['url']
        return True

    def send_message(self, channel, text, **kwargs):
        return self.client.api_call('chat.postMessage',
                                    channel=channel,
                                    text=text,
                                    as_user=not self.config['debug_mode'],
                                    **kwargs)

    def get_events(self):
        try:
            return self.client.rtm_read()

        except WebSocketConnectionClosedException:
            self.logger.error('WebSocket connection for RTM API was closed!')
            if self.client.rtm_connect():
                return self.get_events()

            self.logger.critical('Could not reconnect!')

    def is_own_event(self, event):
        if 'user' in event:
            if event['user'] in (self.authed_user, self.authed_user_id):
                return True

        return False


class PseudoSlackScripted(Slack):
    def __init__(self, config, script):
        self.config = config
        self.logger = getLogger(__name__)

        self.authed_user = 'Scripted Test User'
        self.authed_user_id = 'U00SCRIPT'
        self.authed_team = 'Scripted Test Team'
        self.authed_team_id = 'T00KIDDIE'
        self.authed_team_url = 'https://scripted-bot-testing.slack.com'

        self.script = script
        self.mode = SlackMode.SCRIPTED

    def connect(self):
        return True

    def send_message(self, channel, text, **kwargs):
        print(text)

    def get_events(self):
        with open(self.script) as f:
            for line in f:
                yield self.mock_event(line)

    def mock_event(self, text):
        return {'type': 'message', 'channel': 'C494WSTUL', 'user': self.authed_user_id,
                'text': text}


class PseudoSlackInteractive(Slack):
    def __init__(self, config):
        self.config = config
        self.logger = getLogger(__name__)

        self.authed_user = 'Interactive Test User'
        self.authed_user_id = 'UINTERACT'
        self.authed_team = 'Interactive Test Team'
        self.authed_team_id = 'TINTERACT'
        self.authed_team_url = 'https://interactive-bot-testing.slack.com'

        self.mode = SlackMode.INTERACTIVE

    def connect(self):
        return True

    def send_message(self, channel, text, **kwargs):
        print(text)

    def get_events(self):
        text = input("> ")
        return [self.mock_event(text)]

    def mock_event(self, text):
        return {'type': 'message', 'channel': 'C494WSTUL', 'user': self.authed_user_id,
                'text': text}
