# Botboss Backend API

## Setup Instructions

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Set Environment Variables**
Create a `.env` file in the backend directory:
```env
MONGODB_URL=mongodb+srv://f90396245_db_user:resturentwebsitenew@cluster0.94frwr3.mongodb.net/?appName=Cluster0
DATABASE_NAME=botboss
SECRET_KEY=your-secret-key-for-jwt-tokens
OPENAI_API_KEY=your-openai-api-key-here
```

**⚠️ IMPORTANT:** 
- Never commit the `.env` file to Git
- The password is stored securely in `.env` (not hardcoded)
- Change the password if your repository is public

3. **Run Seed Data** (creates default users and roles):
```bash
python seed_data.py
```

4. **Run the Server**:
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

The application uses **MongoDB** with Beanie ODM.

- Database connection is configured via `MONGODB_URL` environment variable
- Database name is set via `DATABASE_NAME` environment variable
- Collections are created automatically when first used

## Default Credentials

After running `seed_data.py`, you can use:

- **HR Admin**: 
  - Username: `hr_admin`
  - Password: `admin123`

- **Test Candidate**: 
  - Username: `test_candidate`
  - Password: `test123`

## Notes

- Make sure to add your OpenAI API key in the `.env` file
- Change the SECRET_KEY in production
- The MongoDB connection string with password should be in `.env` file (never commit it)
