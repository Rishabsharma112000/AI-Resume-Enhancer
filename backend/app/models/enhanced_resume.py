"""Enhanced Resume model"""

from sqlalchemy import Column, Integer, ForeignKey, Text, String
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class EnhancedResume(Base, TimestampMixin):
    """Enhanced Resume model"""

    __tablename__ = "enhanced_resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    analysis_id = Column(Integer, ForeignKey("resume_analyses.id"), nullable=True)
    
    # Enhanced content
    enhanced_summary = Column(Text, nullable=True)
    enhanced_experience = Column(Text, nullable=True)
    enhanced_full_content = Column(Text, nullable=True)
    improvements_made = Column(Text, nullable=True)
    estimated_ats_score_gain = Column(Integer, nullable=True)

    # Metadata
    version = Column(Integer, default=1, nullable=False)

    # Relationships
    user = relationship("User", back_populates="enhanced_resumes")
    resume = relationship("Resume", back_populates="enhanced_resumes")

    def __repr__(self):
        return f"<EnhancedResume(id={self.id}, resume_id={self.resume_id}, version={self.version})>"
