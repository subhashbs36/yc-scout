import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
# import ollama 
import chromadb
from chromadb.config import DEFAULT_DATABASE,DEFAULT_TENANT,Settings
import asyncio
import os
from groq import Groq
from dotenv import load_dotenv
import time
from utill import *

# Load environment variables
load_dotenv()

app  = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:9200"],  # Change to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

#Initialization #################################################################

groq_model = 'llama-3.3-70b-versatile'
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
 
@app.get('/')
def home():
    return {'message':'Welcome to the Quak bot'}

#Phase 2 ######################################################

@app.get('/response/phase1/{context}/{user_query}')
def retrival_phase1(context: str, user_query: str):
    start = time.time()

    # Prepare the input text
    input_text = context + " " + user_query
    # Query the database (assuming 'collection' is defined elsewhere)
    index_name = "y_combinator_companies"
    rag_results, rag_meta = search_documents(index_name, input_text)
    general_msg = [{
            "role": "user",
            "content": f"""
            You are QuackBot, a domain-specific chatbot for {context}. 
            Given the user query: "{user_query}", and the reference document: "{rag_results}" with metadata: {rag_meta}, 
            please provide a precise answer strictly based on this information. Do not show your thought process, just provide the direct answer.
            """
            }]
    company_specific_msg = [{
            "role": "user",
            "content": f"""
            You are QuackBot, a domain-specific chatbot for {context}. 
            Given the user query: "{user_query}", and the reference document: "{rag_results}" with metadata: {rag_meta}, 
            please provide a precise answer strictly based on this information. Do not show your thought process, just provide the direct answer.
            """
            }
            ]
    if context.lower() != 'genral' :
        if user_query.lower() in ["hi", "hello", "hey", "how are you", "what's up"]:
            return "Hello! How can I assist you today?"
        
        output = groq_call(
            prompt=general_msg,
            model=groq_model,
        )
        
    else:
        output = groq_call(
            prompt=company_specific_msg,
            model=groq_model
        )
    print(f'time taken is  {time.time() - start}')
    return  output

###############################################################

#Phase 2 ######################################################

@app.get('/response/phase2/{context}/{user_query}')
def retrival_phase2(context: str, user_query: str):
    start = time.time()

    # Prepare the input text
    input_text = context + " " + user_query
    # Tokenize the input text
    input = embedd_input(input_text)
    # Query the database (assuming 'collection' is defined elsewhere)
    rag_results, rag_meta = chroma_call(input)
    general_msg = [{
            "role": "user",
            "content": f"""
            You are QuackBot, a domain-specific chatbot for {context}. 
            Given the user query: "{user_query}", and the reference document: "{rag_results}" with metadata: {rag_meta}, 
            please provide a precise answer strictly based on this information. Do not show your thought process, just provide the direct answer.
            """
            }]
    company_specific_msg = [{
            "role": "user",
            "content": f"""
            You are QuackBot, a domain-specific chatbot for {context}. 
            Given the user query: "{user_query}", and the reference document: "{rag_results}" with metadata: {rag_meta}, 
            please provide a precise answer strictly based on this information. Do not show your thought process, just provide the direct answer.
            """
            }
            ]
    if context.lower() != 'genral' :
        if user_query.lower() in ["hi", "hello", "hey", "how are you", "what's up"]:
            return "Hello! How can I assist you today?"
        
        output = groq_call(
            prompt=general_msg,
            model=groq_model,
        )
        
    else:
        output = groq_call(
            prompt=company_specific_msg,
            model=groq_model
        )
    print(f'time taken is  {time.time() - start}')
    return  output

@app.get('/company_data')
def retrive_company_data():
    try:
        company_data = json.load(open('data/company_data_cleaned_final.json'))
        return  company_data
    except Exception as e:
        return (f'Error Fetching the company list : {e}')

###############################################################################

if __name__ == '__main__':
    uvicorn.run(app , host = '0.0.0.0', port = 8000 , reload=True)