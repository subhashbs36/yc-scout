import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the pre-trained model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# File paths
FAISS_INDEX_FILE = "faiss_index.bin"
FAISS_DATA_FILE = "faiss_data.json"

# ✅ Load FAISS Index and Data
def load_faiss_index():
    index = faiss.read_index(FAISS_INDEX_FILE)
    with open(FAISS_DATA_FILE, "r", encoding="utf-8") as file:
        faiss_data_store = json.load(file)
    return index, faiss_data_store

# ✅ FAISS Search Function with Scores and Indices
def search_faiss(query, index, faiss_data_store, top_k=10):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    print(f"dists: {distances}")
    print(f"indices: {indices}")

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx != -1:  # Ensuring valid indices
            result = {
                "index": int(idx),
                "score": float(dist),
                "data": faiss_data_store.get(str(idx), {})  # Fetch from JSON
            }
            results.append(result)

    print(len(results))
    return results


# ✅ Main Execution
if __name__ == "__main__":
    index, faiss_data_store = load_faiss_index()

    query = input("\nEnter your search query: ")
    results = search_faiss(query, index, faiss_data_store)
    for result in results:
        print(json.dumps(result.get("data").get("metadata", "").get("ycombinator", ""), indent=4, ensure_ascii=False))
    # print(json.dumps(results, indent=4, ensure_ascii=False))
