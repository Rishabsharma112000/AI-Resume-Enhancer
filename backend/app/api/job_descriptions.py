"""Job Description routes"""

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.job_description import JobDescriptionCreate, JobDescriptionResponse, JobDescriptionDetailResponse
from app.services.job_description_service import JobDescriptionService

router = APIRouter(prefix="/job-descriptions", tags=["Job Descriptions"])


@router.post("/", response_model=JobDescriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_job_description(
    job_description: JobDescriptionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a job description"""
    jd = JobDescriptionService.create_job_description(db, current_user.id, job_description)
    return jd


@router.post("/upload", response_model=JobDescriptionResponse, status_code=status.HTTP_201_CREATED)
async def upload_job_description(
    file: UploadFile = File(...),
    title: str = "",
    company: str = "",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a job description"""
    if not title:
        title = file.filename or "Job Description"
    
    jd = JobDescriptionService.upload_job_description(db, current_user.id, file, title, company)
    return jd


@router.get("/", response_model=list[JobDescriptionResponse])
async def list_job_descriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all job descriptions for current user"""
    job_descriptions = JobDescriptionService.get_user_job_descriptions(db, current_user.id)
    return job_descriptions


@router.get("/{jd_id}", response_model=JobDescriptionDetailResponse)
async def get_job_description(
    jd_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get job description details"""
    job_description = JobDescriptionService.get_job_description_by_id(db, jd_id, current_user.id)
    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job description not found"
        )
    return job_description


@router.delete("/{jd_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job_description(
    jd_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a job description"""
    JobDescriptionService.delete_job_description(db, jd_id, current_user.id)
    return None
