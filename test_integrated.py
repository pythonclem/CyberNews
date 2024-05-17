import csv
from datetime import datetime, timedelta
from dateutil import parser
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import feedparser

def rss_reader():
    
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


def get_headlines_past_week(csv_file):
    one_week_ago = datetime.now() - timedelta(days=7)
    
    headlines_past_week = []

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                channel_title, title, pub_date = row
                parsed_date = parser.parse(pub_date, dayfirst=True)
                if parsed_date >= one_week_ago:
                    headlines_past_week.append(title)
    
    return headlines_past_week

def extract_entities(headlines):
    nlp = spacy.load("en_core_web_trf")
    docs = [nlp(headline) for headline in headlines]
    entities_list = []

    for doc in docs:
        entities = " ".join([ent.text for ent in doc.ents])
        entities_list.append(entities)
    
    return entities_list

def cluster_headlines(headlines, entities, model_name='all-MiniLM-L6-v2', eps=0.5, min_samples=2):
    model = SentenceTransformer(model_name)
    
    # Create enhanced representations
    enhanced_headlines = [f"{headline} {entity}" for headline, entity in zip(headlines, entities)]
    
    # Encode enhanced headlines to get embeddings
    embeddings = model.encode(enhanced_headlines, convert_to_tensor=True)

    # Use DBSCAN clustering to find related headlines
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine').fit(embeddings)

    # Organize headlines by clusters
    cluster_labels = clustering.labels_
    clusters = {}
    for idx, label in enumerate(cluster_labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(headlines[idx])

    return clusters

def news_aggregator():
    rss_reader()
    headlines = get_headlines_past_week("headlines.csv")
    entities = extract_entities(headlines)
    clusters = cluster_headlines(headlines, entities)

    for cluster, related_headlines in clusters.items():
        if cluster != -1:  # -1 is the noise label in DBSCAN
            print(f"Cluster {cluster}:")
            for headline in related_headlines:
                print(f"  - {headline}")

if __name__ == "__main__":
    news_aggregator()