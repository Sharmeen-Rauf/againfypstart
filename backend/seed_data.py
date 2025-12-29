"""
Script to seed initial data into the database
Run this after starting the server for the first time
"""
from app.database import SessionLocal, engine
from app.models import Base, User, JobRole
from app.auth import get_password_hash

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Create default HR user
    hr_user = db.query(User).filter(User.username == "hr_admin").first()
    if not hr_user:
        hr_user = User(
            email="hr@botboss.com",
            username="hr_admin",
            hashed_password=get_password_hash("admin123"),
            role="hr"
        )
        db.add(hr_user)
        print("Created HR admin user: hr_admin / admin123")
    
    # Create default candidate user
    candidate_user = db.query(User).filter(User.username == "test_candidate").first()
    if not candidate_user:
        candidate_user = User(
            email="candidate@test.com",
            username="test_candidate",
            hashed_password=get_password_hash("test123"),
            role="candidate"
        )
        db.add(candidate_user)
        print("Created test candidate: test_candidate / test123")
    
    # Create default job roles
    roles_data = [
        {"title": "Python Developer", "description": "Backend developer specializing in Python"},
        {"title": "Web Developer", "description": "Full-stack web developer"},
        {"title": "Data Scientist", "description": "Data analyst and machine learning engineer"},
        {"title": "Software Engineer", "description": "General software engineering role"},
    ]
    
    for role_data in roles_data:
        existing_role = db.query(JobRole).filter(JobRole.title == role_data["title"]).first()
        if not existing_role:
            role = JobRole(**role_data)
            db.add(role)
            print(f"Created job role: {role_data['title']}")
    
    db.commit()
    print("\n✅ Seed data created successfully!")
    print("\nDefault credentials:")
    print("HR Admin: hr_admin / admin123")
    print("Test Candidate: test_candidate / test123")
    
except Exception as e:
    db.rollback()
    print(f"Error seeding data: {str(e)}")
finally:
    db.close()

