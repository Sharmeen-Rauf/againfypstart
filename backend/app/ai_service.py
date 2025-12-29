import os
from openai import OpenAI
from typing import List, Dict
import json
import re

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here"))

# Role-based question templates
ROLE_QUESTIONS = {
    "python_developer": [
        "What is your experience with Python? Describe a challenging project you've worked on.",
        "Explain the difference between lists and tuples in Python. When would you use each?",
        "How do you handle errors in Python? Walk me through your approach to exception handling.",
        "Describe a time when you had to optimize code for performance. What was your approach?",
        "What Python libraries or frameworks are you most comfortable with, and why?"
    ],
    "web_developer": [
        "What is your experience with frontend and backend development?",
        "Explain the difference between REST and GraphQL. When would you use each?",
        "How do you ensure your web applications are secure? What security practices do you follow?",
        "Describe your experience with version control systems like Git.",
        "How do you approach responsive design? What are your best practices?"
    ],
    "data_scientist": [
        "What is your experience with data analysis and machine learning?",
        "Explain the difference between supervised and unsupervised learning.",
        "How do you handle missing data in a dataset?",
        "Describe your experience with data visualization tools.",
        "What metrics do you use to evaluate the performance of a machine learning model?"
    ],
    "general": [
        "Tell me about yourself and why you're interested in this position.",
        "What are your greatest strengths and how do they relate to this role?",
        "Describe a challenging project you worked on and how you overcame obstacles.",
        "How do you handle working under pressure or tight deadlines?",
        "Where do you see yourself in the next 5 years?"
    ]
}

def generate_role_questions(job_role: str, num_questions: int = 5) -> List[str]:
    """Generate interview questions based on job role"""
    # Normalize job role name
    role_key = job_role.lower().replace(" ", "_")
    
    # Check if we have predefined questions for this role
    if role_key in ROLE_QUESTIONS:
        questions = ROLE_QUESTIONS[role_key]
    else:
        # Try to match partial role names
        questions = None
        for key in ROLE_QUESTIONS:
            if key in role_key or role_key in key:
                questions = ROLE_QUESTIONS[key]
                break
        
        if not questions:
            questions = ROLE_QUESTIONS["general"]
    
    # Return requested number of questions
    return questions[:num_questions]

def evaluate_response(question: str, response: str) -> Dict[str, float]:
    """Evaluate candidate response using OpenAI"""
    
    try:
        prompt = f"""You are an expert interviewer evaluating a candidate's response. 

Question: {question}
Candidate Response: {response}

Evaluate the response on the following criteria (0-10 scale):
1. Technical Accuracy/Knowledge: How technically correct and knowledgeable is the response?
2. Clarity: How clear and well-structured is the response?
3. Relevance: How relevant is the response to the question asked?
4. Sentiment/Confidence: How confident and positive does the response sound? (Consider tone, confidence level)

Return ONLY a JSON object in this exact format:
{{
    "technical_score": <number between 0-10>,
    "clarity_score": <number between 0-10>,
    "relevance_score": <number between 0-10>,
    "sentiment_score": <number between 0-10>
}}

Be objective and provide accurate scores based on the response quality."""

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert interviewer. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        response_text = completion.choices[0].message.content.strip()
        
        # Extract JSON from response (in case there's extra text)
        json_match = re.search(r'\{[^}]+\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(0)
        
        evaluation = json.loads(response_text)
        
        # Validate and normalize scores
        technical_score = max(0, min(10, float(evaluation.get("technical_score", 5))))
        clarity_score = max(0, min(10, float(evaluation.get("clarity_score", 5))))
        relevance_score = max(0, min(10, float(evaluation.get("relevance_score", 5))))
        sentiment_score = max(0, min(10, float(evaluation.get("sentiment_score", 5))))
        
        return {
            "technical_score": round(technical_score, 2),
            "clarity_score": round(clarity_score, 2),
            "relevance_score": round(relevance_score, 2),
            "sentiment_score": round(sentiment_score, 2)
        }
    
    except Exception as e:
        print(f"Error in AI evaluation: {str(e)}")
        # Fallback to neutral scores if AI fails
        return {
            "technical_score": 5.0,
            "clarity_score": 5.0,
            "relevance_score": 5.0,
            "sentiment_score": 5.0
        }

def calculate_final_score(technical: float, clarity: float, relevance: float, sentiment: float) -> float:
    """Calculate final score using weighted formula"""
    # Weighted formula: Technical (40%), Clarity (20%), Relevance (20%), Sentiment (20%)
    final = (technical * 0.4) + (clarity * 0.2) + (relevance * 0.2) + (sentiment * 0.2)
    return round(final, 2)

