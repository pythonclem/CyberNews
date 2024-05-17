import spacy
from nlp_processing import get_headlines_past_week

def extract_entities_and_score():

    nlp = spacy.load("en_core_web_md")

    # Sample headlines
    headlines = ["Microsoft Warns of Active Zero-Day Exploitation, Patches 60 Windows Vulnerabilities Microsoft Microsoft Microsoft Microsoft Microsoft Microsoft Microsoft Microsoft Microsoft Microsoft",
                "Microsoft Fixes Three Zero-Days in May Patch Tuesday Microsoft Microsoft Microsoft Microsoft Microsoft Microsoft Microsoft Microsoft Microsoft Microsoft",
                "Microsoft Windows DWM Zero-Day Poised for Mass Exploit Microsoft Windows Microsoft Windows Microsoft Windows Microsoft Windows Microsoft Windows Microsoft Windows Microsoft Windows Microsoft Windows Microsoft Windows Microsoft Windows",
                "Dangerous Google Chrome Zero-Day Allows Sandbox Escape Google Chrome Google Chrome Google Chrome Google Chrome Google Chrome Google Chrome Google Chrome Google Chrome Google Chrome Google Chrome",
                "Google Patches Yet Another Actively Exploited Chrome Zero-Day Vulnerability Google Google Google Google Google Google Google Google Google Google",
                "Third Chrome Zero-Day Patched by Google Within One Week Google Google Google Google Google Google Google Google Google Google",
                "Patch Now: Another Google Zero-Day Under Exploit in the Wild Google Google Google Google Google Google Google Google Google Google"]

    # Process headlines with spaCy
    docs = [nlp(headline) for headline in headlines]

    # Extract entities and calculate similarities
    for doc in docs:
        print(f"Headline: {doc.text}")
        print("Similarities:")
        for other_doc in docs:
            if doc != other_doc:
                similarity = doc.similarity(other_doc)
                print(f" - Similarity to '{other_doc.text}': {similarity:.2f}")
        print("\n")


extract_entities_and_score()
