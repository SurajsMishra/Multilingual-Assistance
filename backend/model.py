from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable = False)
    phone = Column(String(20), nullable = True)
    language = Column(String(10), default ="en")
    created_at = Column(DateTime, default=datetime.utcnow)
class Grievance(Base):
    __tablename__ ="grievances"
    id = Column(Integer, primary_key=True, index=True)
    grievance_id = Column(String(30), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = True)
    language = Column(String(10), default = "en")
    original_text = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    department = Column(String(100), nullable = True)
    priority = Column(String(20), default = "medium")
    location = Column(String(255), nullable= True)
    summary = Column(Text, nullable = True)
    status = Column(String(20), default="submitted")
    created_at = Column(DateTime, default=datetime.utcnow)
    update_at = Column(DateTime, default=datetime.utcnow, onupdate = datetime.utcnow)
