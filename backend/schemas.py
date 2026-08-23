from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# User Schemas
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    language: str = Field("auto", max_length=10)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Grievance Schemas
class GrievanceCreate(BaseModel):
    original_text: str = Field(
        ..., min_length=5,
        max_length=5000,
        description="Raw input grievance text from the user"
    )
    language: str = Field("auto", max_length=10)
    location: Optional[str] = Field(None, max_length=255)
    user_id: Optional[int] = None

class GrievanceResponse(BaseModel):
    id: int
    grievance_id: str
    user_id: Optional[int] = None
    language: str
    original_text: Optional[str] = None
    category: Optional[str] = None
    department: Optional[str] = None
    priority: str
    location: Optional[str] = None
    summary: Optional[str] = None
    status: str
    created_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True

class StatusUpdate(BaseModel):
    status: str = Field(..., max_length=50)