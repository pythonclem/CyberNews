from nlp_processing import get_headlines_past_week, cluster_headlines
from rssreader import rss_reader

def news_aggrgator():
    rss_reader()
    headlines = get_headlines_past_week("headlines.csv")
    clusters = cluster_headlines(headlines)

    for cluster, related_headlines in clusters.items():
        if cluster != -1:  # -1 is the noise label in DBSCAN
            print(f"Cluster {cluster}:")
            for headline in related_headlines:
                print(f"  - {headline}")




news_aggrgator()