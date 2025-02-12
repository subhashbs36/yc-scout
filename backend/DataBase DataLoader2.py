import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os

DATA_FILE = "data/company_data_cleaned_final.json"
FAISS_INDEX_FILE = "faiss_index.bin"
FAISS_DATA_FILE = "faiss_data.json"

# Load Sentence Transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# ✅ Safe handling of None values
def preprocess_data(item):
    meta = item.get("metadata", {})
    combined_text = " ".join([
        str(item.get("text", "")),  
        str(meta.get("company_name", "")),  
        str(meta.get("description", "")),  
        str(meta.get("status", "")),  
        " ".join(map(str, meta.get("tags", []))),  
        str(meta.get("location", "")),  
        str(meta.get("country", "")),  
        str(meta.get("year_founded", "")),  
        " ".join(map(str, meta.get("founders_names", []))),  
        str(meta.get("team_size", "")),  
        str(meta.get("website", "")),  
        str(meta.get("linkedin_url", ""))  
    ])
    return combined_text.strip().lower()


def build_faiss_index(data):
    processed_texts = [preprocess_data(item) for item in data]
    full_json_data = {i: item for i, item in enumerate(data)}

    # Encode combined text as embeddings
    embeddings = model.encode(processed_texts, convert_to_numpy=True, show_progress_bar=True)

    # Create FAISS Index (HNSW for better performance)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIDMap(index)
    index.add_with_ids(embeddings, np.array(list(full_json_data.keys())))

    # ✅ Save FAISS Index & Data
    faiss.write_index(index, FAISS_INDEX_FILE)
    with open(FAISS_DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(full_json_data, file, ensure_ascii=False, indent=4)


    print("✅ FAISS index and data saved successfully!")

# ✅ Load FAISS Index and Data
def load_faiss_index():
    if not os.path.exists(FAISS_INDEX_FILE) or not os.path.exists(FAISS_DATA_FILE):
        print("⚠️ FAISS index or data not found. Rebuilding index...")
        data = load_data(DATA_FILE)
        build_faiss_index(data)
    
    index = faiss.read_index(FAISS_INDEX_FILE)
    with open(FAISS_DATA_FILE, "r", encoding="utf-8") as file:
        faiss_data_store = json.load(file)

    print("✅ FAISS index and data loaded successfully!")
    return index, faiss_data_store


# ✅ Hybrid Search: FAISS + Exact Match Boosting
def search_faiss(query, index, faiss_data_store, top_k=10):
    if index is None or faiss_data_store is None:
        print("⚠️ FAISS index is not loaded.")
        return []

    query = query.lower()  # Normalize query
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx != -1:
            results.append(faiss_data_store[str(idx)])  

    # ✅ Boost Exact Matches
    for item in faiss_data_store.values():
        meta = item.get("metadata", {})  # Ensure metadata is a dictionary
        metadata_fields = [
            str(meta.get("company_name", "")).lower(),
            " ".join(map(str, meta.get("tags", []))).lower(),
            " ".join(map(str, meta.get("founders_names", []))).lower(),
            str(meta.get("location", "")).lower()
        ]
        # if any(query in field for field in metadata_fields):
        #     results.insert(0, item)  # Prioritize exact matches

    return results[:top_k]

# ✅ Main Execution
if __name__ == "__main__":
    if not os.path.exists(FAISS_INDEX_FILE):
        print("🔄 FAISS index not found. Building new index...")
        data = load_data(DATA_FILE)
        build_faiss_index(data)

    index, faiss_data_store = load_faiss_index()

    while True:
        query = input("\nEnter your search query: ")
        results = search_faiss(query, index, faiss_data_store)
        print(json.dumps(results, indent=4, ensure_ascii=False))
