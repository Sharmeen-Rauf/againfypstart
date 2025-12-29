from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from app import models, schemas
from app.auth import get_current_user
from app.ai_service import generate_role_questions, evaluate_response, calculate_final_score
from bson import ObjectId

router = APIRouter()

@router.post("/start", response_model=schemas.InterviewResponse)
async def start_interview(interview_data: schemas.InterviewCreate,
                    current_user: models.User = Depends(get_current_user)):
    """Start a new interview"""
    if current_user.role != "candidate":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can start interviews"
        )
    
    # Verify job role exists
    if not ObjectId.is_valid(interview_data.job_role_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid job role ID"
        )
    
    job_role = await models.JobRole.get(ObjectId(interview_data.job_role_id))
    if not job_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job role not found"
        )
    
    # Check if candidate has an in-progress interview
    existing_interview = await models.Interview.find_one(
        models.Interview.candidate_id == current_user.id,
        models.Interview.status == "in_progress"
    )
    
    if existing_interview:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an interview in progress"
        )
    
    # Create interview
    db_interview = models.Interview(
        candidate_id=current_user.id,
        job_role_id=ObjectId(interview_data.job_role_id),
        status="in_progress"
    )
    await db_interview.insert()
    
    # Generate questions for this role
    questions_text = generate_role_questions(job_role.title, num_questions=5)
    
    # Create question records
    for idx, question_text in enumerate(questions_text, 1):
        db_question = models.Question(
            interview_id=db_interview.id,
            question_text=question_text,
            question_number=idx
        )
        await db_question.insert()
    
    return db_interview

@router.get("/current", response_model=schemas.InterviewResponse)
async def get_current_interview(current_user: models.User = Depends(get_current_user)):
    """Get current in-progress interview for candidate"""
    if current_user.role != "candidate":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can access their interviews"
        )
    
    interview = await models.Interview.find_one(
        models.Interview.candidate_id == current_user.id,
        models.Interview.status == "in_progress"
    )
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No interview in progress"
        )
    
    return interview

@router.get("/{interview_id}/questions", response_model=List[schemas.QuestionResponse])
async def get_interview_questions(interview_id: str,
                            current_user: models.User = Depends(get_current_user)):
    """Get all questions for an interview"""
    if not ObjectId.is_valid(interview_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid interview ID"
        )
    
    interview = await models.Interview.get(ObjectId(interview_id))
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
    
    questions = await models.Question.find(
        models.Question.interview_id == ObjectId(interview_id)
    ).sort("+question_number").to_list()
    
    return questions

@router.post("/{interview_id}/respond")
async def submit_response(interview_id: str, response_data: schemas.ResponseCreate,
                    current_user: models.User = Depends(get_current_user)):
    """Submit response to a question"""
    if current_user.role != "candidate":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can submit responses"
        )
    
    if not ObjectId.is_valid(interview_id) or not ObjectId.is_valid(response_data.question_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ID"
        )
    
    # Verify interview exists and belongs to candidate
    interview = await models.Interview.get(ObjectId(interview_id))
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
    question = await models.Question.find_one(
        models.Question.id == ObjectId(response_data.question_id),
        models.Question.interview_id == ObjectId(interview_id)
    )
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Check if response already exists
    existing_response = await models.InterviewResponse.find_one(
        models.InterviewResponse.question_id == ObjectId(response_data.question_id)
    )
    
    if existing_response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Response already submitted for this question"
        )
    
    # Evaluate response using AI
    evaluation = evaluate_response(question.question_text, response_data.response_text)
    
    # Create response record
    db_response = models.InterviewResponse(
        interview_id=ObjectId(interview_id),
        question_id=ObjectId(response_data.question_id),
        response_text=response_data.response_text,
        technical_score=evaluation["technical_score"],
        clarity_score=evaluation["clarity_score"],
        relevance_score=evaluation["relevance_score"],
        sentiment_score=evaluation["sentiment_score"]
    )
    
    await db_response.insert()
    
    return {
        "message": "Response submitted successfully",
        "response_id": str(db_response.id),
        "scores": {
            "technical_score": evaluation["technical_score"],
            "clarity_score": evaluation["clarity_score"],
            "relevance_score": evaluation["relevance_score"],
            "sentiment_score": evaluation["sentiment_score"]
        }
    }

@router.post("/{interview_id}/complete")
async def complete_interview(interview_id: str,
                       current_user: models.User = Depends(get_current_user)):
    """Complete an interview and calculate final scores"""
    if current_user.role != "candidate":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can complete interviews"
        )
    
    if not ObjectId.is_valid(interview_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid interview ID"
        )
    
    interview = await models.Interview.get(ObjectId(interview_id))
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
    responses = await models.InterviewResponse.find(
        models.InterviewResponse.interview_id == ObjectId(interview_id)
    ).to_list()
    
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
    
    await interview.save()
    
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
async def get_interview_responses(interview_id: str,
                            current_user: models.User = Depends(get_current_user)):
    """Get all responses for an interview"""
    if not ObjectId.is_valid(interview_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid interview ID"
        )
    
    interview = await models.Interview.get(ObjectId(interview_id))
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
    
    responses = await models.InterviewResponse.find(
        models.InterviewResponse.interview_id == ObjectId(interview_id)
    ).to_list()
    
    return responses
