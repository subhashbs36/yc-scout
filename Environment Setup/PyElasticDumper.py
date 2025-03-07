import os
import json
import argparse
from elasticsearch import Elasticsearch, helpers


# **Constants**
DEST_FILE = "company_data.json"
ES_INDEX_NAME = "y_combinator_companies"
ES_HOST = "http://localhost:9200"


# **Step 1: Convert .jl File to JSON**
def convert_jl_to_json(source, destination):
    """Reads a .jl file and converts it into a structured JSON file."""
    with open(source, "r", encoding="utf-8") as f:  # ✅ Specify encoding
        data = [json.loads(line) for line in f]

    with open(destination, "w", encoding="utf-8") as f:  # ✅ Write with UTF-8
        json.dump(data, f, indent=4)

    print(f"✅ Data converted from {source} to {destination}")
    return data

# **Step 2: Prepare Data for Elasticsearch**
def prepare_data(data):
    """Extracts text and metadata from JSON data for indexing in Elasticsearch."""
    documents = []

    for obj in data:
        text_data = f"{obj['company_name']} {obj['short_description']} {obj['long_description']}"
        metadata = {
            "company_name": obj["company_name"],
            "description": obj["batch"],
            "status": obj["status"],
            "tags": obj["tags"],
            "location": obj["location"],
            "country": obj["country"],
            "year_founded": obj["year_founded"],
            "num_founders": obj["num_founders"],
            "founders_names": obj["founders_names"],
            "team_size": obj["team_size"],
            "website": obj["website"],
            "cb_url": obj["cb_url"],
            "linkedin_url": obj["linkedin_url"],
            'ycombinator': obj["company_url"]
        }
        documents.append({"text": text_data, "metadata": metadata})

    return documents


# **Step 3: Create Elasticsearch Index**
def create_es_index(es, index_name):
    """Creates an Elasticsearch index with proper mapping if it does not already exist."""
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
                        "status": {"type": "text"},
                        "ycombinator": {"type": "keyword"}
                    }
                },
            }
        }
    }

    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=mapping)
        print(f"✅ Index '{index_name}' created successfully.")
    else:
        print(f"⚠️ Index '{index_name}' already exists.")


# **Step 4: Index Documents in Elasticsearch**
def index_documents_in_es(es, index_name, documents):
    """Indexes a list of documents into Elasticsearch."""
    actions = [
        {
            "_index": index_name,
            "_id": doc_id,
            "_source": doc,
        }
        for doc_id, doc in enumerate(documents)
    ]

    helpers.bulk(es, actions)
    print(f"✅ Indexed {len(documents)} documents in Elasticsearch.")


# **Main Execution**
if __name__ == "__main__":
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Prevent duplicate library errors

    # **Argument Parser for Command-Line Input**
    parser = argparse.ArgumentParser(description="Process a .jl file and index it in Elasticsearch.")
    parser.add_argument("source_file", type=str, nargs="?", default="output.jl",
                        help="Path to the .jl file (default: output.jl)")

    args = parser.parse_args()
    SOURCE_FILE = args.source_file

    print("\n📌 Step 1: Converting .jl to JSON")
    data = convert_jl_to_json(SOURCE_FILE, DEST_FILE)

    print("\n📌 Step 2: Preparing data for Elasticsearch")
    documents = prepare_data(data)
    print(f"✅ Prepared {len(documents)} records for indexing.")

    print("\n📌 Step 3: Connecting to Elasticsearch")
    es = Elasticsearch(ES_HOST)


    if es.ping():
        print("✅ Connected to Elasticsearch.")

        print("\n📌 Step 4: Creating Elasticsearch Index")
        create_es_index(es, ES_INDEX_NAME)

        print("\n📌 Step 5: Indexing Data in Elasticsearch")
        index_documents_in_es(es, ES_INDEX_NAME, documents)

    else:
        print("❌ Could not connect to Elasticsearch. Ensure it is running.")
