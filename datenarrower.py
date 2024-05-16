import feedparser
from dateutil import parser

# URL of the RSS feed
rss_urls = ["https://feeds.feedburner.com/TheHackersNews" , "https://therecord.media/feed", "https://feeds.feedburner.com/securityweek", "https://www.infosecurity-magazine.com/rss/news/", "https://www.darkreading.com/rss.xml", "https://rss.app/feeds/w3xYtTC2lyhvYOi9.xml"]

for rssfeed in rss_urls:

    feed = feedparser.parse(rssfeed)
    if "infosecurity-magazine" in rssfeed:
        channel_title = "infosecurity mag"
    else:
        channel_title = feed.feed.title

# Iterate over each entry/item in the feed
    for entry in feed.entries:

        pub_date = entry.published
        parsed_date = parser.parse(pub_date)
        formatted_date = parsed_date.strftime('%d/%m/%Y')
        print(channel_title)
        print(formatted_date)
