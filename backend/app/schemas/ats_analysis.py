"""ATS analysis schemas"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal


ImpactLevel = Literal["High", "Medium", "Low"]
RoadmapCategory = Literal["Critical Fixes", "Recommended Improvements", "Optional Enhancements"]


class SectionFeedback(BaseModel):
    """Feedback for a single resume section"""

    section_name: str
    score: float = Field(ge=0, le=100)
    assessment: str
    issues: List[str] = []
    missing_information: List[str] = []
    recommendations: List[str] = []
    ats_impact: ImpactLevel = "Medium"
    example_improvement: Optional[str] = None


class KeywordAnalysis(BaseModel):
    """Keyword extraction and job match analysis"""

    extracted_keywords: List[str] = []
    matched_keywords: List[str] = []
    missing_keywords: List[str] = []
    keyword_gaps: List[str] = []
    keyword_match_score: float = 0.0
    recommendations: List[str] = []


class FormattingIssue(BaseModel):
    """ATS formatting/parsing issue"""

    issue: str
    description: str
    ats_impact: ImpactLevel = "Medium"
    recommendation: str


class ImprovementSuggestion(BaseModel):
    """Targeted content improvement suggestion"""

    area: str
    current_state: str
    suggestion: str
    example: Optional[str] = None
    ats_impact: ImpactLevel = "Medium"


class RoadmapItem(BaseModel):
    """Prioritized improvement roadmap item"""

    title: str
    description: str
    category: RoadmapCategory
    estimated_score_gain: float = Field(ge=0, le=100)
    priority: int = Field(ge=1)


class ATSAnalysisReport(BaseModel):
    """Complete ATS analysis report"""

    overall_ats_score: float = Field(ge=0, le=100)
    category_scores: Dict[str, float] = {}
    section_feedback: List[SectionFeedback] = []
    keyword_analysis: KeywordAnalysis = Field(default_factory=KeywordAnalysis)
    formatting_issues: List[FormattingIssue] = []
    improvement_suggestions: List[ImprovementSuggestion] = []
    strengths: List[str] = []
    weaknesses: List[str] = []
    roadmap: List[RoadmapItem] = []
