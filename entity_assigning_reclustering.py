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

def extract_entities(headlines):
    nlp = spacy.load("en_core_web_md")
    docs = [nlp(headline) for headline in headlines]
    entities_list = []
    all_entities = set()

    for doc in docs:
        entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT']]
        entities_list.append(entities)
        all_entities.update(entities)
    
    return entities_list, all_entities


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


def cross_check_entities(headlines, entities_list, all_entities):
    updated_entities_list = []

    for headline, entities in zip(headlines, entities_list):
        updated_entities = set(entities)
        for entity in all_entities:
            if entity in headline and entity not in entities:
                updated_entities.add(entity)
        updated_entities_list.append(list(updated_entities))
    
    return updated_entities_list

def refine_clusters(clusters, threshold=7):
    refined_clusters = {}
    nlp = spacy.load("en_core_web_md")

    for cluster_id, headlines in clusters.items():
        if len(headlines) < threshold:
            refined_clusters[cluster_id] = headlines
        else:
            print(f"Refining cluster {cluster_id} with {len(headlines)} headlines")
            # Extract entities and generate new enriched headlines
            entities_list, all_entities = extract_entities(headlines)
            updated_entities_list = cross_check_entities(headlines, entities_list, all_entities)
            enriched_headlines = [f"{headline} {' '.join(entity_list * 10)}" for headline, entity_list in zip(headlines, updated_entities_list)]
            enriched_docs = [nlp(enriched_headline) for enriched_headline in enriched_headlines]

            # Perform similarity-based re-clustering
            sub_clusters = {}
            doc_clusters = {}  # To keep track of Doc objects for similarity comparison
            for i, doc in enumerate(enriched_docs):
                assigned = False
                for key in doc_clusters.keys():
                    if doc.similarity(doc_clusters[key][0]) > 0.8:
                        sub_clusters[key].append(i)  # store index
                        doc_clusters[key].append(doc)  # store Doc
                        assigned = True
                        break
                if not assigned:
                    new_key = len(sub_clusters)
                    sub_clusters[new_key] = [i]  # store index
                    doc_clusters[new_key] = [doc]  # store Doc

            # Convert sub_clusters back to original headlines
            for sub_cluster_id, indices in sub_clusters.items():
                refined_clusters[f"{cluster_id}-{sub_cluster_id}"] = [headlines[idx] for idx in indices]

    return refined_clusters


def news_aggregator(csv_file):
    headlines = get_headlines_past_week(csv_file)
    initial_clusters = initial_clustering(headlines)
    refined_clusters = refine_clusters(initial_clusters)

    for cluster_id, related_headlines in refined_clusters.items():
        print(f"Cluster {cluster_id}:")
        for headline in related_headlines:
            print(f"  - {headline}")
        print()

if __name__ == "__main__":
    news_aggregator("headlines.csv")