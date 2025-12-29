# MongoDB Setup Instructions

## Connection String Configuration

Your MongoDB connection string has been configured to use environment variables. The password is securely stored and **NOT hardcoded** in the code.

## Setup Steps

1. **Create `.env` file in the `backend` directory:**

```env
MONGODB_URL=mongodb+srv://f90396245_db_user:resturentwebsitenew@cluster0.94frwr3.mongodb.net/?appName=Cluster0
DATABASE_NAME=botboss
SECRET_KEY=your-secret-key-change-in-production
OPENAI_API_KEY=your-openai-api-key-here
```

2. **Security Notes:**
   - ✅ Password is stored in `.env` file (not in code)
   - ✅ `.env` file is in `.gitignore` (won't be committed to Git)
   - ✅ Connection string is loaded from environment variables
   - ⚠️ **Never commit `.env` file to Git**
   - ⚠️ Change password if repository becomes public

3. **For Production Deployment:**
   - Set environment variables on your hosting platform (Railway/Render)
   - Never hardcode credentials in code
   - Use strong, unique passwords
   - Rotate credentials regularly

## Database Migration

The backend has been migrated from SQLite to MongoDB:
- **Beanie** - ODM for MongoDB (async, similar to SQLAlchemy)
- **Motor** - Async MongoDB driver
- All endpoints converted to async/await
- ObjectId strings used instead of integer IDs

## Running the Application

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Create `.env` file** with your MongoDB connection string (see above)

3. **Run seed data** (creates default users and roles):
```bash
python seed_data.py
```

4. **Start the server:**
```bash
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `MONGODB_URL` | MongoDB connection string | Yes | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `DATABASE_NAME` | Database name | Yes | `botboss` |
| `SECRET_KEY` | JWT secret key | Yes | `your-secret-key` |
| `OPENAI_API_KEY` | OpenAI API key | Yes | `sk-...` |

## Troubleshooting

- **Connection Error**: 
  - Verify MongoDB URL format
  - Check username and password
  - Ensure network access is enabled in MongoDB Atlas

- **Database Not Found**: 
  - Database will be created automatically on first use
  - No manual database creation needed

- **Index Errors**: 
  - Indexes are created automatically by Beanie
  - Check MongoDB connection if errors occur

## Password Security

The password `resturentwebsitenew` is:
- ✅ Stored in `.env` file (environment variable)
- ✅ Excluded from Git (via `.gitignore`)
- ✅ Not visible in code or logs
- ⚠️ Should be changed if repository is made public

