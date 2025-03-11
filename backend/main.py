import time
import os
import json
import faiss
import torch
import numpy as np
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from groq import Groq
import json
import re

# Load environment variables
load_dotenv()

# **Initialization #################################################################

# Set environment variable to avoid duplicate library errors
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

groq_model = "llama-3.3-70b-versatile"

# **Load FAISS Index and Metadata**
DATA_FILE = "data/company_data_cleaned_final.json"
FAISS_INDEX_FILE = "faiss_index.bin"
FAISS_DATA_FILE = "faiss_data.json"

# **Load BERT model and tokenizer**
model_name = "bert-base-uncased"

#chatbot clint
client_llm = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# **Initialize Elasticsearch Client**
es = Elasticsearch(hosts=["http://localhost:9200"])

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:9200", "*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Load FAISS Index and Data
def load_faiss_index():
    if not os.path.exists(FAISS_INDEX_FILE) or not os.path.exists(FAISS_DATA_FILE):
        print("⚠️ FAISS index or data not found. Rebuilding index...")
        data = load_data(DATA_FILE)
        # build_faiss_index(data)
    
    index = faiss.read_index(FAISS_INDEX_FILE)
    with open(FAISS_DATA_FILE, "r", encoding="utf-8") as file:
        faiss_data_store = json.load(file)

    print("✅ FAISS index and data loaded successfully!")
    return index, faiss_data_store

# ✅ Hybrid Search: FAISS + Exact Match Boosting
def search_faiss(query, index, faiss_data_store, top_k=5):
    if index is None or faiss_data_store is None:
        print("⚠️ FAISS index is not loaded.")
        return []

    query = query.lower()  # Normalize query
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx != -1:  # Ensuring valid indices
            result = {
                "index": int(idx),
                "score": float(dist)*10,
                "data": faiss_data_store.get(str(idx), {})  # Fetch from JSON
            }
            results.append(result)

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

def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


index, faiss_data_store = load_faiss_index()

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


# **Elasticsearch Query Function**
def search_documents(index_name, query, size=10):
    search_query = {
        "query": {
            "query_string": {
                "query": query
            }
        }
    }
    print(f"\nProcessing Elasticsearch query: {query}")
    response = es.search(index=index_name, body=search_query, size=size)

    data = []
    # Print search results
    if response['hits']['hits']:
        print(f"\nFound {len(response['hits']['hits'])} results for '{query}':\n")
        for hit in response['hits']['hits']:
            print(f"ID: {hit['_id']} | Score: {hit['_score']}")
            val = hit['_source']
            print(f"Source: {val}\n")
            result = {
                "index": int(hit['_id']),
                "score": float(hit['_score']),
                "data": val
            }
            data.append(result)

        return data  # Return actual document field
    else:
        print(f"No results found for '{query}'.")
        return None

# **Generate LLM Prompt**
def generate_prompt(context, user_query, rag_results):
    if context == "General":
        return [{
            "role": "user",
            "content": f"""
            You are QuackBot, a General chatbot for 'Y Combinator'.
            Given the user query: "{user_query}", and the reference document: "{rag_results}",
            please provide a precise on point answer strictly based on this information provided if query is irrelavent reply with saying Out of Bound Question please ask related to Y Combinator Data.
            """
        }]
    if context == "GeneralSearch":
        return [{
            "role": "user",
            "content":f"""You are an expert in generating Elasticsearch queries. 
                Given the following database schema and sample data, generate an Elasticsearch query for user query: "{user_query}". 
                If the query has question like companies founded in 2018, 19 or any then u can search the description like W18 or S18 or F18 because they are winter, spring and fall so i need u to query similar to that any one.

                The database stores company information with the following structure:
                - company_name (String)
                - description (String)
                - status (String)
                - tags (Array of Strings)
                - location (String)
                - country (String)
                - year_founded (Integer)
                - num_founders (Integer)
                - founders_names (Array of Strings)
                - team_size (Integer)
                - website (String)
                - cb_url (String)
                - linkedin_url (String)
                - ycombinator (String)

                **Output the Elasticsearch query strictly in the following JSON format without explanations or additional text:**
                ```json
                {{
                "query": {{
                    "match": {{
                    "<field_name>": "<value>"
                    }}
                }}
                }}
                ```
                Replace `<field_name>` with the appropriate field based on the user query.
                """
            }]
    else:       
        return [{
            "role": "user",
            "content": f"""
            You are QuackBot, a specialized chatbot for {context}. 
            Using only the information provided in the reference document: "{rag_results[0].get("data")}" with metadata: {rag_results[0].get("metadata")}, answer exactly the following query: "{user_query}".
            please provide a precise answer strictly based on this information if query is irrelavent reply with saying Out of Bound Question please ask related to {context}.
            """
        }]

# **Call Groq API**
def groq_call(prompt, model):
    output = client_llm.chat.completions.create(messages=prompt, model=model)
    return output.choices[0].message.content

def extract_value_from_groq_response(groq_response):
    try:
        # Convert response to string if it's not already
        response_str = json.dumps(groq_response) if isinstance(groq_response, dict) else groq_response
        
        # Regex pattern to extract the value inside "match"
        match = re.search(r'"match"\s*:\s*{\s*"([^"]+)"\s*:\s*"([^"]+)"\s*}', response_str)

        if match:
            field_name = match.group(1)  # Extracted field name
            field_value = match.group(2)  # Extracted value
            return field_name, field_value
        else:
            return None, None
    except Exception as e:
        print(f"Error extracting value: {e}")
        return None, None


# **API Endpoints**
@app.get("/")
def home():
    return {"message": "Welcome to the Quak bot"}

# **Phase 1: Elasticsearch-based Retrieval**
@app.get("/response/phase1/{context}/{user_query}/{k_results}")
def retrival_phase1(context: str, user_query: str, k_results: int):
    start = time.time()
    index_name = "y_combinator_companies"
    
    print(f"Received phase1 retrieval request with context: {context}, user_query: {user_query}")
    
    if context == "General":
        General_prompt = generate_prompt("GeneralSearch", user_query, rag_results=None)
        groq_response = groq_call(prompt=General_prompt, model=groq_model)
        # Extract value from Groq response
        field_name, field_value = extract_value_from_groq_response(groq_response)
        print("Extracted field name and value:", field_name, field_value)

        if field_name and field_value:
            query_attribute = f"{field_value}"
        else:
            query_attribute = groq_response.get("query", groq_response)

        rag_results = search_documents(index_name, query_attribute, size=k_results)
        print("Retrieved rag_results from Elasticsearch:", rag_results)
    else:
        rag_results = search_documents(index_name, context, size=k_results)
        print("Retrieved rag_results for non-general context:", rag_results)

    if not rag_results:
        return {"error": "No relevant Elasticsearch data found."}

    rag_data = []
    for result in rag_results:
        text = result.get("data", "").get("text", "")
        ycombinator = result.get("data", "").get("metadata", "").get("ycombinator", "")
        rag_index = result.get("index", "")
        score = result.get("score", "")
        rag_data.append({"text": text, "ycombinator": ycombinator, "index": rag_index, "score": score})
    print(rag_data)
    print("Generating prompt for Groq call with rag_results...")
    prompt = generate_prompt(context, user_query, rag_results)
    print("Generated prompt:", prompt)
    output = groq_call(prompt=prompt, model=groq_model)
    print("Final output from groq_call:", output)
    # output["index_data"] = rag_data
    print(f"Time taken: {time.time() - start}")
    return [output, rag_data]


# **Phase 2: FAISS-based Retrieval**
@app.get("/response/phase2/{context}/{user_query}/{k_results}")
def retrival_phase2(context: str, user_query: str, k_results: int):
    start = time.time()
    input_text = f"{context} {user_query}"

    if context == "General":
        General_prompt = generate_prompt("GeneralSearch", user_query, rag_results=None)
        groq_response = groq_call(prompt=General_prompt, model=groq_model)
        print(groq_response)

        # Extract value from Groq response
        field_name, field_value = extract_value_from_groq_response(groq_response)

        if field_name and field_value:
            query_attribute = f"{field_value}"
        else:
            query_attribute = groq_response.get("query", groq_response)    
    
        faiss_results = search_faiss(query_attribute, index=index, faiss_data_store=faiss_data_store, top_k=k_results)
    else:
        faiss_results = search_faiss(context, index=index, faiss_data_store=faiss_data_store, top_k=k_results)
        
    if not faiss_results:
        return {"error": "No relevant Faiss data found."}
    
    # Extract "text" and "ycombinator" from FAISS results    
    faiss_data = []
    for result in faiss_results:
        text = result.get("data", "").get("text", "")
        ycombinator = result.get("data", "").get("metadata", "").get("ycombinator", "")
        faiss_index = result.get("index", "")
        score = result.get("score", "")
        faiss_data.append({"text": text, "ycombinator": ycombinator, "index": faiss_index, "score": score})
    
    print(faiss_data)

    prompt = generate_prompt(context, user_query, faiss_results)
    output = groq_call(prompt=prompt, model=groq_model)
    print("Final output from groq_call:", output)
    # output["index_data"] = faiss_data
    print(output)
    print(f"Time taken: {time.time() - start}")
    return [output, faiss_data]

# **Retrieve Company Data**
@app.get("/company_data")
def retrieve_company_data():
    try:
        company_data_path = "company_data.json"
        if os.path.exists(company_data_path):
            company_data = json.load(open(company_data_path))
            return company_data
        else:
            return {"error": "Company data file not found."}
    except Exception as e:
        return {"error": f"Error fetching company list: {e}"}

# **Delete Existing Data in Elasticsearch**
@app.delete("/delete_index/{index_name}")
def delete_index(index_name: str):
    try:
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
            return {"message": f"Index '{index_name}' deleted successfully."}
        else:
            return {"error": f"Index '{index_name}' does not exist."}
    except Exception as e:
        return {"error": f"Failed to delete index: {e}"}

# **Run API Server**
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # **Load FAISS Index and Metadata**
