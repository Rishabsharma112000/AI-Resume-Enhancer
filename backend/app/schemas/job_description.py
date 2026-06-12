"""Job Description schemas"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class JobDescriptionBase(BaseModel):
    """Base job description schema"""

    title: str = Field(..., min_length=1, max_length=255)
    company: Optional[str] = None
    content: str = Field(..., min_length=1)


class JobDescriptionCreate(JobDescriptionBase):
    """Job description creation schema"""

    pass


class JobDescriptionResponse(JobDescriptionBase):
    """Job description response schema"""

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobDescriptionDetailResponse(JobDescriptionResponse):
    """Job description detail response schema"""

    file_name: Optional[str] = None
