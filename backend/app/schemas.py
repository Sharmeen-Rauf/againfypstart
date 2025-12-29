from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Job Role Schemas
class JobRoleBase(BaseModel):
    title: str
    description: Optional[str] = None

class JobRoleCreate(JobRoleBase):
    pass

class JobRoleResponse(JobRoleBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Interview Schemas
class InterviewBase(BaseModel):
    job_role_id: int

class InterviewCreate(InterviewBase):
    pass

class InterviewResponse(BaseModel):
    id: int
    candidate_id: int
    job_role_id: int
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    technical_score: float
    clarity_score: float
    relevance_score: float
    sentiment_score: float
    final_score: float
    
    class Config:
        from_attributes = True

# Question Schemas
class QuestionBase(BaseModel):
    question_text: str
    question_number: int

class QuestionResponse(QuestionBase):
    id: int
    interview_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Response Schemas
class ResponseBase(BaseModel):
    response_text: str

class ResponseCreate(ResponseBase):
    question_id: int

class ResponseEvaluation(BaseModel):
    technical_score: float
    clarity_score: float
    relevance_score: float
    sentiment_score: float

class ResponseDetail(ResponseBase):
    id: int
    interview_id: int
    question_id: int
    technical_score: float
    clarity_score: float
    relevance_score: float
    sentiment_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Dashboard Schemas
class CandidateSummary(BaseModel):
    candidate_id: int
    candidate_username: str
    candidate_email: str
    interview_id: int
    job_role: str
    final_score: float
    status: str
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

