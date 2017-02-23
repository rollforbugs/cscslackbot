from __future__ import print_function
from __future__ import unicode_literals

import sys
import tweepy

import config
import secrets
import twitter
import cscslackbot.plugins as plugins
import cscslackbot.slack as slack
from cscslackbot.utils.logging import log_info, log_error

# Configure twitter api
using_twiiter = True
try:
    consumer_key = secrets.twitter_consumer_key
    consumer_secret = secrets.twitter_consumer_secret
    access_token = secrets.twitter_access_token
    access_secret = secrets.twitter_access_secret

    if "" not in {consumer_key, consumer_secret, access_token, access_secret}:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        twitter_api = tweepy.API(auth)
    else:
        using_twiiter = False

except AttributeError:
    print("Update secrets for twitter api", file=sys.stderr)
    using_twiiter = False


def parse_command(event):
    plugins.plugins_process_event(event)
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
                tweet_ = tweet.text.strip().replace("\n", "\n> ")
                msg_out = "".join(
                    ["> ", tweet_, "\n", tweet.author.screen_name, " - ",
                     str(tweet.created_at.year)])

                slack.send_message(event['channel'], msg_out)
            except tweepy.error.TweepError:
                pass


def run():
    if not slack.connect():
        log_error('Cannot connect to Slack. Please verify your token in the config.')
        return

    plugins.load_plugins()

    if config.debug_mode:
        slack.client.api_call('chat.postMessage',
                              channel='#bottesting',
                              text='{} is now testing.'.format(slack.authed_user))

    try:
        while True:
            events = slack.get_event()
            for event in events:
                log_info(str(event))

                if config.debug_mode:
                    # Whitelist #bottesting
                    if 'channel' not in event:
                        continue
                    if event['channel'] not in ['C494WSTUL', '#bottesting']:
                        continue
                    # Only respond to the developer when in debug mode
                    if 'user' not in event or event['user'] != slack.authed_user_id:
                        continue

                parse_command(event)
    except KeyboardInterrupt:
        if config.debug_mode:
            slack.send_message('#bottesting', 'I\'m dead! (SIGINT)')


if __name__ == '__main__':
    run()
