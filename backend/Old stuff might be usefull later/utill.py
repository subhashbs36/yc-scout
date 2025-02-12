from groq import Groq
import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from transformers import AutoTokenizer, AutoModel
import chromadb
from chromadb.config import DEFAULT_DATABASE,DEFAULT_TENANT,Settings
import torch

#Initialize #################################################################
load_dotenv()

# Load the model and tokenizer once during startup
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# establish connection to the chromaDB
client_DB = chromadb.PersistentClient(
    path = 'my_local_data',
    database=DEFAULT_DATABASE,
    settings=Settings(),
    tenant= DEFAULT_TENANT
)

#create a collection for data and maintain the name imp cant duplicate 
collection = client_DB.get_or_create_collection("local")

#chatbot clint
client_llm = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


# Initialize Elasticsearch client
es = Elasticsearch(hosts=["http://localhost:9200"])
#################################################################################

#Phase 1 

# Elastic Search Function
def search_documents(index_name, query, size=10):
    search_query = {
        "query": {
            "query_string": {
                "query": query  # General query for full-text search across all fields
            }
        }
    }

    response = es.search(index=index_name, body=search_query, size=size)

    data = []
    metadata = []
    # Print search results
    if response['hits']['hits']:
        print(f"\nFound {len(response['hits']['hits'])} results for '{query}':\n")
        for hit in response['hits']['hits']:
            print(f"ID: {hit['_id']} | Score: {hit['_score']}")
            val = hit['_source']
            del val['image_urls']
            print(f"Source: {val}\n")
            data.append(val)
        rag_results = val['documents'][0]
        rag_meta = val['metadatas'][0]
        print(f'{rag_results} \n')
        print(f'{rag_meta} \n')
        return rag_results, rag_meta
    else:
        print(f"No results found for '{query}'.")
        return None

# Embedding function
def embedd_input(text):
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)  # Mean pooling
    return embeddings.squeeze().tolist()

#ChromaDB Call Function
def chroma_call(prompt):
    # Query the database (assuming 'collection' is defined elsewhere)
    result = collection.query(
        query_texts=prompt,
        n_results=4,
    )
    rag_results = result['documents'][0]
    rag_meta = result['metadatas'][0]
    print(f'{rag_results} \n')
    print(f'{rag_meta} \n')
    return rag_results, rag_meta

# Groq Call Function
def groq_call(prompt, model):
    output = client_llm.chat.completions.create(messages=prompt, model=model)
    return output.choices[0].message.content