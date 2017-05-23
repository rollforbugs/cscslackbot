from __future__ import unicode_literals

import re


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
    if len(match) == 0:
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
