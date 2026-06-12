"""Resume service"""

import os
from sqlalchemy.orm import Session
from app.models.resume import Resume
from app.schemas.resume import ResumeCreate
from app.utils.file_handler import extract_text_from_file
from fastapi import HTTPException, status, UploadFile
from app.core.config import settings


class ResumeService:
    """Resume service class"""

    @staticmethod
    def upload_resume(db: Session, user_id: int, file: UploadFile) -> Resume:
        """Upload a resume file"""
        # Validate file
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename",
            )

        # Check file extension
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}",
            )

        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

        # Save file
        file_content = file.file.read()
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds maximum allowed size",
            )

        # Generate unique filename
        import uuid
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as f:
            f.write(file_content)

        # Extract text from file
        try:
            raw_text = extract_text_from_file(file_path, file_extension)
        except Exception as e:
            os.remove(file_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process file: {str(e)}",
            )

        # Create resume record
        db_resume = Resume(
            user_id=user_id,
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_type=file_extension,
            file_size=len(file_content),
            raw_text=raw_text,
        )
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)

        return db_resume

    @staticmethod
    def get_resume_by_id(db: Session, resume_id: int, user_id: int) -> Resume:
        """Get resume by ID"""
        return db.query(Resume).filter(
            Resume.id == resume_id,
            Resume.user_id == user_id
        ).first()

    @staticmethod
    def get_user_resumes(db: Session, user_id: int) -> list:
        """Get all resumes for a user"""
        return db.query(Resume).filter(
            Resume.user_id == user_id,
            Resume.is_active == 1
        ).all()

    @staticmethod
    def delete_resume(db: Session, resume_id: int, user_id: int) -> bool:
        """Delete a resume"""
        resume = ResumeService.get_resume_by_id(db, resume_id, user_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found",
            )

        # Delete file
        try:
            if os.path.exists(resume.file_path):
                os.remove(resume.file_path)
        except Exception:
            pass

        # Mark as inactive
        resume.is_active = 0
        db.commit()
        return True
