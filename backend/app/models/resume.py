"""Resume model"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class Resume(Base, TimestampMixin):
    """Resume model"""

    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(10), nullable=False)  # pdf, docx, doc
    file_size = Column(Integer, nullable=False)
    raw_text = Column(Text, nullable=True)
    is_active = Column(Integer, default=1, nullable=False)

    # Relationships
    user = relationship("User", back_populates="resumes")
    analyses = relationship("ResumeAnalysis", back_populates="resume", cascade="all, delete-orphan")
    enhanced_resumes = relationship(
        "EnhancedResume", back_populates="resume", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Resume(id={self.id}, user_id={self.user_id}, filename={self.filename})>"
