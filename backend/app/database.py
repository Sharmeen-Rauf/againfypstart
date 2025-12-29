from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection URL from environment variable
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/botboss")

# Database name
DATABASE_NAME = os.getenv("DATABASE_NAME", "botboss")

client = None
database = None
initialized = False

async def init_db():
    """Initialize MongoDB connection and Beanie"""
    global client, database, initialized
    
    # In serverless, we initialize on each cold start
    # Connection pooling is handled by Motor/AsyncIOMotorClient
    try:
        if initialized and client:
            return database
    except:
        pass
    
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    
    # Import models here to avoid circular imports
    from app.models import User, JobRole, Interview, Question, InterviewResponse
    
    # Initialize Beanie with models
    await init_beanie(
        database=database,
        document_models=[User, JobRole, Interview, Question, InterviewResponse]
    )
    
    initialized = True
    return database

async def close_db():
    """Close MongoDB connection"""
    global client, initialized
    # In serverless environments like Vercel, connections are managed per invocation
    # We don't need to close them as they're cleaned up automatically
    pass
