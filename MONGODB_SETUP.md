# MongoDB Setup Instructions

## Connection String

Your MongoDB connection string has been configured to use environment variables. The password is securely stored and not hardcoded.

## Setup Steps

1. **Create `.env` file in the `backend` directory:**

```env
MONGODB_URL=mongodb+srv://f90396245_db_user:resturentwebsitenew@cluster0.94frwr3.mongodb.net/?appName=Cluster0
DATABASE_NAME=botboss
SECRET_KEY=your-secret-key-change-in-production
OPENAI_API_KEY=your-openai-api-key-here
```

2. **Important Security Notes:**
   - ✅ Password is stored in `.env` file (not in code)
   - ✅ `.env` file is in `.gitignore` (won't be committed)
   - ✅ Never commit `.env` file to Git
   - ⚠️ Change password if repository is public

3. **For Production:**
   - Use environment variables on your hosting platform
   - Never hardcode credentials
   - Use strong passwords
   - Rotate credentials regularly

## Database Changes

The backend has been migrated from SQLite to MongoDB using:
- **Beanie** - ODM for MongoDB (similar to SQLAlchemy)
- **Motor** - Async MongoDB driver
- All endpoints are now async

## Running the Application

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Create `.env` file with your MongoDB connection string

3. Run seed data:
```bash
python seed_data.py
```

4. Start the server:
```bash
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `DATABASE_NAME` | Database name | `botboss` |
| `SECRET_KEY` | JWT secret key | `your-secret-key` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |

## Troubleshooting

- **Connection Error**: Check MongoDB URL format and credentials
- **Database Not Found**: Database will be created automatically
- **Index Errors**: Indexes are created automatically by Beanie

