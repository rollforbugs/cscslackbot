from __future__ import unicode_literals

import re

import tweepy

import secrets


#

def find_twitter_url(msg):
    """
    Extracts a twitter url from text.
    Args:
        msg (str):

    Returns:
        (str): url
        (NoneType): No twitter url was found.
    """
    link_rx = r'(?:http[s]?://)?twitter\.com/[A-z0-9]+/status/\d+'

    match = re.findall(link_rx, msg)
    if len(match) < 0:
        return None
    return match[0]


def parse_status_url(url):
    """Returns the status id of a tweet from the url.
    Returns None for a
    Args:
        url (str): url of a tweet

    Returns:
        int: status id
        NoneType: Failure
    """
    # url = "https://twitter.com/SwiftOnSecurity/status/834639723318611969"
    parts = url.split("/")
    if parts[0].startswith("http"):
        parts = parts[2:]

    if parts[2] != "status":
        return None

    try:
        sid = int(parts[3])
        return sid
    except ValueError:
        return None


# test

consumer_key = secrets.twitter_consumer_key
consumer_secret = secrets.twitter_consumer_secret

access_token = secrets.twitter_access_token
access_secret = secrets.twitter_access_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
twitter_api = tweepy.API(auth)

url = "https://twitter.com/SwiftOnSecurity/status/834639723318611969"

status = parse_status_url(url)
try:
    tweet = twitter_api.get_status(status)
    print(tweet.created_at)
except tweepy.error.TweepError:
    print "passed"
