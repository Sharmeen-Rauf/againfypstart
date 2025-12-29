from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas.JobRoleResponse])
def get_all_roles(db: Session = Depends(get_db)):
    """Get all available job roles"""
    roles = db.query(models.JobRole).all()
    return roles

@router.post("/", response_model=schemas.JobRoleResponse)
def create_role(role_data: schemas.JobRoleCreate, db: Session = Depends(get_db), 
                current_user: models.User = Depends(get_current_user)):
    """Create a new job role (HR only)"""
    if current_user.role != "hr":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can create job roles"
        )
    
    # Check if role already exists
    existing_role = db.query(models.JobRole).filter(models.JobRole.title == role_data.title).first()
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job role with this title already exists"
        )
    
    db_role = models.JobRole(**role_data.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    
    return db_role

@router.get("/{role_id}", response_model=schemas.JobRoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """Get a specific job role by ID"""
    role = db.query(models.JobRole).filter(models.JobRole.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job role not found"
        )
    return role

