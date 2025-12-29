from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter()

@router.get("/candidates", response_model=List[schemas.CandidateSummary])
def get_all_candidates(db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)):
    """Get all candidates with their interview scores (HR only)"""
    if current_user.role != "hr":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can access candidate data"
        )
    
    # Get all completed interviews with candidate and job role info
    interviews = db.query(models.Interview).filter(
        models.Interview.status == "completed"
    ).all()
    
    candidate_summaries = []
    for interview in interviews:
        candidate = db.query(models.User).filter(models.User.id == interview.candidate_id).first()
        job_role = db.query(models.JobRole).filter(models.JobRole.id == interview.job_role_id).first()
        
        if candidate and job_role:
            candidate_summaries.append(schemas.CandidateSummary(
                candidate_id=candidate.id,
                candidate_username=candidate.username,
                candidate_email=candidate.email,
                interview_id=interview.id,
                job_role=job_role.title,
                final_score=interview.final_score,
                status=interview.status,
                completed_at=interview.completed_at
            ))
    
    # Sort by final score (descending)
    candidate_summaries.sort(key=lambda x: x.final_score, reverse=True)
    
    return candidate_summaries

@router.get("/candidates/{candidate_id}/interview/{interview_id}")
def get_candidate_interview_details(candidate_id: int, interview_id: int,
                                    db: Session = Depends(get_db),
                                    current_user: models.User = Depends(get_current_user)):
    """Get detailed interview information for a candidate (HR only)"""
    if current_user.role != "hr":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can access candidate details"
        )
    
    interview = db.query(models.Interview).filter(
        models.Interview.id == interview_id,
        models.Interview.candidate_id == candidate_id
    ).first()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    candidate = db.query(models.User).filter(models.User.id == candidate_id).first()
    job_role = db.query(models.JobRole).filter(models.JobRole.id == interview.job_role_id).first()
    questions = db.query(models.Question).filter(
        models.Question.interview_id == interview_id
    ).order_by(models.Question.question_number).all()
    
    responses = db.query(models.InterviewResponse).filter(
        models.InterviewResponse.interview_id == interview_id
    ).all()
    
    # Build response map
    response_map = {r.question_id: r for r in responses}
    
    # Build detailed response
    detailed_questions = []
    for question in questions:
        response = response_map.get(question.id)
        detailed_questions.append({
            "question_id": question.id,
            "question_text": question.question_text,
            "question_number": question.question_number,
            "response": {
                "response_text": response.response_text if response else None,
                "technical_score": response.technical_score if response else None,
                "clarity_score": response.clarity_score if response else None,
                "relevance_score": response.relevance_score if response else None,
                "sentiment_score": response.sentiment_score if response else None,
            } if response else None
        })
    
    return {
        "candidate": {
            "id": candidate.id,
            "username": candidate.username,
            "email": candidate.email
        },
        "job_role": job_role.title if job_role else None,
        "interview": {
            "id": interview.id,
            "status": interview.status,
            "started_at": interview.started_at,
            "completed_at": interview.completed_at,
            "technical_score": interview.technical_score,
            "clarity_score": interview.clarity_score,
            "relevance_score": interview.relevance_score,
            "sentiment_score": interview.sentiment_score,
            "final_score": interview.final_score
        },
        "questions_and_responses": detailed_questions
    }

@router.get("/statistics")
def get_dashboard_statistics(db: Session = Depends(get_db),
                             current_user: models.User = Depends(get_current_user)):
    """Get dashboard statistics (HR only)"""
    if current_user.role != "hr":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can access statistics"
        )
    
    total_interviews = db.query(models.Interview).count()
    completed_interviews = db.query(models.Interview).filter(
        models.Interview.status == "completed"
    ).count()
    in_progress_interviews = db.query(models.Interview).filter(
        models.Interview.status == "in_progress"
    ).count()
    total_candidates = db.query(models.User).filter(models.User.role == "candidate").count()
    total_roles = db.query(models.JobRole).count()
    
    # Calculate average final score
    completed = db.query(models.Interview).filter(
        models.Interview.status == "completed"
    ).all()
    avg_score = sum(i.final_score for i in completed) / len(completed) if completed else 0
    
    return {
        "total_interviews": total_interviews,
        "completed_interviews": completed_interviews,
        "in_progress_interviews": in_progress_interviews,
        "total_candidates": total_candidates,
        "total_job_roles": total_roles,
        "average_final_score": round(avg_score, 2) if completed else 0
    }

