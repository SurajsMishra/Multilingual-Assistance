from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from model import Grievance, User
from schemas import (GrievanceCreate, GrievanceResponse, StatusUpdate)
from services.grievance_service import classify_grievance

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
    classification = classify_grievance(
        grievance.original_text
    )
    grievance_id = generate_grievance_id(db)
    new_grievance = Grievance(
        grievance_id=grievance_id,
        user_id=grievance.user_id,
        language=grievance.language,
        original_text=grievance.original_text,
        location=grievance.location,
        category=classification["category"],
        department=classification["department"],
        priority=classification["priority"],
        summary=classification["summary"],
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