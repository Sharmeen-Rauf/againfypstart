"""
Script to seed initial data into the database
Run this after starting the server for the first time
"""
import asyncio
from app.database import init_db
from app.models import User, JobRole
from app.auth import get_password_hash

async def seed():
    # Initialize database
    await init_db()
    
    # Create default HR user
    hr_user = await User.find_one(User.username == "hr_admin")
    if not hr_user:
        hr_user = User(
            email="hr@botboss.com",
            username="hr_admin",
            hashed_password=get_password_hash("admin123"),
            role="hr"
        )
        await hr_user.insert()
        print("Created HR admin user: hr_admin / admin123")
    
    # Create default candidate user
    candidate_user = await User.find_one(User.username == "test_candidate")
    if not candidate_user:
        candidate_user = User(
            email="candidate@test.com",
            username="test_candidate",
            hashed_password=get_password_hash("test123"),
            role="candidate"
        )
        await candidate_user.insert()
        print("Created test candidate: test_candidate / test123")
    
    # Create default job roles
    roles_data = [
        {"title": "Python Developer", "description": "Backend developer specializing in Python"},
        {"title": "Web Developer", "description": "Full-stack web developer"},
        {"title": "Data Scientist", "description": "Data analyst and machine learning engineer"},
        {"title": "Software Engineer", "description": "General software engineering role"},
    ]
    
    for role_data in roles_data:
        existing_role = await JobRole.find_one(JobRole.title == role_data["title"])
        if not existing_role:
            role = JobRole(**role_data)
            await role.insert()
            print(f"Created job role: {role_data['title']}")
    
    print("\n✅ Seed data created successfully!")
    print("\nDefault credentials:")
    print("HR Admin: hr_admin / admin123")
    print("Test Candidate: test_candidate / test123")

if __name__ == "__main__":
    asyncio.run(seed())
