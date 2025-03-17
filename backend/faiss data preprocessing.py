import numpy as np
np.float_ = np.float64
import json
document_path = 'company_data.json' 
data = json.load(open(document_path))

document = []

for obj in data:
    text_data = f"{obj['company_name']} {obj['short_description']} {obj['long_description']}"
    metadata = {
        'company_name': obj['company_name'],
        'description': obj['batch'],
        'status': obj['status'],
        'tags': obj['tags'],
        'location': obj['location'],
        'country': obj['country'],
        'year_founded': obj['year_founded'],
        'num_founders': obj['num_founders'],
        'founders_names': obj['founders_names'],
        'team_size': obj['team_size'],
        'website': obj['website'],
        'cb_url': obj['cb_url'],
        'linkedin_url': obj['linkedin_url'],
        'ycombinator': obj["company_url"]
    }
    document.append({'text': text_data, 'metadata': metadata})

json.dump(document,open('company_data_cleaned_final.json','w'),indent=4)