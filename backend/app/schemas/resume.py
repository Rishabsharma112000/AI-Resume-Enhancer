"""Resume schemas"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ResumeBase(BaseModel):
    """Base resume schema"""

    original_filename: str


class ResumeCreate(ResumeBase):
    """Resume creation schema"""

    pass


class ResumeResponse(ResumeBase):
    """Resume response schema"""

    id: int
    user_id: int
    filename: str
    file_type: str
    file_size: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResumeDetailResponse(ResumeResponse):
    """Resume detail response schema"""

    raw_text: Optional[str] = None
