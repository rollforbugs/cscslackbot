from __future__ import unicode_literals

from logging import getLogger

import tweepy

import cscslackbot.slack as slack
from cscslackbot.config import get_config
from cscslackbot.plugins import Plugin
from . import twitter


config = get_config('plugins.twitter')
logger = getLogger(__name__)

# Configure twitter api
using_twitter = True
try:
    consumer_key = config['consumer_key']
    consumer_secret = config['consumer_secret']
    access_token = config['access_token']
    access_secret = config['access_secret']

    if "" not in {consumer_key, consumer_secret, access_token, access_secret}:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        twitter_api = tweepy.API(auth)
    else:
        using_twitter = False

except AttributeError:
    logger.error('Update secrets for Twitter API')
    using_twitter = False


class TwitterPlugin(Plugin):
    name = 'twitter'
    help_text = 'Displays content of posted Twitter links'

    def process_event(self, event):
        # Validate event
        if event['type'] != 'message':
            return
        if 'text' not in event:
            return

        # Get the message
        message = event['text'].strip()

        # Extract twitter
        if using_twitter:
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
