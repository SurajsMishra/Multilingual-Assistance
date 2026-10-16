import json
import os
from .vector_store import add_scheme
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "schemes", "data", "schemes.json")
def index_schemes():
    with open(DATA_FILE,"r", encoding="utf-8")as file:
        schemes = json.load(file)
    for index, scheme in enumerate(schemes):
        text = f"""
        Scheme Name: {scheme.get('name', '')}
        Category: {scheme.get('category', '')}
        State: {scheme.get('state', '')}
        Description: {scheme.get('description', '')}
        Eligibility: {scheme.get('eligibility', '')}
        Benefits:  {scheme.get('benefits', '')}
        Documents: {','.join(scheme.get('documents', []))}
        Application: {scheme.get('application', '')}
        """
        add_scheme(
            scheme_id=f"scheme_{index}",
            text=text,
            metadata={
                "name": scheme.get("name", ""),
                "category": scheme.get("category", ""),
                "state": scheme.get("state", "")
            }
        )
    print(f"Successfully indexed {len(schemes)} schemes.")
if __name__ == "__main__":
    index_schemes()
    