from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

# Helper to convert ObjectId to string
class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.str_schema()

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str = Field(alias="_id", default=None)
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# Job Role Schemas
class JobRoleBase(BaseModel):
    title: str
    description: Optional[str] = None

class JobRoleCreate(JobRoleBase):
    pass

class JobRoleResponse(JobRoleBase):
    id: str = Field(alias="_id", default=None)
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# Interview Schemas
class InterviewBase(BaseModel):
    job_role_id: str

class InterviewCreate(InterviewBase):
    pass

class InterviewResponse(BaseModel):
    id: str = Field(alias="_id", default=None)
    candidate_id: str
    job_role_id: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    technical_score: float
    clarity_score: float
    relevance_score: float
    sentiment_score: float
    final_score: float
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# Question Schemas
class QuestionBase(BaseModel):
    question_text: str
    question_number: int

class QuestionResponse(QuestionBase):
    id: str = Field(alias="_id", default=None)
    interview_id: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# Response Schemas
class ResponseBase(BaseModel):
    response_text: str

class ResponseCreate(ResponseBase):
    question_id: str

class ResponseEvaluation(BaseModel):
    technical_score: float
    clarity_score: float
    relevance_score: float
    sentiment_score: float

class ResponseDetail(ResponseBase):
    id: str = Field(alias="_id", default=None)
    interview_id: str
    question_id: str
    technical_score: float
    clarity_score: float
    relevance_score: float
    sentiment_score: float
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

# Dashboard Schemas
class CandidateSummary(BaseModel):
    candidate_id: str
    candidate_username: str
    candidate_email: str
    interview_id: str
    job_role: str
    final_score: float
    status: str
    completed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
