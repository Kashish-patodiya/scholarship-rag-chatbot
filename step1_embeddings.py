from sentence_transformers import SentenceTransformer, util

# 1. Model load karo (ye text ko numbers mein badalta hai)
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Hamare "documents"
sentences = [
    "Scholarship for students whose family income is below 8 lakh",
    "Financial aid for poor college students",
    "How to bake a chocolate cake",
    "Last date to apply for the scholarship is 31 October",
    "Deadline for scholarship application",
]

# 3. Har sentence ko numbers mein badlo
embeddings = model.encode(sentences)
print("Shape:", embeddings.shape)

# 4. Sentences ki aapas mein similarity
scores = util.cos_sim(embeddings, embeddings)
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        print(f"{scores[i][j]:.2f} | {sentences[i]}  <->  {sentences[j]}")

# 5. Sawaal poochho
query = "money help for poor students"
query_embedding = model.encode(query)
results = util.cos_sim(query_embedding, embeddings)[0]

print("\nQuery:", query)
ranked = sorted(zip(results.tolist(), sentences), reverse=True)
for score, sentence in ranked:
    print(f"{score:.2f} | {sentence}")