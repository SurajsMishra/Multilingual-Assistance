from ai.groq import generate_response


def generate_answer(question: str, context: str):

    # Keep the context small and focused
    context = context[:2000]

    prompt = f"""
You are an Indian government scheme assistant.

Use ONLY the information provided in the scheme information below.

SCHEME INFORMATION:
{context}

USER QUESTION:
{question}

Instructions:
1. Identify the most relevant scheme.
2. Explain why it is relevant to the user.
3. Mention eligibility and benefits only if they are present in the provided information.
4. Do not invent information.
5. If some information is missing, clearly say that it needs to be verified.
6. Answer in the same language as the user's question.
7. Keep the answer concise and easy to understand.

Answer:
"""

    return generate_response(
        prompt,
        temperature=0.1,
        max_tokens=200
    )