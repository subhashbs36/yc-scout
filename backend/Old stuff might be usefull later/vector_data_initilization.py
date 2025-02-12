import json
import faiss
import numpy as np

import ollama  # Assuming you have this module available

def vector_data_initialization():
    # Load data
    data = json.load(open('data/company_data_cleaned_final.json'))

    # Initialize FAISS index. Replace 768 with your embedding dimension.
    embedding_dim = 768
    index = faiss.IndexFlatL2(embedding_dim)
    
    # List to hold document texts and their metadata
    documents = []
    metadatas = []

    for i, d in enumerate(data):
        metadata = d['metadata']

        # Get embedding from ollama embed model
        response = ollama.embed(model='jina/jina-embeddings-v2-base-en:latest', input=d['text'])
        embeddings = response['embeddings']  # assuming this returns a list of floats
        
        # Convert embedding to a NumPy array (1, dim) of type float32 for FAISS
        embedding_np = np.array(embeddings, dtype='float32').reshape(1, -1)
        index.add(embedding_np)

        documents.append(d['text'])
        metadatas.append({
            'company_name': metadata.get('company_name', ''),
            'description': metadata.get('description', ''),
            'tags': ''.join(str(x) for x in metadata.get('tags', [])),
            'location': metadata.get('location', ''),
            'country': metadata.get('country', ''),
            'year_founded': metadata.get('year_founded', 0),
            'num_founders': metadata.get('num_founders', 0),
            'founders_names': ''.join(str(x) for x in metadata.get('founders_names', [])),
            'team_size': metadata.get('team_size', 0),
            'website': metadata.get('website', ''),
            'linkedin_url': metadata.get('linkedin_url', ''),
            'status': metadata.get('sta', '')
        })

    # Now, 'index' contains all the embeddings and you can perform searches.
    # 'documents' and 'metadatas' are lists that map to each index.
    return index, documents, metadatas
