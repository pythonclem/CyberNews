import spacy

# Load the medium English model
nlp = spacy.load("en_core_web_md")

# Define the two strings
string1 = "The quick brown fox jumps over the lazy dog."
string2 = "A fast brown fox leaps over a lazy dog."

# Process the strings with spaCy
doc1 = nlp(string1)
doc2 = nlp(string2)

# Calculate similarity
similarity = doc1.similarity(doc2)

# Print the similarity score
print(f"Similarity: {similarity}")