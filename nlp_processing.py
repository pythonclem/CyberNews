import csv
from dateutil import parser
from datetime import datetime, timedelta
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import DBSCAN

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

def cluster_headlines(headlines, model_name='all-MiniLM-L6-v2', eps=0.5, min_samples=2):
    # Load a pre-trained sentence transformer model
    model = SentenceTransformer(model_name)

    # Encode headlines to get embeddings
    embeddings = model.encode(headlines, convert_to_tensor=True)

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

