from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from model import Grievance, User
from schemas import (GrievanceCreate, GrievanceResponse, StatusUpdate)
from services.grievance_service import classify_grievance
from ai.grievance_ai import classify_with_ai
from services.language_service import detect_language
from services.speech_service import speech_to_text
from fastapi import UploadFile, File
from services.tts_service import text_to_speech
from fastapi.responses import FileResponse
import os


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

@router.post("/Voice")
async def create_voice_grievance(
    audio: UploadFile = File (...),
    db: Session = Depends(get_db)
):
    import os
    import uuid
    file_extension = os.path.splitext(audio.filename)[1].lower()
    if not file_extension:
        file_extension = ".webm"

    audio_path = f"temp_{uuid.uuid4()}{file_extension}"
    try:
        with open(audio_path, "wb") as f:
            f.write(await audio.read())
        print("Audio file:", audio_path)
        print("Audio extension:", file_extension)
        print("Audio size:", os.path.getsize(audio_path), "bytes")
        speech_result = speech_to_text(audio_path)
        text = speech_result["text"]
        detected_language = speech_result["language"]
        print("Transcribed text:", text)
        print("Detected Language:", detected_language)
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail = "Could not understand audio."
            )   
    
        try:
            ai_result = classify_with_ai(
                text,
                detected_language
            )
            category = ai_result.category
            department = ai_result.department
            priority = ai_result.priority
            summary = ai_result.summary
        except Exception as e:
            print("AI Classification failed", e)
            fallback = classify_grievance(text)
            category = fallback["category"]
            department = fallback["department"]
            priority = fallback["priority"]
            summary = fallback["summary"]

        intent = "grievance"
        grievance_id = generate_grievance_id(db)
        if detected_language == "hi":
            response_text = (
                f"आपकी शिकायत सफलतापूर्वक दर्ज कर ली गई है। "
                f"आपकी शिकायत संख्या {grievance_id} है।"
            )
        else:
            response_text = (
                f"Your grievance has been successfully registered. "
                f"Your grievance number is {grievance_id}."
            )

        new_grievance = Grievance(
            grievance_id=grievance_id,
            original_text=text,
            language=detected_language,
            category=category,
            department=department,
            priority=priority,
            summary=summary,
            status="submitted"
        )
        db.add(new_grievance)
        db.commit()
        db.refresh(new_grievance)
        audio_dir = "audio"
        os.makedirs(
            audio_dir,
            exist_ok=True
        )
        audio_filename = f"{grievance_id}.mp3"
        audio_output_path = os.path.join(
            audio_dir,
            audio_filename
        )
        print("Generating TTS....")
        print("Audio path:", audio_output_path)
        await text_to_speech(
            response_text,
            detected_language,
            audio_output_path
        )
        print("Audio generated:", os.path.exists(audio_output_path))
        return {
            "success": True,
            "grievance_id": grievance_id,
            "text": text,
            "language": detected_language,
            "category": category,
            "department": department,
            "priority": priority,
            "summary": summary,
            "intent": intent,
            "status": "submitted",
            "response_text": response_text,
            "audio_url": f"/grievances/audio/{audio_filename}"
        }
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print("Cleaned up temp audio file:", audio_path)

@router.get("/audio/{filename}")
async def get_audio(filename: str):
    import os
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
    audio_dir = os.path.join(
        BASE_DIR,
        "audio"
    )
    file_path = os.path.join(
        audio_dir,
        filename
    )
    print("Audio directory:", audio_dir)
    print("Request file:", filename)
    print("Full audio path:", file_path)
    print("File exists:", os.path.exists(file_path))
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Audio file not found: {filename}"
        )

    return FileResponse(
        file_path,
        media_type = "audio/mpeg",
        filename = filename
    )
