"""Enhanced Resume schemas"""

from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class EnhanceResumeRequest(BaseModel):
    """Request to enhance a resume from analysis"""

    analysis_id: int


class ImprovementChange(BaseModel):
    """Before/after improvement record"""

    section: str
    change: str
    before: Optional[str] = None
    after: Optional[str] = None


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
    enhanced_full_content: Optional[str] = None
    improvements_made: Optional[List[Any]] = None
    estimated_ats_score_gain: Optional[float] = None
    original_content: Optional[str] = None
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EnhancedResumeDetailResponse(EnhancedResumeResponse):
    """Enhanced resume detail response schema"""

    pass
