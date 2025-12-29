from beanie import Document
from pydantic import Field, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId

class User(Document):
    email: EmailStr
    username: str = Field(..., unique=True)
    hashed_password: str
    role: str  # "hr" or "candidate"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "username",
        ]

class JobRole(Document):
    title: str = Field(..., unique=True)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "job_roles"
        indexes = [
            "title",
        ]

class Interview(Document):
    candidate_id: ObjectId
    job_role_id: ObjectId
    status: str = "in_progress"  # "in_progress", "completed", "cancelled"
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # Final scores
    technical_score: float = 0.0
    clarity_score: float = 0.0
    relevance_score: float = 0.0
    sentiment_score: float = 0.0
    final_score: float = 0.0
    
    class Settings:
        name = "interviews"
        indexes = [
            "candidate_id",
            "job_role_id",
            "status",
        ]

class Question(Document):
    interview_id: ObjectId
    question_text: str
    question_number: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "questions"
        indexes = [
            "interview_id",
        ]

class InterviewResponse(Document):
    interview_id: ObjectId
    question_id: ObjectId
    response_text: str
    
    # Individual scores for this response
    technical_score: float = 0.0
    clarity_score: float = 0.0
    relevance_score: float = 0.0
    sentiment_score: float = 0.0
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "interview_responses"
        indexes = [
            "interview_id",
            "question_id",
        ]
