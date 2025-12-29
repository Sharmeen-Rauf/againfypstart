from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # "hr" or "candidate"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    interviews = relationship("Interview", back_populates="candidate")
    
class JobRole(Base):
    __tablename__ = "job_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    interviews = relationship("Interview", back_populates="job_role")
    
class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"))
    job_role_id = Column(Integer, ForeignKey("job_roles.id"))
    status = Column(String, default="in_progress")  # "in_progress", "completed", "cancelled"
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Final scores
    technical_score = Column(Float, default=0.0)
    clarity_score = Column(Float, default=0.0)
    relevance_score = Column(Float, default=0.0)
    sentiment_score = Column(Float, default=0.0)
    final_score = Column(Float, default=0.0)
    
    # Relationships
    candidate = relationship("User", back_populates="interviews")
    job_role = relationship("JobRole", back_populates="interviews")
    responses = relationship("InterviewResponse", back_populates="interview", cascade="all, delete-orphan")
    
class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question_text = Column(Text)
    question_number = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    response = relationship("InterviewResponse", back_populates="question", uselist=False)
    
class InterviewResponse(Base):
    __tablename__ = "interview_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    response_text = Column(Text)
    
    # Individual scores for this response
    technical_score = Column(Float, default=0.0)
    clarity_score = Column(Float, default=0.0)
    relevance_score = Column(Float, default=0.0)
    sentiment_score = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    interview = relationship("Interview", back_populates="responses")
    question = relationship("Question", back_populates="response")

