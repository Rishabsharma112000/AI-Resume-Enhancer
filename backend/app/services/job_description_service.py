"""Job Description service"""

import os
from sqlalchemy.orm import Session
from app.models.job_description import JobDescription
from app.schemas.job_description import JobDescriptionCreate
from app.utils.file_handler import extract_text_from_file
from fastapi import HTTPException, status, UploadFile
from app.core.config import settings


class JobDescriptionService:
    """Job Description service class"""

    @staticmethod
    def create_job_description(
        db: Session, user_id: int, job_description: JobDescriptionCreate
    ) -> JobDescription:
        """Create a job description"""
        db_job_desc = JobDescription(
            user_id=user_id,
            title=job_description.title,
            company=job_description.company,
            content=job_description.content,
        )
        db.add(db_job_desc)
        db.commit()
        db.refresh(db_job_desc)
        return db_job_desc

    @staticmethod
    def upload_job_description(db: Session, user_id: int, file: UploadFile, title: str, company: str = None) -> JobDescription:
        """Upload a job description file"""
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename",
            )

        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed",
            )

        file_content = file.file.read()
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds maximum allowed size",
            )

        # Extract text
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name

        try:
            content = extract_text_from_file(tmp_path, file_extension)
        finally:
            os.remove(tmp_path)

        # Create job description
        db_job_desc = JobDescription(
            user_id=user_id,
            title=title,
            company=company,
            content=content,
            file_name=file.filename,
        )
        db.add(db_job_desc)
        db.commit()
        db.refresh(db_job_desc)
        return db_job_desc

    @staticmethod
    def get_job_description_by_id(db: Session, jd_id: int, user_id: int) -> JobDescription:
        """Get job description by ID"""
        return db.query(JobDescription).filter(
            JobDescription.id == jd_id,
            JobDescription.user_id == user_id
        ).first()

    @staticmethod
    def get_user_job_descriptions(db: Session, user_id: int) -> list:
        """Get all job descriptions for a user"""
        return db.query(JobDescription).filter(
            JobDescription.user_id == user_id,
            JobDescription.is_active == 1
        ).all()

    @staticmethod
    def delete_job_description(db: Session, jd_id: int, user_id: int) -> bool:
        """Delete a job description"""
        job_desc = JobDescriptionService.get_job_description_by_id(db, jd_id, user_id)
        if not job_desc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job description not found",
            )

        job_desc.is_active = 0
        db.commit()
        return True
