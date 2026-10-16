import sys
from ollama import chat

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

response = chat(
    model = "llama3.2:3b",
    messages=[{
        "role": "user",
        "content": "Say hello in hindi"
    }]
)
print(response.message.content)
