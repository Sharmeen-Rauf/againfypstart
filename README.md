# Botboss - AI Interview Platform

An AI-driven interview platform that automates candidate shortlisting using NLP and sentiment analysis.

## Features (MVP)

✅ Text-based AI interview (no video initially)  
✅ Role-based questions  
✅ AI response evaluation  
✅ Scoring system  
✅ HR dashboard (basic)  

## Tech Stack

- **Frontend**: ReactJS with Vite
- **Backend**: Python FastAPI
- **AI/NLP**: OpenAI API (GPT-3.5-turbo)
- **Database**: MongoDB (with Beanie ODM)
- **Hosting**: Vercel (Frontend) + Railway/Render (Backend)

## Project Structure

```
againfypstart/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── ai_service.py
│   │   └── routers/
│   ├── requirements.txt
│   ├── seed_data.py
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   └── App.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── vercel.json
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```env
MONGODB_URL=mongodb+srv://f90396245_db_user:resturentwebsitenew@cluster0.94frwr3.mongodb.net/?appName=Cluster0
DATABASE_NAME=botboss
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=your-secret-key-for-jwt-tokens
```

4. Run seed data (creates default users and roles):
```bash
python seed_data.py
```

5. Start the server:
```bash
uvicorn app.main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file (optional, defaults to localhost):
```
VITE_API_URL=http://localhost:8000
```

4. Start development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Default Credentials

After running `seed_data.py`, you can use:

- **HR Admin**: 
  - Username: `hr_admin`
  - Password: `admin123`

- **Test Candidate**: 
  - Username: `test_candidate`
  - Password: `test123`

## Deployment

### Frontend (Vercel)

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variable: `VITE_API_URL` to your backend URL
4. Deploy

### Backend (Railway/Render)

1. Push code to GitHub
2. Connect repository to Railway/Render
3. Set environment variables:
   - `MONGODB_URL` - Your MongoDB connection string
   - `DATABASE_NAME` - Database name (default: botboss)
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `SECRET_KEY` - JWT secret key
4. Deploy

## API Documentation

Once backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Scoring Formula

Final Score = (Technical × 0.4) + (Clarity × 0.2) + (Relevance × 0.2) + (Sentiment × 0.2)

## Notes

- Make sure to add your MongoDB connection string and OpenAI API key in the backend `.env` file
- Change the SECRET_KEY in production
- **Never commit the `.env` file to Git** (it contains sensitive credentials)
- The database will be created automatically when you first run the application
- See `backend/MONGODB_SETUP.md` for detailed MongoDB setup instructions

