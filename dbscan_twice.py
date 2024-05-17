import csv
from datetime import datetime, timedelta
from dateutil import parser
import spacy
from sentence_transformers import SentenceTransformer
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

def initial_clustering(headlines, model_name='all-MiniLM-L6-v2', eps=0.5, min_samples=2):
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

def extract_entities(headlines):
    nlp = spacy.load("en_core_web_trf")
    docs = [nlp(headline) for headline in headlines]
    entities_list = []

    for doc in docs:
        entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT']]
        entities_list.append(entities)
    
    return entities_list

def refine_clusters(clusters, threshold=7):
    refined_clusters = {}
    model = SentenceTransformer('all-MiniLM-L6-v2')

    for cluster_id, headlines in clusters.items():
        if len(headlines) < threshold:
            refined_clusters[cluster_id] = headlines
        else:
            print(f"Refining cluster {cluster_id} with {len(headlines)} headlines")
            # Extract entities and generate new embeddings
            entities = extract_entities(headlines)
            enriched_headlines = [f"{headline} {' '.join(entity_list * 10)}" for headline, entity_list in zip(headlines, entities)]
            for enriched_head in enriched_headlines:
                print(enriched_head)
            embeddings = model.encode(enriched_headlines, convert_to_tensor=True)

            # Perform DBSCAN clustering again within the large cluster
            sub_clustering = DBSCAN(eps=0.5, min_samples=2, metric='cosine').fit(embeddings)
            sub_cluster_labels = sub_clustering.labels_

            # Organize headlines by new sub-clusters
            sub_clusters = {}
            for idx, label in enumerate(sub_cluster_labels):
                if label not in sub_clusters:
                    sub_clusters[label] = []
                sub_clusters[label].append(headlines[idx])
            
            # Add the refined sub-clusters to the final result
            for sub_cluster_id, sub_headlines in sub_clusters.items():
                refined_clusters[f"{cluster_id}-{sub_cluster_id}"] = sub_headlines

    return refined_clusters

def news_aggregator(csv_file):
    headlines = get_headlines_past_week(csv_file)
    initial_clusters = initial_clustering(headlines)
    refined_clusters = refine_clusters(initial_clusters)

    # for cluster_id, related_headlines in refined_clusters.items():
    #     print(f"Cluster {cluster_id}:")
    #     for headline in related_headlines:
    #         print(f"  - {headline}")
    #     print()

if __name__ == "__main__":
    news_aggregator("headlines.csv")