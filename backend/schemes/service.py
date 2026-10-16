import json
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "schemes.json"
)

def load_schemes():
    with open(
        DATA_FILE,
        "r",
        encoding = "utf-8"
    )as file:
        return json.load(file)

def search_schemes(query:str):
    schemes = load_schemes()
    query_words = query.lower().split()
    results = []
    for scheme in schemes:
        searchable_text = " ".join([
            scheme.get("name", ""),
            scheme.get("category", ""),
            scheme.get("state", ""),
            scheme.get("description", ""),
            scheme.get("eligibility", ""),
            scheme.get("benefits", "")
        ]).lower()

        score = 0
        for word in query_words:
            if word in searchable_text:
                score += 1
            
        if score>0:
            results.append({
                "scheme": scheme,
                "score": score
            })

    results.sort(key =lambda x: x["score"],
    reverse = True)

    return results