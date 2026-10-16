import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.retriever import retrieve_schemes

query = "I need financial help for my education"
results = retrieve_schemes(query, top_k=3)
print("\nSEARCH RESULT\n")
print(results)