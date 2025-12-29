from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app import models, schemas
from app.auth import get_current_user
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[schemas.JobRoleResponse])
async def get_all_roles():
    """Get all available job roles"""
    roles = await models.JobRole.find_all().to_list()
    return roles

@router.post("/", response_model=schemas.JobRoleResponse)
async def create_role(role_data: schemas.JobRoleCreate, current_user: models.User = Depends(get_current_user)):
    """Create a new job role (HR only)"""
    if current_user.role != "hr":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can create job roles"
        )
    
    # Check if role already exists
    existing_role = await models.JobRole.find_one(models.JobRole.title == role_data.title)
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job role with this title already exists"
        )
    
    db_role = models.JobRole(**role_data.dict())
    await db_role.insert()
    return db_role

@router.get("/{role_id}", response_model=schemas.JobRoleResponse)
async def get_role(role_id: str):
    """Get a specific job role by ID"""
    if not ObjectId.is_valid(role_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role ID"
        )
    
    role = await models.JobRole.get(ObjectId(role_id))
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job role not found"
        )
    return role
