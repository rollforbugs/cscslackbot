from __future__ import print_function
from __future__ import unicode_literals

import sys
import tweepy
from slackclient import SlackClient

import config
import secrets
import twitter
from cscslackbot.utils.logging import log_info

# Configure slack api
sc = SlackClient(secrets.SLACK_API_KEY)
channels = sc.api_call('channels.list', exclude_archived=1)
authed_user = ''
authed_user_id = ''

# Configure twitter api
using_twiiter = True
try:
    consumer_key = secrets.twitter_consumer_key
    consumer_secret = secrets.twitter_consumer_secret
    access_token = secrets.twitter_access_token
    access_secret = secrets.twitter_access_secret

    if "" not in { consumer_key,consumer_secret,access_token,access_secret}:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        twitter_api = tweepy.API(auth)
    else:
        using_twiiter = False

except AttributeError:
    print("Update secrets for twitter api", file=sys.stderr)
    using_twiiter = False

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

    # Extract twitter
    if using_twiiter:
        twitter_url = twitter.find_twitter_url(message)
        if twitter_url:
            status_id = twitter.parse_status_url(twitter_url)
            try:
                tweet = twitter_api.get_status(status_id)
                msg_out = "".join(["> ", tweet.text,"\n", tweet.display_name, " - ", tweet.created_at[:4]])
                sc.api_call('chat.postMessage',
                            channel=event['channel'],
                            text=msg_out)
            except tweepy.error.TweepError:
                pass

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
        slapped = ':hand: :eight_pointed_black_star: {}!'.format(name)
        sc.api_call('chat.postMessage',
                    channel=event['channel'],
                    text=slapped)

    if action == 'identify':
        sc.api_call('chat.postMessage',
                    channel=event['channel'],
                    text='{}\'s bot, reporting in'.format(authed_user))


def run():
    if sc.rtm_connect():
        try:
            test_result = sc.api_call('auth.test', token=secrets.SLACK_API_KEY)
            authed_user = test_result['user']
            authed_user_id = test_result['user_id']

            if config.debug_mode:
                sc.api_call('chat.postMessage', channel='#bottesting', text='{} is now testing.'.format(authed_user))

            while True:
                events = sc.rtm_read()
                for event in events:
                    log_info(str(event))

                    if config.debug_mode:
                        # Whitelist #bottesting
                        if 'channel' not in event:
                            continue
                        if event['channel'] not in ['C494WSTUL', '#bottesting']:
                            continue
                        # Only respond to the developer when in debug mode
                        if 'user' not in event or event['user'] != authed_user_id:
                            continue

                    parse_command(event)
        except KeyboardInterrupt:
            if config.debug_mode:
                sc.api_call('chat.postMessage', channel='#bottesting', text='I\'m dead! (SIGINT)')


if __name__ == '__main__':
    run()
