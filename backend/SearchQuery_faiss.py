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

# ✅ FAISS Search Function
def search_faiss(query, index, faiss_data_store, top_k=10):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = [faiss_data_store[str(idx)] for idx in indices[0] if idx != -1]
    print(len(results))
    return results

# ✅ Main Execution
if __name__ == "__main__":
    index, faiss_data_store = load_faiss_index()

    query = input("\nEnter your search query: ")
    results = search_faiss(query, index, faiss_data_store)

    print(json.dumps(results, indent=4, ensure_ascii=False))
