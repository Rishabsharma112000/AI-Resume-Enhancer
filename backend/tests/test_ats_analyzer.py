"""Tests for ATS analyzer"""

import pytest

from app.services.ats_analyzer import analyze_resume_ats


SAMPLE_RESUME = """
John Smith
john.smith@email.com | (555) 123-4567 | linkedin.com/in/johnsmith | San Francisco, CA

PROFESSIONAL SUMMARY
Results-driven Software Engineer with 5+ years of experience building scalable web applications.
Proven track record of reducing deployment time by 40% and leading cross-functional teams.

WORK EXPERIENCE
Senior Software Engineer | Acme Corp | Jan 2020 – Present
• Led migration of monolithic app to microservices, reducing deployment time by 40%
• Architected REST API serving 2M+ daily requests, achieving 99.9% uptime
• Mentored team of 5 junior developers, improving code review turnaround by 25%

Software Engineer | TechStart Inc | Jun 2017 – Dec 2019
• Built React dashboard used by 10K+ customers
• Implemented CI/CD pipeline reducing release cycles from 2 weeks to 2 days

EDUCATION
Bachelor of Science in Computer Science | Stanford University | 2017

SKILLS
Python, Java, JavaScript, React, AWS, Docker, Kubernetes, SQL, Git, Agile, Leadership

PROJECTS
E-Commerce Platform | Python, Django, PostgreSQL
• Built full-stack application handling 10K+ daily transactions

CERTIFICATIONS
AWS Certified Solutions Architect | Amazon Web Services | 2021
"""

SAMPLE_JD = """
We are looking for a Senior Software Engineer with experience in Python, React, AWS,
Docker, Kubernetes, microservices, REST APIs, CI/CD, and agile methodologies.
Must have strong leadership and communication skills.
"""


def test_analyze_resume_returns_report():
    report = analyze_resume_ats(SAMPLE_RESUME)
    assert report.overall_ats_score > 0
    assert report.overall_ats_score <= 100
    assert len(report.category_scores) >= 15
    assert len(report.section_feedback) == 8


def test_category_scores_present():
    report = analyze_resume_ats(SAMPLE_RESUME)
    expected_categories = [
        "Resume Structure",
        "Contact Information",
        "Professional Summary",
        "Work Experience",
        "Skills",
        "Education",
        "Projects",
        "Certifications",
        "Keyword Optimization",
        "Formatting & Structure",
        "Action Verb Usage",
        "Achievement & Impact",
        "Skills Gap",
        "Readability & Professionalism",
        "Industry Relevance",
    ]
    for cat in expected_categories:
        assert cat in report.category_scores
        assert 0 <= report.category_scores[cat] <= 100


def test_deep_analysis_dimensions():
    report = analyze_resume_ats(SAMPLE_RESUME, SAMPLE_JD)
    assert report.action_verb_analysis.score > 0
    assert report.achievement_impact_analysis.quantified_bullets > 0
    assert report.skills_gap_analysis.score > 0
    assert report.readability_analysis.score > 0
    assert report.industry_relevance_analysis.score > 0
    assert report.job_compatibility_analysis is not None
    assert report.job_compatibility_analysis.compatibility_level in ("Strong", "Moderate", "Weak")


def test_coaching_insights_and_checklist():
    report = analyze_resume_ats(SAMPLE_RESUME)
    assert len(report.coaching_insights) > 0
    assert len(report.optimization_checklist) > 0
    insight = report.coaching_insights[0]
    assert insight.what_is_wrong
    assert insight.why_it_impacts_ats
    assert insight.how_to_fix
    assert insight.expected_improvement


def test_section_feedback_structure():
    report = analyze_resume_ats(SAMPLE_RESUME)
    for section in report.section_feedback:
        assert section.section_name
        assert 0 <= section.score <= 100
        assert section.assessment
        assert section.ats_impact in ("High", "Medium", "Low")
        assert section.why_it_affects_ats


def test_keyword_analysis_with_jd():
    report = analyze_resume_ats(SAMPLE_RESUME, SAMPLE_JD)
    assert report.keyword_analysis.keyword_match_score > 0
    assert len(report.keyword_analysis.extracted_keywords) > 0
    assert len(report.keyword_analysis.matched_keywords) > 0


def test_strengths_and_weaknesses():
    report = analyze_resume_ats(SAMPLE_RESUME)
    assert isinstance(report.strengths, list)
    assert isinstance(report.weaknesses, list)
    assert len(report.strengths) > 0


def test_roadmap_generated():
    report = analyze_resume_ats(SAMPLE_RESUME)
    assert isinstance(report.roadmap, list)
    for item in report.roadmap:
        assert item.category in (
            "Critical Fixes",
            "Recommended Improvements",
            "Optional Enhancements",
        )
        assert item.estimated_score_gain >= 0


def test_poor_resume_low_score():
    poor_resume = "John\nSome random text without sections."
    report = analyze_resume_ats(poor_resume)
    assert report.overall_ats_score < 60
    assert len(report.weaknesses) > 0
    assert len(report.roadmap) > 0


def test_improvement_suggestions():
    report = analyze_resume_ats(SAMPLE_RESUME)
    assert isinstance(report.improvement_suggestions, list)


def test_formatting_issues_detected():
    table_resume = SAMPLE_RESUME + "\n| Col1 | Col2 | Col3 |\n| Data | More | Here |"
    report = analyze_resume_ats(table_resume)
    assert len(report.formatting_issues) > 0
