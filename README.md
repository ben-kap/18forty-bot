# 18Forty Mastodon Bot
A Mastodon bot which pulls from the various public RSS feeds from [18Forty](https://18forty.org/) and posts to Mastodon whenever a new content is added to one of the RSS feeds.

The `toot.py` script must be manually run in order to check the RSS feed and post if a new article is found. This process can be automated using a cronjob or similar method.

The code should be able to be adapted fairly easily to other websites with a public RSS feed.
