from __future__ import unicode_literals
from slackclient import SlackClient
import time
import secrets

sc = SlackClient(secrets.SLACK_API_KEY)
channels = sc.api_call('channels.list', exclude_archived=1)
print(channels)

if sc.rtm_connect():
    while True:
        events = sc.rtm_read()
        for event in events:
            print(time.strftime("%Y-%m-%d %H:%M:%S  ", time.gmtime()) + str(event))
