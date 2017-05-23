from __future__ import unicode_literals

from logging import getLogger

import tweepy

from cscslackbot.plugins import Plugin
from . import twitter


logger = getLogger(__name__)


class TwitterPlugin(Plugin):
    name = 'twitter'
    help_text = 'Displays content of posted Twitter links'

    def __init__(self, config, slack, bot):
        super(self.__class__, self).__init__(config, slack, bot)

        # Configure twitter api
        self.using_twitter = True
        try:
            consumer_key = self.config['secrets']['twitter_consumer_key']
            consumer_secret = self.config['secrets']['twitter_consumer_secret']
            access_token = self.config['secrets']['twitter_access_token']
            access_secret = self.config['secrets']['twitter_access_secret']

            if "" not in {consumer_key, consumer_secret, access_token, access_secret}:
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                auth.set_access_token(access_token, access_secret)
                self.twitter_api = tweepy.API(auth)
            else:
                self.using_twitter = False

        except AttributeError:
            logger.error('Update secrets for Twitter API')
            self.using_twitter = False

    def process_event(self, event):
        # Validate event
        if event['type'] != 'message':
            return
        if 'text' not in event:
            return

        # Get the message
        message = event['text'].strip()

        # Extract twitter
        if self.using_twitter:
            twitter_url = twitter.find_twitter_url(message)
            if twitter_url:
                status_id = twitter.parse_status_url(twitter_url)
                try:
                    tweet = self.twitter_api.get_status(status_id)
                    tweet_ = tweet.text.strip().replace("\n", "\n> ")
                    msg_out = "".join(
                        ["> ", tweet_, "\n", tweet.author.screen_name, " - ",
                         str(tweet.created_at.year)])

                    self.slack.send_message(event['channel'], msg_out)
                except tweepy.error.TweepError:
                    pass
