# Vercel serverless entry point
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangum import Mangum
from app.main import app

# Wrap FastAPI app with Mangum for serverless compatibility
handler = Mangum(app, lifespan="off")  # lifespan handled in FastAPI app
