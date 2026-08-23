from pydantic import BaseModel
from ollama import chat
class GrievanceResult(BaseModel):
    category : str
    department: str
    priority : str
    summary: str
    intent: str

def classify_with_ai(text: str, language: str):
    prompt = f"""
    You are an AI classifier for a government citizen grievance system.

Analyze the citizen complaint.
Citizen language:
{language}

Complaint:
{text}

Choose exactly one category:
water_supply
road
electricity
sanitation
ration
pension
healthcare
education
transport
municipal
general

Choose exactly one depatment:
water_department
pwd
electricity_department
municipal_department
food_department
social_welfare_department
health_department
education_department
transport_department
general_department

Choose exactly one priority:
low
medium
high
critical

Choose exactly one intent:

grievance
scheme_query
general_query

Rules:

- Understand Hindi, English and Hinglish.
- Preserve the meaning of the citizen's complaint.
- Do not invent facts.
- Use critical only for serious emergencies or threats to life.
- Keep the summary short.
"""

    response = chat(
        model = "llama3.2:3b",
        messages = [
            {
                "role": "system",
                "content":(
                    "You classify citizen complaint info"
                    "structured govermnment-service categories."
                )
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        format=GrievanceResult.model_json_schema(),
        options={
            "temperature": 0
        }
    )

    result = GrievanceResult.model_validate_json(response.message.content)
    return result