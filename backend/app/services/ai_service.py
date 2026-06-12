"""OpenAI-powered resume analysis enrichment and enhancement"""

import json
import re
from typing import Optional

import httpx

from app.core.config import settings
from app.schemas.ats_analysis import (
    ATSAnalysisReport,
    CoachingInsight,
    ChecklistItem,
    ImprovementSuggestion,
)


def _is_configured() -> bool:
    return bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip())


def _extract_json(text: str) -> dict:
    """Extract JSON object from model response."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


async def _chat_completion(system_prompt: str, user_prompt: str, temperature: float = 0.4) -> str:
    """Call OpenAI chat completions API."""
    if not _is_configured():
        raise RuntimeError("OpenAI API key is not configured")

    url = f"{settings.OPENAI_BASE_URL.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    return data["choices"][0]["message"]["content"]


COACHING_SYSTEM_PROMPT = """You are an expert ATS resume coach and career advisor.
Provide detailed, human-like coaching — never generic filler.
Every insight must explain what is wrong, why it hurts ATS performance, how to fix it, and expected improvement.
Return ONLY valid JSON matching the requested schema. No markdown."""


async def enrich_analysis_with_ai(
    report: ATSAnalysisReport,
    resume_text: str,
    job_description_text: Optional[str] = None,
) -> ATSAnalysisReport:
    """Enrich rule-based ATS report with AI coaching insights."""
    if not _is_configured():
        return report

    report_summary = {
        "overall_ats_score": report.overall_ats_score,
        "category_scores": report.category_scores,
        "strengths": report.strengths,
        "weaknesses": report.weaknesses,
        "missing_keywords": report.keyword_analysis.missing_keywords[:15],
        "section_scores": [
            {"name": s.section_name, "score": s.score, "issues": s.issues[:3]}
            for s in report.section_feedback
        ],
        "action_verb_score": report.action_verb_analysis.score,
        "achievement_score": report.achievement_impact_analysis.score,
        "skills_gap": report.skills_gap_analysis.missing_skills[:10],
    }

    jd_context = (
        f"\n\nTarget Job Description:\n{job_description_text[:4000]}"
        if job_description_text
        else "\n\nNo job description provided — give general industry guidance."
    )

    user_prompt = f"""Analyze this resume ATS report and provide expert coaching.

Resume (excerpt):
{resume_text[:6000]}

ATS Report Summary:
{json.dumps(report_summary, indent=2)}
{jd_context}

Return JSON with this exact structure:
{{
  "coaching_insights": [
    {{
      "area": "string",
      "what_is_wrong": "string",
      "why_it_impacts_ats": "string",
      "how_to_fix": "string",
      "expected_improvement": "string",
      "priority": "Critical|High|Medium|Low"
    }}
  ],
  "improvement_suggestions": [
    {{
      "area": "string",
      "current_state": "string",
      "suggestion": "string",
      "example": "string or null",
      "ats_impact": "High|Medium|Low",
      "why_it_affects_ats": "string",
      "expected_improvement": "string"
    }}
  ],
  "optimization_checklist": [
    {{
      "item": "string",
      "completed": false,
      "priority": "Critical|High|Medium|Low",
      "category": "string"
    }}
  ],
  "strengths": ["string"],
  "weaknesses": ["string"]
}}

Provide 6-10 coaching_insights, 5-8 improvement_suggestions, and 8-12 checklist items.
Prioritize highest-impact ATS fixes first."""

    try:
        raw = await _chat_completion(COACHING_SYSTEM_PROMPT, user_prompt, temperature=0.5)
        data = _extract_json(raw)

        if data.get("coaching_insights"):
            report.coaching_insights = [
                CoachingInsight.model_validate(item) for item in data["coaching_insights"]
            ]

        if data.get("improvement_suggestions"):
            report.improvement_suggestions = [
                ImprovementSuggestion.model_validate(item)
                for item in data["improvement_suggestions"]
            ]

        if data.get("optimization_checklist"):
            report.optimization_checklist = [
                ChecklistItem.model_validate(item) for item in data["optimization_checklist"]
            ]

        if data.get("strengths"):
            report.strengths = data["strengths"][:10]

        if data.get("weaknesses"):
            report.weaknesses = data["weaknesses"][:10]

        report.ai_enhanced = True
    except Exception:
        pass

    return report


ENHANCE_SYSTEM_PROMPT = """You are an expert resume writer specializing in ATS-optimized resumes.
Rewrite resume content to maximize ATS compatibility while maintaining factual accuracy.
NEVER invent employers, degrees, dates, or achievements not supported by the original resume.
You may rephrase, strengthen verbs, add reasonable metric framing only where implied, and improve structure.
Return ONLY valid JSON. No markdown."""


async def enhance_resume_with_ai(
    resume_text: str,
    analysis_report: Optional[ATSAnalysisReport] = None,
    job_description_text: Optional[str] = None,
) -> dict:
    """Generate AI-enhanced resume content."""
    if not _is_configured():
        raise RuntimeError(
            "OpenAI API key is not configured. Set OPENAI_API_KEY in your environment."
        )

    analysis_context = ""
    if analysis_report:
        analysis_context = f"""
ATS Analysis Summary:
- Overall Score: {analysis_report.overall_ats_score}
- Missing Keywords: {', '.join(analysis_report.keyword_analysis.missing_keywords[:15])}
- Top Weaknesses: {'; '.join(analysis_report.weaknesses[:5])}
- Skills Gaps: {', '.join(analysis_report.skills_gap_analysis.missing_skills[:10])}
"""

    jd_context = (
        f"\nTarget Job Description:\n{job_description_text[:4000]}"
        if job_description_text
        else ""
    )

    user_prompt = f"""Enhance this resume for ATS optimization and professional impact.

Original Resume:
{resume_text[:8000]}
{analysis_context}
{jd_context}

Requirements:
1. Rewrite using professional, ATS-friendly language
2. Improve bullet points with strong action verbs
3. Quantify achievements where the original implies measurable impact
4. Optimize for ATS keyword matching (use missing keywords only if factually accurate)
5. Improve professional summary/objective
6. Enhance work experience descriptions
7. Improve skills presentation
8. Fix grammar, spelling, and formatting
9. Maintain factual accuracy — do not fabricate experience
10. Use standard section headings: PROFESSIONAL SUMMARY, WORK EXPERIENCE, EDUCATION, SKILLS, etc.

Return JSON:
{{
  "enhanced_summary": "rewritten professional summary",
  "enhanced_experience": "rewritten work experience section with bullets",
  "enhanced_skills": "optimized skills section",
  "enhanced_full_content": "complete enhanced resume text with all sections",
  "improvements_made": [
    {{
      "section": "string",
      "change": "what was improved",
      "before": "original excerpt",
      "after": "enhanced excerpt"
    }}
  ],
  "estimated_ats_score_gain": number
}}"""

    raw = await _chat_completion(ENHANCE_SYSTEM_PROMPT, user_prompt, temperature=0.4)
    return _extract_json(raw)
