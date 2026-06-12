"""User model"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    job_descriptions = relationship(
        "JobDescription", back_populates="user", cascade="all, delete-orphan"
    )
    analyses = relationship(
        "ResumeAnalysis", back_populates="user", cascade="all, delete-orphan"
    )
    enhanced_resumes = relationship(
        "EnhancedResume", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, full_name={self.full_name})>"
