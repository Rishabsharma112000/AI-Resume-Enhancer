"""Enhanced Resume schemas"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EnhancedResumeCreate(BaseModel):
    """Enhanced resume creation schema"""

    resume_id: int
    analysis_id: Optional[int] = None


class EnhancedResumeResponse(BaseModel):
    """Enhanced resume response schema"""

    id: int
    user_id: int
    resume_id: int
    analysis_id: Optional[int] = None
    enhanced_summary: Optional[str] = None
    enhanced_experience: Optional[str] = None
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EnhancedResumeDetailResponse(EnhancedResumeResponse):
    """Enhanced resume detail response schema"""

    enhanced_full_content: Optional[str] = None
