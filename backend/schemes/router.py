from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import json
import os
from .service import search_schemes
from rag.assistant import ask_scheme_assistant

router = APIRouter(
    prefix="/schemes",
    tags=["Schemes"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(
    BASE_DIR, "data", "schemes.json"
)

class SchemeQuestion(BaseModel):
    question: str

@router.post("/ask")
def ask_scheme(question: SchemeQuestion):
    result = ask_scheme_assistant(question.question)
    return {
        "success": True,
        "question": question.question,
        "answer": result["answer"],
        "sources": result.get("sources", [])
    }
    
def load_schemes():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@router.get("/")
def get_schemes():
    schemes = load_schemes()
    return {
        "success": True,
        "count": len(schemes),
        "schemes": schemes
    }

@router.get("/search")
def search_scheme_endpoint(
    q: str = Query(..., min_length=1)
):
    results = search_schemes(q)
    return {
        "success": True,
        "query": q,
        "count": len(results),
        "results": results
    } 

@router.get("/{scheme_name}")
def get_scheme(scheme_name: str):
    schemes = load_schemes()
    for scheme in schemes:
        if scheme["name"].lower() == scheme_name.lower():
            return {
                "success": True,
                "scheme": scheme
            }
    raise HTTPException(
        status_code=404,
        detail="Scheme not found"
    )