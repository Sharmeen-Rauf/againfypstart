# Botboss Backend API

## Setup Instructions

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Set Environment Variables**
Create a `.env` file in the backend directory:
```
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=your-secret-key-for-jwt-tokens
```

3. **Run the Server**
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user (HR or Candidate)
- `POST /api/auth/login` - Login and get access token
- `GET /api/auth/me` - Get current user info

### Job Roles
- `GET /api/roles/` - Get all job roles
- `POST /api/roles/` - Create a new job role (HR only)
- `GET /api/roles/{role_id}` - Get specific job role

### Interviews
- `POST /api/interviews/start` - Start a new interview (Candidate)
- `GET /api/interviews/current` - Get current interview (Candidate)
- `GET /api/interviews/{interview_id}/questions` - Get interview questions
- `POST /api/interviews/{interview_id}/respond` - Submit response to a question
- `POST /api/interviews/{interview_id}/complete` - Complete interview
- `GET /api/interviews/{interview_id}/responses` - Get all responses

### Dashboard
- `GET /api/dashboard/candidates` - Get all candidates with scores (HR)
- `GET /api/dashboard/candidates/{candidate_id}/interview/{interview_id}` - Get detailed interview info
- `GET /api/dashboard/statistics` - Get dashboard statistics

## Database

The application uses SQLite by default. The database file `botboss.db` will be created automatically on first run.

## Notes

- Make sure to add your OpenAI API key in the `.env` file
- Change the SECRET_KEY in production
- The database will be created automatically when you first run the application

