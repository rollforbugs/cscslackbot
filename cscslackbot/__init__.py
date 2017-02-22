from __future__ import unicode_literals
from slackclient import SlackClient
import config
import secrets
from cscslackbot.utils.logging import log_info

sc = SlackClient(secrets.SLACK_API_KEY)
channels = sc.api_call('channels.list', exclude_archived=1)
authed_user = sc.api_call('auth.test', token=secrets.SLACK_API_KEY)['user']


def parse_command(event):
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
                    text='Right now, I support the following commands:\n'
                         + '`!help`\n`!hello`\n`!slap`\n`!identify`\n'
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
        name = command.partition('slap')[2].strip()
        if name == '':
            return
        slapped = 'slaps {}!'.format(name)
        sc.api_call('chat.meMessage',
                    channel=event['channel'],
                    text=slapped)

    if action == 'identify':
        sc.api_call('chat.postMessage',
                    channel=event['channel'],
                    text='{}\'s bot, reporting in'.format(authed_user))


def run():
    if sc.rtm_connect():
        try:
            sc.api_call('chat.postMessage', channel='#bottesting', text='I\'m online!')
            while True:
                events = sc.rtm_read()
                for event in events:
                    # Whitelist #bottesting
                    if 'channel' not in event:
                        continue
                    if event['channel'] not in ['C494WSTUL', '#bottesting']:
                        continue

                    parse_command(event)
                    log_info(str(event))
        except KeyboardInterrupt:
            sc.api_call('chat.postMessage', channel='#bottesting', text='I\'m dead! (SIGINT)')
        except:
            sc.api_call('chat.postMessage', channel='#bottesting', text='I\'m dead! (exception)')


if __name__ == '__main__':
    run()
