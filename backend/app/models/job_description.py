"""Job Description model"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin


class JobDescription(Base, TimestampMixin):
    """Job Description model"""

    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    file_name = Column(String(255), nullable=True)
    is_active = Column(Integer, default=1, nullable=False)

    # Relationships
    user = relationship("User", back_populates="job_descriptions")
    analyses = relationship("ResumeAnalysis", back_populates="job_description")

    def __repr__(self):
        return f"<JobDescription(id={self.id}, title={self.title}, company={self.company})>"
