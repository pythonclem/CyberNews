import feedparser
import csv
from dateutil import parser

rss_urls = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://therecord.media/feed",
    "https://feeds.feedburner.com/securityweek",
    "https://www.infosecurity-magazine.com/rss/news/",
    "https://www.darkreading.com/rss.xml",
    "https://rss.app/feeds/w3xYtTC2lyhvYOi9.xml"
]

existing_headlines = set()
try:
    with open('headlines.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                existing_headlines.add(row[1])

except FileNotFoundError:
    pass

with open('headlines.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    for rssfeed in rss_urls:
        feed = feedparser.parse(rssfeed)
        
        if "infosecurity-magazine" in rssfeed:
            channel_title = "infosecurity mag"
        else:
            channel_title = feed.feed.title

        for entry in feed.entries:
            title = entry.title
            
            if title not in existing_headlines:
                pub_date = entry.published
                parsed_date = parser.parse(pub_date)
                formatted_date = parsed_date.strftime('%d/%m/%Y')
                
                writer.writerow([channel_title, title, formatted_date])
                existing_headlines.add(title)
            
            else:
                print("Headline Exists")
