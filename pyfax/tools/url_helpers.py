"""Helpers for loading data from URLs."""

import json

import feedparser
import requests


def load_rss(url):
    """Load data from an RSS feed.

    Args:
        url: The URL of the feed.
    """
    return feedparser.parse(url)


def load_json(url, headers={}, cookies={}):
    """Load data from a JSON feed.

    Args:
        url: The URL of the feed.
        headers: Headers to send with the request.
        cookies: Cookies to send with the request.
    """
    feed = load(url, headers, cookies)
    return json.loads(feed)


def load_csv(url, headers={}, cookies={}):
    """Load data from a CSV feed.

    Args:
        url: The URL of the feed.
        headers: Headers to send with the request.
        cookies: Cookies to send with the request.
    """
    feed = load(url, headers, cookies)
    return [i.split(",") for i in feed.split("\n")]


def load(url, headers={}, cookies={}):
    """Load data from a URL.

    Args:
        url: The URL.
        headers: Headers to send with the request.
        cookies: Cookies to send with the request.
    """
    headers["User-Agent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/50.0.2661.102 Safari/537.36")
    out = requests.get(url, headers=headers, cookies=cookies).text
    try:
        return out.decode('utf-8')
    except:  # noqa: E722
        return out
