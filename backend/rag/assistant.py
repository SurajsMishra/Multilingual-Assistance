from .retriever import retrieve_schemes
from .llm import generate_answer


def ask_scheme_assistant(question: str):

    schemes = retrieve_schemes(question, top_k=1)

    if not schemes:
        return {
            "answer": "I could not find a relevant government scheme.",
            "sources": []
        }

    scheme = schemes[0]

    context = scheme["document"][:1200]

    answer = generate_answer(
        question,
        context
    )

    sources = [
        scheme["metadata"]
    ]

    return {
        "answer": answer,
        "sources": sources
    }