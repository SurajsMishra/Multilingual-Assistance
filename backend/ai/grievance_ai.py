import json
from pydantic import BaseModel
from ai.groq import generate_response
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

Choose exactly ONE category from:
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

Choose exactly ONE department from:
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

Choose exactly ONE priority from:
low
medium
high
critical

Choose exactly ONE intent from:
grievance
scheme_query
general_query

Rules:
- Understand Hindi, English and Hinglish.
- Preserve the meaning of the citizen's complaint.
- Do not invent facts.
- Use critical only for serious emergencies or threats to life.
- Keep the summary short.
- Return ONLY valid JSON.
"""

    response = generate_response(
        prompt,
        temperature=0,
        max_tokens=300
    )

    data = json.loads(response)

    # Safety fallback if the model forgets the summary
    if not data.get("summary"):
        data["summary"] = text

    # Validate against our Pydantic model
    result = GrievanceResult.model_validate(data)

    return result