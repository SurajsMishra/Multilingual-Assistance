from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from model import Grievance, User
from schemas import (GrievanceCreate, GrievanceResponse, StatusUpdate)
from services.grievance_service import classify_grievance
from ai.grievance_ai import classify_with_ai
from services.language_service import detect_language

router = APIRouter(
    prefix="/grievances",
    tags=["Grievances"]
)

def generate_grievance_id(db: Session):
    count = db.query(Grievance).count() + 1
    year = datetime.now().year
    return f"GRV-{year}-{count:05d}"

@router.post("", response_model=GrievanceResponse)
def create_grievance(
    grievance: GrievanceCreate,
    db: Session = Depends(get_db)
):

    if grievance.language == "auto":
        detected_language = detect_language(grievance.original_text)
    else:
        detected_language = grievance.language
    try:
        ai_result = classify_with_ai(
            grievance.original_text,
            detected_language
        )
        category=ai_result.category
        department=ai_result.department
        priority=ai_result.priority
        summary=ai_result.summary
        
    except Exception as e:
        print("AI Classification Failed:", e)
        from services.grievance_service import classify_grievance
        fallback = classify_grievance(
            grievance.original_text
        )
        category = fallback["category"]
        department = fallback["department"]
        priority = fallback["priority"]
        summary = fallback["summary"]

    grievance_id = generate_grievance_id(db)
    new_grievance = Grievance(
        grievance_id=grievance_id,
        user_id=grievance.user_id,
        language=detected_language,
        original_text=grievance.original_text,
        location=grievance.location,
        category=category,
        department=department,
        priority=priority,
        summary=summary,
        status="submitted"
    )
    db.add(new_grievance)
    db.commit()
    db.refresh(new_grievance)
    return new_grievance

@router.get("", response_model=list[GrievanceResponse])
def get_grievances(
    db: Session = Depends(get_db)
):
    return db.query(Grievance).all()

@router.get("/{grievance_id}", response_model=GrievanceResponse)
def get_grievance_by_id(
    grievance_id: str, db: Session = Depends(get_db)
):
    grievance = (
        db.query(Grievance)
        .filter(
            Grievance.grievance_id == grievance_id
        ).first()
    )
    if not grievance:
        raise HTTPException(
            status_code=404,
            detail="Grievance not found"
        )
    return grievance

@router.put("/{grievance_id}/status")
def update_status(
    grievance_id: str,
    data: StatusUpdate,
    db: Session = Depends(get_db)
):
    allowed_statuses = [
        "submitted", "assigned", "in_progress", "resolved", "rejected"
    ]

    if data.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    grievance = (
        db.query(Grievance).filter(
            Grievance.grievance_id == grievance_id
        ).first()
    )

    if not grievance:
        raise HTTPException(
            status_code=404,
            detail="Grievance not found"
        )
    grievance.status = data.status
    db.commit()
    db.refresh(grievance)
    return {
        "message": "status updated",
        "grievance_id": grievance.grievance_id,
        "status": grievance.status
    }