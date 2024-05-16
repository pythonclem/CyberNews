import spacy

nlp = spacy.load("en_core_web_md")

# Sample headlines
headlines = [
    "Apple announces new iPhone model",
    "Google releases latest Android update",
    "Microsoft acquires new AI startup",
    "New iPhone model has groundbreaking features"
]

# Process headlines with spaCy
docs = [nlp(headline) for headline in headlines]

# Extract entities and calculate similarities
for doc in docs:
    print(f"Headline: {doc.text}")
    print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])
    print("Similarities:")
    for other_doc in docs:
        if doc != other_doc:
            similarity = doc.similarity(other_doc)
            print(f" - Similarity to '{other_doc.text}': {similarity:.2f}")
    print("\n")