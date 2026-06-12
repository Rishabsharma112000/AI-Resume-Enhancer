"""ATS analysis schemas"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal


ImpactLevel = Literal["High", "Medium", "Low"]
RoadmapCategory = Literal["Critical Fixes", "Recommended Improvements", "Optional Enhancements"]
PriorityLevel = Literal["Critical", "High", "Medium", "Low"]


class SectionFeedback(BaseModel):
    """Feedback for a single resume section"""

    section_name: str
    score: float = Field(ge=0, le=100)
    assessment: str
    issues: List[str] = []
    missing_information: List[str] = []
    recommendations: List[str] = []
    ats_impact: ImpactLevel = "Medium"
    why_it_affects_ats: Optional[str] = None
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
    why_it_affects_ats: Optional[str] = None


class ImprovementSuggestion(BaseModel):
    """Targeted content improvement suggestion"""

    area: str
    current_state: str
    suggestion: str
    example: Optional[str] = None
    ats_impact: ImpactLevel = "Medium"
    why_it_affects_ats: Optional[str] = None
    expected_improvement: Optional[str] = None


class RoadmapItem(BaseModel):
    """Prioritized improvement roadmap item"""

    title: str
    description: str
    category: RoadmapCategory
    estimated_score_gain: float = Field(ge=0, le=100)
    priority: int = Field(ge=1)


class CoachingInsight(BaseModel):
    """Detailed career coaching insight"""

    area: str
    what_is_wrong: str
    why_it_impacts_ats: str
    how_to_fix: str
    expected_improvement: str
    priority: PriorityLevel = "Medium"


class ActionVerbAnalysis(BaseModel):
    """Action verb usage analysis"""

    score: float = Field(ge=0, le=100, default=0)
    strong_verbs_found: List[str] = []
    weak_phrases_found: List[str] = []
    strong_verb_count: int = 0
    weak_phrase_count: int = 0
    assessment: str = ""
    issues: List[str] = []
    recommendations: List[str] = []
    why_it_affects_ats: str = (
        "ATS and recruiters scan for strong action verbs that signal ownership and impact. "
        "Passive language reduces keyword density and perceived seniority."
    )


class AchievementImpactAnalysis(BaseModel):
    """Achievement and impact quantification analysis"""

    score: float = Field(ge=0, le=100, default=0)
    quantified_bullets: int = 0
    total_bullets: int = 0
    unquantified_bullets: int = 0
    assessment: str = ""
    issues: List[str] = []
    recommendations: List[str] = []
    why_it_affects_ats: str = (
        "Quantified achievements improve both ATS keyword matching and recruiter ranking. "
        "Metrics demonstrate measurable impact that algorithms and humans reward."
    )


class SkillsGapAnalysis(BaseModel):
    """Skills gap analysis against job or industry standards"""

    score: float = Field(ge=0, le=100, default=0)
    present_skills: List[str] = []
    missing_skills: List[str] = []
    skill_gaps: List[str] = []
    assessment: str = ""
    issues: List[str] = []
    recommendations: List[str] = []
    why_it_affects_ats: str = (
        "ATS systems rank candidates by skill keyword overlap with job requirements. "
        "Missing skills reduce your match score and may filter you out before human review."
    )


class ReadabilityAnalysis(BaseModel):
    """Readability and professionalism analysis"""

    score: float = Field(ge=0, le=100, default=0)
    professionalism_score: float = Field(ge=0, le=100, default=0)
    assessment: str = ""
    issues: List[str] = []
    recommendations: List[str] = []
    why_it_affects_ats: str = (
        "Clear, professional language ensures ATS parsers extract the right entities "
        "and recruiters quickly understand your qualifications."
    )


class IndustryRelevanceAnalysis(BaseModel):
    """Industry relevance scoring"""

    score: float = Field(ge=0, le=100, default=0)
    relevant_keywords: List[str] = []
    industry_gaps: List[str] = []
    assessment: str = ""
    issues: List[str] = []
    recommendations: List[str] = []
    why_it_affects_ats: str = (
        "Industry-specific terminology signals domain expertise to ATS keyword filters "
        "and helps you rank for role-specific searches."
    )


class JobCompatibilityAnalysis(BaseModel):
    """Job role compatibility analysis"""

    score: float = Field(ge=0, le=100, default=0)
    compatibility_level: str = "Unknown"
    aligned_areas: List[str] = []
    misalignment_areas: List[str] = []
    assessment: str = ""
    issues: List[str] = []
    recommendations: List[str] = []
    why_it_affects_ats: str = (
        "Role compatibility determines whether your resume passes automated screening "
        "for a specific position based on title, skills, and experience alignment."
    )


class ChecklistItem(BaseModel):
    """Resume optimization checklist item"""

    item: str
    completed: bool = False
    priority: PriorityLevel = "Medium"
    category: str = "General"


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
    coaching_insights: List[CoachingInsight] = []
    action_verb_analysis: ActionVerbAnalysis = Field(default_factory=ActionVerbAnalysis)
    achievement_impact_analysis: AchievementImpactAnalysis = Field(
        default_factory=AchievementImpactAnalysis
    )
    skills_gap_analysis: SkillsGapAnalysis = Field(default_factory=SkillsGapAnalysis)
    readability_analysis: ReadabilityAnalysis = Field(default_factory=ReadabilityAnalysis)
    industry_relevance_analysis: IndustryRelevanceAnalysis = Field(
        default_factory=IndustryRelevanceAnalysis
    )
    job_compatibility_analysis: Optional[JobCompatibilityAnalysis] = None
    optimization_checklist: List[ChecklistItem] = []
    ai_enhanced: bool = False
