"""Resume Analysis model"""

from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class ResumeAnalysis(Base, TimestampMixin):
    """Resume Analysis model"""

    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=True)
    
    # Analysis scores
    ats_score = Column(Float, nullable=True)
    keyword_match_score = Column(Float, nullable=True)
    
    # Analysis data (JSON)
    missing_skills = Column(JSON, nullable=True)
    missing_keywords = Column(JSON, nullable=True)
    strengths = Column(JSON, nullable=True)
    weaknesses = Column(JSON, nullable=True)
    
    # Raw analysis output
    analysis_output = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="analyses")
    resume = relationship("Resume", back_populates="analyses")
    job_description = relationship("JobDescription", back_populates="analyses")

    def __repr__(self):
        return f"<ResumeAnalysis(id={self.id}, resume_id={self.resume_id}, ats_score={self.ats_score})>"
