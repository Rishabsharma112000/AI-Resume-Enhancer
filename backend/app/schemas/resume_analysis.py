"""Resume Analysis schemas"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.schemas.ats_analysis import ATSAnalysisReport


class AnalysisData(BaseModel):
    """Analysis data schema"""

    missing_skills: Optional[List[str]] = None
    missing_keywords: Optional[List[str]] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None


class ResumeAnalysisCreate(BaseModel):
    """Resume analysis creation schema"""

    resume_id: int
    job_description_id: Optional[int] = None


class ResumeAnalysisResponse(BaseModel):
    """Resume analysis response schema"""

    id: int
    user_id: int
    resume_id: int
    job_description_id: Optional[int] = None
    ats_score: Optional[float] = None
    keyword_match_score: Optional[float] = None
    missing_skills: Optional[List[str]] = None
    missing_keywords: Optional[List[str]] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    ats_report: Optional[ATSAnalysisReport] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
