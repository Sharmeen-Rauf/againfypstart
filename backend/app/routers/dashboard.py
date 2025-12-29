from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app import models, schemas
from app.auth import get_current_user
from bson import ObjectId

router = APIRouter()

@router.get("/candidates", response_model=List[schemas.CandidateSummary])
async def get_all_candidates(current_user: models.User = Depends(get_current_user)):
    """Get all candidates with their interview scores (HR only)"""
    if current_user.role != "hr":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can access candidate data"
        )
    
    # Get all completed interviews
    interviews = await models.Interview.find(
        models.Interview.status == "completed"
    ).to_list()
    
    candidate_summaries = []
    for interview in interviews:
        candidate = await models.User.get(interview.candidate_id)
        job_role = await models.JobRole.get(interview.job_role_id)
        
        if candidate and job_role:
            candidate_summaries.append(schemas.CandidateSummary(
                candidate_id=str(candidate.id),
                candidate_username=candidate.username,
                candidate_email=candidate.email,
                interview_id=str(interview.id),
                job_role=job_role.title,
                final_score=interview.final_score,
                status=interview.status,
                completed_at=interview.completed_at
            ))
    
    # Sort by final score (descending)
    candidate_summaries.sort(key=lambda x: x.final_score, reverse=True)
    
    return candidate_summaries

@router.get("/candidates/{candidate_id}/interview/{interview_id}")
async def get_candidate_interview_details(candidate_id: str, interview_id: str,
                                    current_user: models.User = Depends(get_current_user)):
    """Get detailed interview information for a candidate (HR only)"""
    if current_user.role != "hr":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can access candidate details"
        )
    
    if not ObjectId.is_valid(interview_id) or not ObjectId.is_valid(candidate_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID"
        )
    
    interview = await models.Interview.find_one(
        models.Interview.id == ObjectId(interview_id),
        models.Interview.candidate_id == ObjectId(candidate_id)
    )
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    candidate = await models.User.get(ObjectId(candidate_id))
    job_role = await models.JobRole.get(interview.job_role_id)
    questions = await models.Question.find(
        models.Question.interview_id == ObjectId(interview_id)
    ).sort("+question_number").to_list()
    
    responses = await models.InterviewResponse.find(
        models.InterviewResponse.interview_id == ObjectId(interview_id)
    ).to_list()
    
    # Build response map
    response_map = {str(r.question_id): r for r in responses}
    
    # Build detailed response
    detailed_questions = []
    for question in questions:
        response = response_map.get(str(question.id))
        detailed_questions.append({
            "question_id": str(question.id),
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
            "id": str(candidate.id),
            "username": candidate.username,
            "email": candidate.email
        },
        "job_role": job_role.title if job_role else None,
        "interview": {
            "id": str(interview.id),
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
async def get_dashboard_statistics(current_user: models.User = Depends(get_current_user)):
    """Get dashboard statistics (HR only)"""
    if current_user.role != "hr":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can access statistics"
        )
    
    total_interviews = await models.Interview.find_all().count()
    completed_interviews = await models.Interview.find(
        models.Interview.status == "completed"
    ).count()
    in_progress_interviews = await models.Interview.find(
        models.Interview.status == "in_progress"
    ).count()
    total_candidates = await models.User.find(
        models.User.role == "candidate"
    ).count()
    total_roles = await models.JobRole.find_all().count()
    
    # Calculate average final score
    completed = await models.Interview.find(
        models.Interview.status == "completed"
    ).to_list()
    avg_score = sum(i.final_score for i in completed) / len(completed) if completed else 0
    
    return {
        "total_interviews": total_interviews,
        "completed_interviews": completed_interviews,
        "in_progress_interviews": in_progress_interviews,
        "total_candidates": total_candidates,
        "total_job_roles": total_roles,
        "average_final_score": round(avg_score, 2) if completed else 0
    }
