"""User schemas"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)


class UserCreate(UserBase):
    """User creation schema"""

    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """User login schema"""

    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """User update schema"""

    full_name: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    """User response schema"""

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema"""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
