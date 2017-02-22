from __future__ import unicode_literals
from slackclient import SlackClient
import time
import config
import secrets
from utils.logging import log_info

sc = SlackClient(secrets.SLACK_API_KEY)
channels = sc.api_call('channels.list', exclude_archived=1)


def parse_command(event: dict):
    # Validate event
    if 'type' not in event:
        return
    if event['type'] != 'message':
        return
    if 'text' not in event:
        return

    # Get the message
    message = event['text'].strip()
    # Check if the message is for us
    if not message.startswith(config.prefix):
        return

    # Perform the appropriate action
    command = message[len(config.prefix):].strip()
    action = command.split()[0]
    if action == 'help':
        sc.api_call('chat.postMessage',
                    channel=event['channel'],
                    text='Right now, I support the following commands:\n`!help`\n`!hello`\n'
                         + 'This help is also literally just a string right now.\n'
                         + 'A more robust architecture would be nice.')
    if action == 'hello':
        greeting = 'Hey! :partyparrot:'
        if 'user' in event:
            user = event['user']
            greeting = 'Hey <@{}>! :partyparrot:'.format(user)
        sc.api_call('chat.postMessage',
                    channel=event['channel'],
                    text=greeting)

     if action == 'slap':
         if 'user' in event:
             user = event['user']
             slapped = '/me slaps <@{}>!   '.format(user)
         sc.api_call('chat.postMessage',
                     channel=event['channel'],
                     text=slaped)

def main():
    if sc.rtm_connect():
        while True:
            events = sc.rtm_read()
            for event in events:
                parse_command(event)
                log_info(str(event))


if __name__ == '__main__':
    main()
