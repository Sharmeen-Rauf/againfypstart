from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user
from app.ai_service import generate_role_questions, evaluate_response, calculate_final_score

router = APIRouter()

@router.post("/start", response_model=schemas.InterviewResponse)
def start_interview(interview_data: schemas.InterviewCreate, db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)):
    """Start a new interview"""
    if current_user.role != "candidate":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can start interviews"
        )
    
    # Verify job role exists
    job_role = db.query(models.JobRole).filter(models.JobRole.id == interview_data.job_role_id).first()
    if not job_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job role not found"
        )
    
    # Check if candidate has an in-progress interview
    existing_interview = db.query(models.Interview).filter(
        models.Interview.candidate_id == current_user.id,
        models.Interview.status == "in_progress"
    ).first()
    
    if existing_interview:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an interview in progress"
        )
    
    # Create interview
    db_interview = models.Interview(
        candidate_id=current_user.id,
        job_role_id=interview_data.job_role_id,
        status="in_progress"
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    
    # Generate questions for this role
    questions_text = generate_role_questions(job_role.title, num_questions=5)
    
    # Create question records
    for idx, question_text in enumerate(questions_text, 1):
        db_question = models.Question(
            interview_id=db_interview.id,
            question_text=question_text,
            question_number=idx
        )
        db.add(db_question)
    
    db.commit()
    
    return db_interview

@router.get("/current", response_model=schemas.InterviewResponse)
def get_current_interview(db: Session = Depends(get_db),
                          current_user: models.User = Depends(get_current_user)):
    """Get current in-progress interview for candidate"""
    if current_user.role != "candidate":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can access their interviews"
        )
    
    interview = db.query(models.Interview).filter(
        models.Interview.candidate_id == current_user.id,
        models.Interview.status == "in_progress"
    ).first()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No interview in progress"
        )
    
    return interview

@router.get("/{interview_id}/questions", response_model=List[schemas.QuestionResponse])
def get_interview_questions(interview_id: int, db: Session = Depends(get_db),
                            current_user: models.User = Depends(get_current_user)):
    """Get all questions for an interview"""
    interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Check if user has access to this interview
    if current_user.role == "candidate" and interview.candidate_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    questions = db.query(models.Question).filter(
        models.Question.interview_id == interview_id
    ).order_by(models.Question.question_number).all()
    
    return questions

@router.post("/{interview_id}/respond")
def submit_response(interview_id: int, response_data: schemas.ResponseCreate,
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)):
    """Submit response to a question"""
    if current_user.role != "candidate":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can submit responses"
        )
    
    # Verify interview exists and belongs to candidate
    interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    if interview.candidate_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if interview.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview is not in progress"
        )
    
    # Verify question exists and belongs to this interview
    question = db.query(models.Question).filter(
        models.Question.id == response_data.question_id,
        models.Question.interview_id == interview_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Check if response already exists
    existing_response = db.query(models.InterviewResponse).filter(
        models.InterviewResponse.question_id == response_data.question_id
    ).first()
    
    if existing_response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Response already submitted for this question"
        )
    
    # Evaluate response using AI
    evaluation = evaluate_response(question.question_text, response_data.response_text)
    
    # Create response record
    db_response = models.InterviewResponse(
        interview_id=interview_id,
        question_id=response_data.question_id,
        response_text=response_data.response_text,
        technical_score=evaluation["technical_score"],
        clarity_score=evaluation["clarity_score"],
        relevance_score=evaluation["relevance_score"],
        sentiment_score=evaluation["sentiment_score"]
    )
    
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    
    return {
        "message": "Response submitted successfully",
        "response_id": db_response.id,
        "scores": {
            "technical_score": evaluation["technical_score"],
            "clarity_score": evaluation["clarity_score"],
            "relevance_score": evaluation["relevance_score"],
            "sentiment_score": evaluation["sentiment_score"]
        }
    }

@router.post("/{interview_id}/complete")
def complete_interview(interview_id: int, db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)):
    """Complete an interview and calculate final scores"""
    if current_user.role != "candidate":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can complete interviews"
        )
    
    interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    if interview.candidate_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if interview.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview is not in progress"
        )
    
    # Get all responses for this interview
    responses = db.query(models.InterviewResponse).filter(
        models.InterviewResponse.interview_id == interview_id
    ).all()
    
    if not responses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No responses submitted"
        )
    
    # Calculate average scores
    avg_technical = sum(r.technical_score for r in responses) / len(responses)
    avg_clarity = sum(r.clarity_score for r in responses) / len(responses)
    avg_relevance = sum(r.relevance_score for r in responses) / len(responses)
    avg_sentiment = sum(r.sentiment_score for r in responses) / len(responses)
    
    # Calculate final score
    final_score = calculate_final_score(avg_technical, avg_clarity, avg_relevance, avg_sentiment)
    
    # Update interview
    interview.technical_score = round(avg_technical, 2)
    interview.clarity_score = round(avg_clarity, 2)
    interview.relevance_score = round(avg_relevance, 2)
    interview.sentiment_score = round(avg_sentiment, 2)
    interview.final_score = final_score
    interview.status = "completed"
    interview.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(interview)
    
    return {
        "message": "Interview completed successfully",
        "final_scores": {
            "technical_score": interview.technical_score,
            "clarity_score": interview.clarity_score,
            "relevance_score": interview.relevance_score,
            "sentiment_score": interview.sentiment_score,
            "final_score": interview.final_score
        }
    }

@router.get("/{interview_id}/responses", response_model=List[schemas.ResponseDetail])
def get_interview_responses(interview_id: int, db: Session = Depends(get_db),
                            current_user: models.User = Depends(get_current_user)):
    """Get all responses for an interview"""
    interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Check access
    if current_user.role == "candidate" and interview.candidate_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    responses = db.query(models.InterviewResponse).filter(
        models.InterviewResponse.interview_id == interview_id
    ).all()
    
    return responses

