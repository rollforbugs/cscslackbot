from __future__ import unicode_literals

import tweepy

from cscslackbot.plugins import Plugin
from . import twitter


plugin = Plugin(__name__, 'Generate previews for tweets')

twitter_api = None


@plugin.on_load()
def on_load():
    # Configure twitter api
    try:
        consumer_key = plugin.config['consumer_key']
        consumer_secret = plugin.config['consumer_secret']
        access_token = plugin.config['access_token']
        access_secret = plugin.config['access_secret']

        if consumer_key and consumer_secret and access_token and access_secret:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_secret)
            global twitter_api
            twitter_api = tweepy.API(auth)

    except KeyError:
        plugin.logger.error('Update secrets for Twitter API')


@plugin.on('message')
def generate_tweet_preview(event):
    if not twitter_api:
        return

    # Validate event
    if 'text' not in event:
        return

    # Get the message
    message = event['text'].strip()

    # Extract twitter
    twitter_url = twitter.find_twitter_url(message)
    if twitter_url:
        status_id = twitter.parse_status_url(twitter_url)
        try:
            tweet = twitter_api.get_status(status_id, tweet_mode='extended')
            tweet_ = tweet.full_text.strip().replace("\n", "\n> ")
            msg_out = "".join(
                ["> ", tweet_, "\n", tweet.author.screen_name, " - ",
                 str(tweet.created_at.year)])

            plugin.slack.send_message(event['channel'], msg_out)
        except tweepy.error.TweepError:
            pass
