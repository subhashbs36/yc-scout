import os
import json
import faiss
import numpy as np
import torch
from elasticsearch import Elasticsearch, helpers
from transformers import AutoTokenizer, AutoModel

# Set environment variable to avoid duplicate library errors
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# **Load Data from JSON**
def load_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

# **Prepare Data (Text + Metadata)**
def prepare_data(data):
    texts, metadatas = [], {}
    for i, item in enumerate(data):
        text = item.get("text", "No description available")
        metadata = item.get("metadata", {})

        texts.append(text)
        metadatas[str(i)] = {  # Store metadata using index as key
            'company_name': metadata.get('company_name', ''),
            'description': metadata.get('description', []),
            'tags': ', '.join(metadata.get('tags', [])),
            'location': metadata.get('location', ''),
            'country': metadata.get('country', ''),
            'year_founded': metadata.get('year_founded', 0),
            'num_founders': metadata.get('num_founders', 0),
            'founders_names': ', '.join(metadata.get('founders_names', [])),
            'team_size': metadata.get('team_size', 0),
            'website': metadata.get('website', ''),
            'linkedin_url': metadata.get('linkedin_url', ''),
            'status': metadata.get('status', '')
        }
    return texts, metadatas

# **Generate Text Embeddings using BERT**
def encode_texts(texts, tokenizer, model, batch_size=32, device="cpu"):
    embeddings = []
    model.to(device)
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        encoded_inputs = tokenizer(
            batch,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=512
        ).to(device)
        with torch.no_grad():
            outputs = model(**encoded_inputs)
        batch_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
        embeddings.append(batch_embeddings)
    return np.vstack(embeddings)

# **Save FAISS Index**
def save_faiss_index(index, file_path):
    faiss.write_index(index, file_path)

# **Load FAISS Index**
def load_faiss_index(file_path):
    return faiss.read_index(file_path)

# **Save Metadata Separately**
def save_metadata(metadata, file_path):
    with open(file_path, "w") as file:
        json.dump(metadata, file)

# **Load Metadata**
def load_metadata(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# **Create Elasticsearch Index with Proper Mapping**
def create_es_index(es, index_name):
    mapping = {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "metadata": {
                    "properties": {
                        "company_name": {"type": "text"},
                        "description": {"type": "text"},
                        "tags": {"type": "text"},
                        "location": {"type": "text"},
                        "country": {"type": "text"},
                        "year_founded": {"type": "integer"},
                        "num_founders": {"type": "integer"},
                        "founders_names": {"type": "text"},
                        "team_size": {"type": "integer"},
                        "website": {"type": "keyword"},
                        "linkedin_url": {"type": "keyword"},
                        "status": {"type": "text"}
                    }
                }
            }
        }
    }
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mapping)
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Index '{index_name}' already exists.")

# **Index Documents in Elasticsearch**
def index_documents_in_es(es, index_name, documents):
    actions = [
        {
            "_index": index_name,
            "_id": doc_id,
            "_source": doc
        }
        for doc_id, doc in enumerate(documents)
    ]
    helpers.bulk(es, actions)
    print(f"Indexed {len(documents)} documents in Elasticsearch.")

# **Main Execution**
if __name__ == "__main__":
    print("Step 1: Loading and preprocessing data")
    file_path = "data/company_data_cleaned_final.json"
    data = load_data(file_path)
    print(f"Loaded {len(data)} records from {file_path}.")

    texts, metadatas = prepare_data(data)
    print(f"Prepared {len(texts)} texts with metadata.")

    # print("\nStep 2: Loading BERT tokenizer and model")
    # model_name = "bert-base-uncased"
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = AutoModel.from_pretrained(model_name)
    # print("BERT tokenizer and model loaded.")

    # print("\nStep 3: Generating embeddings")
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    # print(f"Using device: {device}")
    # embeddings = encode_texts(texts, tokenizer, model, device=device)
    # embeddings = embeddings.astype(np.float32)
    # print(f"Generated embeddings shape: {embeddings.shape}")

    # print("\nStep 4: Initializing and populating FAISS index")
    # dimension = embeddings.shape[1]
    # index = faiss.IndexFlatL2(dimension)
    # index.add(embeddings)
    # print(f"Number of vectors in the index: {index.ntotal}")

    # print("\nStep 5: Saving FAISS index and metadata")
    # save_faiss_index(index, "faiss_index.bin")
    # save_metadata(metadatas, "metadata.json")
    # print("FAISS index and metadata saved.")

    print("\nStep 6: Connecting to Elasticsearch")
    es = Elasticsearch("http://localhost:9200")  # Ensure ES is running locally
    index_name = "y_combinator_companies"

    if es.ping():
        print("Connected to Elasticsearch.")
        
        print("\nStep 7: Creating Elasticsearch index")
        create_es_index(es, index_name)

        print("\nStep 8: Indexing documents in Elasticsearch")
        es_documents = [{"text": texts[i], "metadata": metadatas[str(i)]} for i in range(len(texts))]
        index_documents_in_es(es, index_name, es_documents)
    else:
        print("Could not connect to Elasticsearch. Ensure it is running.")

    # print("\nStep 9: Processing query")
    # query = ["Automate your workflows with AI."]
    # print(f"Original query: {query}")
    # query_embeddings = encode_texts(query, tokenizer, model, device=device)
    # query_embeddings = query_embeddings.astype(np.float32)

    # print("\nStep 10: Searching FAISS index")
    # k = 5  # Number of nearest neighbors
    # distances, indices = index.search(query_embeddings, k)

    # print("\nTop matches from FAISS:")
    # for i, idx in enumerate(indices[0]):
    #     idx_str = str(idx)
    #     metadata = metadatas.get(idx_str, {})
    #     print(f"Match {i + 1}: {texts[idx]} (Distance: {distances[0][i]})")
    #     print(f"Metadata: {json.dumps(metadata, indent=2)}\n")
