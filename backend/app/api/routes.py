"""API routes"""

from fastapi import APIRouter, Depends
from app.api import auth, users, resumes, job_descriptions, analysis

router = APIRouter(prefix="/api/v1")

# Include routers
router.include_router(auth.router, tags=["Authentication"])
router.include_router(users.router, tags=["Users"])
router.include_router(resumes.router, tags=["Resumes"])
router.include_router(job_descriptions.router, tags=["Job Descriptions"])
router.include_router(analysis.router, tags=["Analysis"])
