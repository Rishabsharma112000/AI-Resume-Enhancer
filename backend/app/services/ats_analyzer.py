"""Comprehensive ATS resume analyzer"""

import re
from typing import Optional

from app.schemas.ats_analysis import (
    ATSAnalysisReport,
    SectionFeedback,
    KeywordAnalysis,
    FormattingIssue,
    ImprovementSuggestion,
    RoadmapItem,
    CoachingInsight,
    ActionVerbAnalysis,
    AchievementImpactAnalysis,
    SkillsGapAnalysis,
    ReadabilityAnalysis,
    IndustryRelevanceAnalysis,
    JobCompatibilityAnalysis,
    ChecklistItem,
)
from app.utils.text_processor import (
    extract_email,
    extract_phone,
    extract_skills_from_text,
)
from app.utils.file_handler import extract_keywords


SECTION_PATTERNS = {
    "Professional Summary": r"(?:PROFESSIONAL\s+SUMMARY|SUMMARY|OBJECTIVE|PROFILE|ABOUT\s+ME)",
    "Work Experience": r"(?:WORK\s+EXPERIENCE|EXPERIENCE|PROFESSIONAL\s+EXPERIENCE|EMPLOYMENT)",
    "Education": r"(?:EDUCATION|ACADEMIC\s+BACKGROUND|ACADEMIC)",
    "Skills": r"(?:SKILLS|TECHNICAL\s+SKILLS|CORE\s+COMPETENCIES|COMPETENCIES)",
    "Projects": r"(?:PROJECTS|PORTFOLIO|PERSONAL\s+PROJECTS)",
    "Certifications": r"(?:CERTIFICATIONS|LICENSES|CREDENTIALS)",
}

CATEGORY_LABELS = {
    "resume_structure": "Resume Structure",
    "contact_information": "Contact Information",
    "professional_summary": "Professional Summary",
    "work_experience": "Work Experience",
    "skills": "Skills",
    "education": "Education",
    "projects": "Projects",
    "certifications": "Certifications",
    "keyword_optimization": "Keyword Optimization",
    "formatting_readability": "Formatting & Structure",
    "action_verbs": "Action Verb Usage",
    "achievement_impact": "Achievement & Impact",
    "skills_gap": "Skills Gap",
    "readability_professionalism": "Readability & Professionalism",
    "industry_relevance": "Industry Relevance",
    "job_compatibility": "Job Role Compatibility",
}

ACTION_VERBS = {
    "achieved", "built", "created", "delivered", "designed", "developed",
    "drove", "enhanced", "established", "executed", "generated", "implemented",
    "improved", "increased", "launched", "led", "managed", "optimized",
    "orchestrated", "produced", "reduced", "resolved", "spearheaded",
    "streamlined", "transformed", "automated", "architected", "collaborated",
    "coordinated", "mentored", "negotiated", "pioneered", "scaled",
}

WEAK_VERBS = {"helped", "worked", "responsible", "assisted", "participated", "involved"}

INDUSTRY_KEYWORDS = {
    "python", "java", "javascript", "typescript", "react", "angular", "vue",
    "node.js", "sql", "aws", "azure", "gcp", "docker", "kubernetes", "git",
    "agile", "scrum", "ci/cd", "rest", "api", "machine learning", "data analysis",
    "project management", "leadership", "communication", "problem solving",
    "stakeholder", "cross-functional", "kpi", "roi", "sla", "devops",
    "microservices", "cloud", "security", "compliance", "automation",
}


def _extract_section_content(text: str, pattern: str) -> tuple[bool, str]:
    """Return whether section exists and its content snippet."""
    text_upper = text.upper()
    match = re.search(pattern, text_upper)
    if not match:
        return False, ""

    start_idx = match.start()
    remaining = text_upper[start_idx + len(match.group(0)) :]
    next_section_start = len(text)

    for other_pattern in SECTION_PATTERNS.values():
        if other_pattern == pattern:
            continue
        next_match = re.search(other_pattern, remaining)
        if next_match:
            candidate = start_idx + len(match.group(0)) + next_match.start()
            next_section_start = min(next_section_start, candidate)

    content = text[start_idx:next_section_start].strip()
    return True, content


def _detect_sections(text: str) -> dict[str, tuple[bool, str]]:
    """Detect all resume sections."""
    return {
        name: _extract_section_content(text, pattern)
        for name, pattern in SECTION_PATTERNS.items()
    }


def _count_bullet_points(text: str) -> int:
    bullet_chars = ["•", "●", "▪", "◦", "‣"]
    count = sum(text.count(c) for c in bullet_chars)
    count += len(re.findall(r"(?m)^\s*[-*]\s+", text))
    return count


def _has_quantifiable_metrics(text: str) -> bool:
    patterns = [
        r"\d+%",
        r"\$\d+",
        r"\d+\+?\s*(?:users|customers|clients|team members|employees)",
        r"(?:increased|decreased|reduced|improved|saved|grew)\s+(?:by\s+)?\d+",
        r"\d+\s*(?:x|times)",
        r"\d+\s*(?:years?|months?|weeks?|days?)",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def _count_action_verbs(text: str) -> int:
    words = re.findall(r"\b[a-z]+\b", text.lower())
    return sum(1 for w in words if w in ACTION_VERBS)


def _count_weak_verbs(text: str) -> int:
    words = re.findall(r"\b[a-z]+\b", text.lower())
    return sum(1 for w in words if w in WEAK_VERBS)


def _analyze_contact(text: str) -> tuple[float, SectionFeedback]:
    score = 0.0
    issues = []
    missing = []
    recommendations = []

    email = extract_email(text)
    phone = extract_phone(text)
    has_linkedin = bool(re.search(r"linkedin\.com", text, re.IGNORECASE))
    has_location = bool(
        re.search(
            r"\b(?:[A-Z][a-z]+,\s*)?(?:AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b",
            text,
        )
        or re.search(r"\b(?:remote|hybrid|on-?site)\b", text, re.IGNORECASE)
    )

    if email:
        score += 30
    else:
        missing.append("Professional email address")
        recommendations.append("Add a professional email address at the top of your resume")
        issues.append("No email address detected — ATS systems use this for candidate matching")

    if phone:
        score += 25
    else:
        missing.append("Phone number")
        recommendations.append("Include a phone number with a standard format (e.g., (555) 123-4567)")

    if has_linkedin:
        score += 20
    else:
        missing.append("LinkedIn profile URL")
        recommendations.append("Add your LinkedIn profile URL for recruiter visibility")

    if has_location:
        score += 15
    else:
        missing.append("City/State or location preference")
        recommendations.append("Include your city and state, or note if you're open to remote work")

    name_present = len(text.strip().split("\n")[0].split()) >= 2 if text.strip() else False
    if name_present:
        score += 10
    else:
        issues.append("Name may not be clearly visible at the top of the resume")
        recommendations.append("Place your full name prominently at the top in a larger font")

    impact = "High" if not email or not phone else ("Medium" if missing else "Low")
    assessment = (
        "Contact information is complete and ATS-parseable."
        if score >= 80
        else "Contact section needs improvement for ATS parsing and recruiter outreach."
        if score >= 50
        else "Critical contact information is missing — ATS may fail to identify you as a candidate."
    )

    return min(score, 100), SectionFeedback(
        section_name="Contact Information",
        score=min(score, 100),
        assessment=assessment,
        issues=issues,
        missing_information=missing,
        recommendations=recommendations,
        ats_impact=impact,
        example_improvement="John Smith | john.smith@email.com | (555) 123-4567 | linkedin.com/in/johnsmith | San Francisco, CA",
    )


def _analyze_summary(text: str, sections: dict) -> tuple[float, SectionFeedback]:
    found, content = sections.get("Professional Summary", (False, ""))
    issues = []
    missing = []
    recommendations = []
    score = 0.0

    if not found:
        score = 20
        missing.append("Professional summary section")
        recommendations.append("Add a 'Professional Summary' or 'Summary' section with 2-4 impactful sentences")
        issues.append("No summary section detected — recruiters and ATS look for this near the top")
        return score, SectionFeedback(
            section_name="Professional Summary",
            score=score,
            assessment="Professional summary section is missing.",
            issues=issues,
            missing_information=missing,
            recommendations=recommendations,
            ats_impact="High",
            example_improvement=(
                "Results-driven Software Engineer with 5+ years of experience building scalable "
                "web applications. Proven track record of reducing deployment time by 40% and leading "
                "cross-functional teams of 8+ engineers. Expertise in Python, React, and AWS cloud infrastructure."
            ),
        )

    body = re.sub(SECTION_PATTERNS["Professional Summary"], "", content, flags=re.IGNORECASE).strip()
    word_count = len(body.split())

    if word_count >= 30:
        score += 35
    elif word_count >= 15:
        score += 25
        issues.append("Summary is too brief — aim for 2-4 sentences (40-80 words)")
    else:
        score += 10
        issues.append("Summary content is very short or empty")

    if _has_quantifiable_metrics(body):
        score += 25
    else:
        recommendations.append("Include quantifiable achievements in your summary (years of experience, metrics, team size)")
        missing.append("Quantifiable metrics in summary")

    action_count = _count_action_verbs(body)
    if action_count >= 2:
        score += 20
    else:
        recommendations.append("Use strong action verbs (e.g., 'Led', 'Delivered', 'Architected') in your summary")
        issues.append("Summary lacks strong action verbs")

    if re.search(r"\b(?:i am|i have|my)\b", body, re.IGNORECASE):
        score -= 10
        issues.append("Avoid first-person pronouns ('I', 'my') in resume summaries")
        recommendations.append("Rewrite summary in third person without 'I' or 'my'")

    score = max(min(score, 100), 0)
    assessment = (
        "Strong professional summary with relevant keywords and metrics."
        if score >= 75
        else "Summary exists but could be more impactful for ATS ranking."
        if score >= 50
        else "Professional summary needs significant improvement."
    )

    return score, SectionFeedback(
        section_name="Professional Summary",
        score=score,
        assessment=assessment,
        issues=issues,
        missing_information=missing,
        recommendations=recommendations,
        ats_impact="High" if score < 50 else "Medium",
        example_improvement=(
            "Senior Product Manager with 7+ years driving B2B SaaS growth. Increased monthly "
            "active users by 65% and reduced churn by 22% through data-driven feature prioritization."
        ),
    )


def _analyze_experience(text: str, sections: dict) -> tuple[float, SectionFeedback]:
    found, content = sections.get("Work Experience", (False, ""))
    issues = []
    missing = []
    recommendations = []
    score = 0.0

    if not found:
        return 15, SectionFeedback(
            section_name="Work Experience",
            score=15,
            assessment="Work experience section is missing — this is critical for ATS evaluation.",
            issues=["No work experience section detected"],
            missing_information=["Work experience section with job titles, companies, dates, and bullet points"],
            recommendations=[
                "Add a clearly labeled 'Work Experience' or 'Professional Experience' section",
                "Include job title, company name, location, and date range for each role",
                "Use 3-5 bullet points per role with action verbs and measurable results",
            ],
            ats_impact="High",
            example_improvement=(
                "Senior Software Engineer | Acme Corp | Jan 2020 – Present\n"
                "• Led migration of monolithic app to microservices, reducing deployment time by 40%\n"
                "• Mentored team of 5 junior developers, improving code review turnaround by 25%"
            ),
        )

    body = re.sub(SECTION_PATTERNS["Work Experience"], "", content, flags=re.IGNORECASE).strip()
    bullet_count = _count_bullet_points(body)

    if bullet_count >= 8:
        score += 30
    elif bullet_count >= 4:
        score += 20
        issues.append("Consider adding more bullet points to describe your impact (aim for 3-5 per role)")
    else:
        score += 10
        issues.append("Insufficient bullet points — experience descriptions appear sparse")

    if re.search(r"\b(?:20\d{2}|19\d{2})\b", body):
        score += 20
    else:
        missing.append("Date ranges for positions")
        recommendations.append("Include date ranges (e.g., 'Jan 2020 – Present') for each position")
        issues.append("No date ranges detected — ATS uses dates for experience validation")

    if _has_quantifiable_metrics(body):
        score += 25
    else:
        recommendations.append("Add quantifiable results: percentages, dollar amounts, team sizes, or time saved")
        missing.append("Measurable achievements in experience bullets")
        issues.append("Experience bullets lack quantifiable metrics")

    action_count = _count_action_verbs(body)
    weak_count = _count_weak_verbs(body)
    if action_count >= 3:
        score += 15
    else:
        recommendations.append("Start each bullet with a strong action verb (Led, Built, Optimized, Delivered)")

    if weak_count > action_count and weak_count > 0:
        score -= 10
        issues.append("Too many passive/weak phrases ('responsible for', 'helped with', 'worked on')")

    if re.search(r"(?:inc\.|corp\.|llc|ltd|company)", body, re.IGNORECASE):
        score += 10

    score = max(min(score, 100), 0)
    assessment = (
        "Work experience is well-structured with strong, measurable accomplishments."
        if score >= 75
        else "Experience section present but needs stronger impact statements."
        if score >= 50
        else "Work experience section requires significant enhancement."
    )

    return score, SectionFeedback(
        section_name="Work Experience",
        score=score,
        assessment=assessment,
        issues=issues,
        missing_information=missing,
        recommendations=recommendations,
        ats_impact="High" if score < 50 else "Medium",
        example_improvement=(
            "• Architected REST API serving 2M+ daily requests, achieving 99.9% uptime\n"
            "• Reduced cloud infrastructure costs by $120K annually through AWS optimization"
        ),
    )


def _analyze_skills(text: str, sections: dict) -> tuple[float, SectionFeedback]:
    found, content = sections.get("Skills", (False, ""))
    issues = []
    missing = []
    recommendations = []
    score = 0.0
    found_skills = extract_skills_from_text(text)

    if not found:
        score = 25 if found_skills else 10
        issues.append("No dedicated skills section detected")
        missing.append("Dedicated skills section with categorized technical and soft skills")
        recommendations.append("Add a 'Skills' or 'Technical Skills' section listing relevant competencies")
        if found_skills:
            recommendations.append(f"Skills found in body text ({len(found_skills)} detected) — consolidate into a dedicated section")
    else:
        score += 40
        body = re.sub(SECTION_PATTERNS["Skills"], "", content, flags=re.IGNORECASE).strip()
        if len(body.split()) >= 5:
            score += 20
        else:
            issues.append("Skills section appears sparse")
            recommendations.append("List 8-15 relevant skills, grouped by category if applicable")

    if len(found_skills) >= 8:
        score += 25
    elif len(found_skills) >= 4:
        score += 15
        recommendations.append("Include more industry-relevant skills and technologies")
    else:
        score += 5
        missing.append("Industry-standard technical skills")
        recommendations.append("Add skills matching your target role (programming languages, tools, frameworks)")

    if re.search(r"(?:,\s*){3,}", text) or "|" in content:
        score += 10
    else:
        recommendations.append("Format skills as a comma-separated list or categorized groups for ATS parsing")

    if re.search(r"(?:proficient|expert|advanced|intermediate|beginner)", text, re.IGNORECASE):
        score += 5

    score = max(min(score, 100), 0)
    assessment = (
        "Skills section is comprehensive and ATS-friendly."
        if score >= 75
        else "Skills section needs expansion and better formatting."
        if score >= 50
        else "Skills section is weak or missing — critical for keyword matching."
    )

    return score, SectionFeedback(
        section_name="Skills",
        score=score,
        assessment=assessment,
        issues=issues,
        missing_information=missing,
        recommendations=recommendations,
        ats_impact="High" if score < 50 else "Medium",
        example_improvement="Technical: Python, Java, SQL, AWS, Docker, Kubernetes | Tools: Git, Jira, Jenkins | Soft Skills: Leadership, Agile, Communication",
    )


def _analyze_education(text: str, sections: dict) -> tuple[float, SectionFeedback]:
    found, content = sections.get("Education", (False, ""))
    issues = []
    missing = []
    recommendations = []
    score = 0.0

    if not found:
        return 30, SectionFeedback(
            section_name="Education",
            score=30,
            assessment="Education section not detected.",
            issues=["No education section found"],
            missing_information=["Degree, institution, graduation year"],
            recommendations=["Add an 'Education' section with degree, school name, and graduation date"],
            ats_impact="Medium",
            example_improvement="Bachelor of Science in Computer Science | Stanford University | May 2019 | GPA: 3.8/4.0",
        )

    body = re.sub(SECTION_PATTERNS["Education"], "", content, flags=re.IGNORECASE).strip()
    score += 40

    if re.search(r"\b(?:bachelor|master|ph\.?d|b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?b\.?a\.?|associate)\b", body, re.IGNORECASE):
        score += 25
    else:
        issues.append("Degree type not clearly stated")
        recommendations.append("Specify degree type (e.g., Bachelor of Science, Master of Business Administration)")

    if re.search(r"\b(?:university|college|institute|school)\b", body, re.IGNORECASE):
        score += 20
    else:
        missing.append("Institution name")
        recommendations.append("Include the full name of your educational institution")

    if re.search(r"\b(?:20\d{2}|19\d{2})\b", body):
        score += 15
    else:
        missing.append("Graduation year")
        recommendations.append("Add graduation year or expected graduation date")

    score = max(min(score, 100), 0)
    return score, SectionFeedback(
        section_name="Education",
        score=score,
        assessment="Education section is present and parseable." if score >= 70 else "Education section needs more detail.",
        issues=issues,
        missing_information=missing,
        recommendations=recommendations,
        ats_impact="Medium" if score < 50 else "Low",
    )


def _analyze_projects(text: str, sections: dict) -> tuple[float, SectionFeedback]:
    found, content = sections.get("Projects", (False, ""))
    issues = []
    missing = []
    recommendations = []

    if not found:
        return 50, SectionFeedback(
            section_name="Projects",
            score=50,
            assessment="No projects section detected. Optional but valuable for technical roles.",
            issues=[],
            missing_information=["Projects section (recommended for technical/entry-level candidates)"],
            recommendations=[
                "Consider adding a 'Projects' section to showcase hands-on work",
                "Include project name, technologies used, and measurable outcomes",
            ],
            ats_impact="Low",
            example_improvement=(
                "E-Commerce Platform | Python, Django, PostgreSQL\n"
                "• Built full-stack application handling 10K+ daily transactions with 99.5% uptime"
            ),
        )

    body = re.sub(SECTION_PATTERNS["Projects"], "", content, flags=re.IGNORECASE).strip()
    score = 60.0

    if _count_bullet_points(body) >= 2:
        score += 20
    else:
        issues.append("Project descriptions lack detail — add bullet points with technologies and outcomes")
        recommendations.append("Describe each project with technologies used and results achieved")

    if _has_quantifiable_metrics(body):
        score += 20
    else:
        recommendations.append("Include metrics in project descriptions (users served, performance gains, etc.)")

    return min(score, 100), SectionFeedback(
        section_name="Projects",
        score=min(score, 100),
        assessment="Projects section adds value to your resume." if score >= 70 else "Projects section needs more detail.",
        issues=issues,
        missing_information=missing,
        recommendations=recommendations,
        ats_impact="Low",
    )


def _analyze_certifications(text: str, sections: dict) -> tuple[float, SectionFeedback]:
    found, content = sections.get("Certifications", (False, ""))
    if not found:
        return 50, SectionFeedback(
            section_name="Certifications",
            score=50,
            assessment="No certifications section detected. Optional unless required by target role.",
            issues=[],
            missing_information=["Certifications section (if applicable to your field)"],
            recommendations=["Add relevant certifications (AWS, PMP, CPA, etc.) if you hold any"],
            ats_impact="Low",
        )

    body = re.sub(SECTION_PATTERNS["Certifications"], "", content, flags=re.IGNORECASE).strip()
    score = 70.0
    issues = []
    recommendations = []

    if len(body.split()) >= 3:
        score += 20
    else:
        issues.append("Certification entries appear incomplete")
        recommendations.append("Include certification name, issuing organization, and date obtained")

    if re.search(r"\b(?:20\d{2}|19\d{2})\b", body):
        score += 10
    else:
        recommendations.append("Add certification dates for validity verification")

    return min(score, 100), SectionFeedback(
        section_name="Certifications",
        score=min(score, 100),
        assessment="Certifications section is present.",
        issues=issues,
        missing_information=[],
        recommendations=recommendations,
        ats_impact="Low",
    )


def _analyze_structure(sections: dict) -> tuple[float, SectionFeedback]:
    core_sections = ["Professional Summary", "Work Experience", "Education", "Skills"]
    found_count = sum(1 for s in core_sections if sections.get(s, (False, ""))[0])
    score = found_count * 20

    issues = []
    missing = []
    recommendations = []

    for section in core_sections:
        if not sections.get(section, (False, ""))[0]:
            missing.append(section)
            recommendations.append(f"Add a clearly labeled '{section}' section heading")

    if found_count >= 3:
        assessment = "Resume has a solid structural foundation with standard sections."
    elif found_count >= 2:
        assessment = "Resume structure is partially complete — missing key sections."
        issues.append("Missing standard resume sections reduces ATS parse accuracy")
    else:
        assessment = "Resume structure is weak — ATS may fail to categorize content correctly."
        issues.append("Critical structural sections are missing")

    return min(score, 100), SectionFeedback(
        section_name="Resume Structure",
        score=min(score, 100),
        assessment=assessment,
        issues=issues,
        missing_information=missing,
        recommendations=recommendations,
        ats_impact="High" if found_count < 3 else "Medium",
    )


def _analyze_formatting(text: str) -> tuple[float, list[FormattingIssue]]:
    issues: list[FormattingIssue] = []
    score = 100.0

    if text.count("\t") > 5:
        score -= 15
        issues.append(FormattingIssue(
            issue="Tab characters detected",
            description="Tab characters can cause ATS parsing errors and misaligned content.",
            ats_impact="Medium",
            recommendation="Replace tabs with standard spacing or bullet points.",
        ))

    if re.search(r"\|.{1,30}\|", text):
        score -= 20
        issues.append(FormattingIssue(
            issue="Table-like formatting detected",
            description="Content formatted in table structures may not parse correctly in ATS.",
            ats_impact="High",
            recommendation="Convert table content to simple bullet points or line-separated text.",
        ))

    pipe_columns = len(re.findall(r"(?:\S+\s*\|\s*\S+){2,}", text))
    if pipe_columns > 3:
        score -= 15
        issues.append(FormattingIssue(
            issue="Multi-column layout indicators",
            description="Pipe-separated or multi-column layouts often break ATS parsing.",
            ats_impact="High",
            recommendation="Use a single-column layout with standard section headings.",
        ))

    special_chars = len(re.findall(r"[^\x00-\x7F]", text))
    if special_chars > 20:
        score -= 10
        issues.append(FormattingIssue(
            issue="Special characters or icons detected",
            description="Non-standard characters, icons, or graphics may not be parsed by ATS.",
            ats_impact="Medium",
            recommendation="Replace icons and special symbols with plain text equivalents.",
        ))

    lines = text.split("\n")
    short_lines = sum(1 for line in lines if 0 < len(line.strip()) < 20)
    if len(lines) > 10 and short_lines / len(lines) > 0.5:
        score -= 10
        issues.append(FormattingIssue(
            issue="Possible multi-column layout",
            description="Many short lines may indicate a multi-column design that ATS cannot read in order.",
            ats_impact="High",
            recommendation="Restructure content in a single-column, top-to-bottom format.",
        ))

    bullet_styles = set()
    if "•" in text:
        bullet_styles.add("bullet")
    if re.search(r"(?m)^\s*-\s+", text):
        bullet_styles.add("dash")
    if re.search(r"(?m)^\s*\*\s+", text):
        bullet_styles.add("asterisk")
    if len(bullet_styles) > 1:
        score -= 5
        issues.append(FormattingIssue(
            issue="Inconsistent bullet formatting",
            description="Mixed bullet styles can affect readability and parsing consistency.",
            ats_impact="Low",
            recommendation="Use a single bullet style throughout the resume.",
        ))

    if text.count("\n") < 5 and len(text) > 200:
        score -= 15
        issues.append(FormattingIssue(
            issue="Insufficient line breaks",
            description="Dense text blocks are hard for ATS to segment into sections.",
            ats_impact="Medium",
            recommendation="Add clear section headings and line breaks between entries.",
        ))

    heading_found = any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in SECTION_PATTERNS.values()
    )
    if not heading_found:
        score -= 20
        issues.append(FormattingIssue(
            issue="Missing section headings",
            description="Without standard section headings, ATS cannot categorize resume content.",
            ats_impact="High",
            recommendation="Add standard headings: Summary, Experience, Education, Skills.",
        ))

    if re.search(r"(?:www\.|http)", text, re.IGNORECASE) and not re.search(r"linkedin", text, re.IGNORECASE):
        score -= 5
        issues.append(FormattingIssue(
            issue="URLs may not be hyperlink-friendly",
            description="Plain-text URLs are fine, but ensure they are complete and readable.",
            ats_impact="Low",
            recommendation="Write full URLs (linkedin.com/in/yourname) without relying on hyperlinks.",
        ))

    return max(score, 0), issues


def _analyze_keywords(
    text: str,
    job_description_text: Optional[str] = None,
) -> KeywordAnalysis:
    resume_skills = extract_skills_from_text(text)
    resume_keywords = list(dict.fromkeys(resume_skills + extract_keywords(text, 25)))

    matched = []
    missing = []
    gaps = []
    recommendations = []
    match_score = 0.0

    if job_description_text:
        jd_skills = extract_skills_from_text(job_description_text)
        jd_keywords = list(dict.fromkeys(jd_skills + extract_keywords(job_description_text, 30)))
        text_lower = text.lower()

        for kw in jd_keywords:
            if kw.lower() in text_lower or kw in resume_skills:
                matched.append(kw)
            else:
                missing.append(kw)

        if jd_keywords:
            match_score = (len(matched) / len(jd_keywords)) * 100

        if missing:
            gaps = missing[:10]
            recommendations.append(
                f"Incorporate {len(missing)} missing job-relevant keywords naturally into your experience and skills sections"
            )
            recommendations.append(
                "Mirror exact terminology from the job description where it accurately reflects your experience"
            )
    else:
        industry_present = [kw for kw in INDUSTRY_KEYWORDS if kw in text.lower()]
        industry_missing = [kw for kw in INDUSTRY_KEYWORDS if kw not in text.lower()][:8]
        matched = industry_present
        gaps = industry_missing
        missing = industry_missing
        match_score = (len(industry_present) / len(INDUSTRY_KEYWORDS)) * 100
        recommendations.append("Upload a job description for targeted keyword matching")
        if industry_missing:
            recommendations.append(
                "Consider adding industry-standard keywords relevant to your target role"
            )

    if len(resume_keywords) < 10:
        recommendations.append("Expand keyword coverage by adding more role-specific terms throughout the resume")

    return KeywordAnalysis(
        extracted_keywords=resume_keywords[:30],
        matched_keywords=matched[:20],
        missing_keywords=missing[:20],
        keyword_gaps=gaps[:10],
        keyword_match_score=round(match_score, 1),
        recommendations=recommendations,
    )


def _build_improvement_suggestions(
    section_feedback: list[SectionFeedback],
    keyword_analysis: KeywordAnalysis,
) -> list[ImprovementSuggestion]:
    suggestions = []

    for section in section_feedback:
        if section.score < 70 and section.recommendations:
            suggestions.append(ImprovementSuggestion(
                area=section.section_name,
                current_state=section.assessment,
                suggestion=section.recommendations[0],
                example=section.example_improvement,
                ats_impact=section.ats_impact,
            ))

    if keyword_analysis.missing_keywords:
        suggestions.append(ImprovementSuggestion(
            area="Keyword Optimization",
            current_state=f"Missing {len(keyword_analysis.missing_keywords)} relevant keywords",
            suggestion="Integrate missing keywords into experience bullets and skills section",
            example=f"Add terms like: {', '.join(keyword_analysis.missing_keywords[:5])}",
            ats_impact="High",
        ))

    return suggestions[:12]


def _build_roadmap(
    section_feedback: list[SectionFeedback],
    formatting_issues: list[FormattingIssue],
    keyword_analysis: KeywordAnalysis,
) -> list[RoadmapItem]:
    items: list[RoadmapItem] = []
    priority = 1

    for issue in formatting_issues:
        if issue.ats_impact == "High":
            items.append(RoadmapItem(
                title=issue.issue,
                description=issue.recommendation,
                category="Critical Fixes",
                estimated_score_gain=8.0,
                priority=priority,
            ))
            priority += 1

    for section in sorted(section_feedback, key=lambda s: s.score):
        if section.score < 50 and section.ats_impact == "High":
            gain = min(15.0, (70 - section.score) * 0.3)
            items.append(RoadmapItem(
                title=f"Fix {section.section_name}",
                description=section.recommendations[0] if section.recommendations else section.assessment,
                category="Critical Fixes",
                estimated_score_gain=round(gain, 1),
                priority=priority,
            ))
            priority += 1

    if keyword_analysis.missing_keywords and keyword_analysis.keyword_match_score < 60:
        items.append(RoadmapItem(
            title="Improve keyword alignment",
            description=f"Add {len(keyword_analysis.missing_keywords)} missing keywords from the job description",
            category="Recommended Improvements",
            estimated_score_gain=round(min(12.0, len(keyword_analysis.missing_keywords) * 1.5), 1),
            priority=priority,
        ))
        priority += 1

    for section in section_feedback:
        if 50 <= section.score < 75:
            items.append(RoadmapItem(
                title=f"Enhance {section.section_name}",
                description=section.recommendations[0] if section.recommendations else section.assessment,
                category="Recommended Improvements",
                estimated_score_gain=round(min(8.0, (80 - section.score) * 0.2), 1),
                priority=priority,
            ))
            priority += 1

    optional_sections = ["Projects", "Certifications"]
    for section in section_feedback:
        if section.section_name in optional_sections and section.score < 70:
            items.append(RoadmapItem(
                title=f"Add or improve {section.section_name}",
                description=section.recommendations[0] if section.recommendations else section.assessment,
                category="Optional Enhancements",
                estimated_score_gain=3.0,
                priority=priority,
            ))
            priority += 1

    return items[:15]


def _find_strong_verbs(text: str) -> list[str]:
    words = re.findall(r"\b[a-z]+\b", text.lower())
    return list(dict.fromkeys(w for w in words if w in ACTION_VERBS))


def _find_weak_phrases(text: str) -> list[str]:
    found = []
    patterns = [
        (r"\bresponsible for\b", "responsible for"),
        (r"\bhelped with\b", "helped with"),
        (r"\bworked on\b", "worked on"),
        (r"\bassisted with\b", "assisted with"),
        (r"\bparticipated in\b", "participated in"),
        (r"\binvolved in\b", "involved in"),
        (r"\bduties included\b", "duties included"),
    ]
    for pattern, label in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            found.append(label)
    return found


def _analyze_action_verbs(text: str) -> ActionVerbAnalysis:
    strong = _find_strong_verbs(text)
    weak = _find_weak_phrases(text)
    strong_count = _count_action_verbs(text)
    weak_count = _count_weak_verbs(text) + len(weak)

    score = 40.0
    issues = []
    recommendations = []

    if strong_count >= 8:
        score += 35
    elif strong_count >= 4:
        score += 20
        recommendations.append("Increase action verb density — aim for one strong verb per bullet point")
    else:
        score += 5
        issues.append("Resume lacks sufficient strong action verbs")
        recommendations.append("Start bullets with verbs like Led, Built, Delivered, Optimized, Architected")

    if weak_count == 0:
        score += 25
    elif weak_count <= 2:
        score += 10
        issues.append("Some passive or weak phrasing detected")
        recommendations.append("Replace passive phrases with ownership-focused action verbs")
    else:
        issues.append(f"Found {weak_count} weak/passive phrases that dilute impact")
        recommendations.append("Eliminate 'responsible for', 'helped with', and 'worked on' phrasing")

    score = max(min(score, 100), 0)
    assessment = (
        "Excellent action verb usage — bullets convey ownership and impact."
        if score >= 75
        else "Moderate action verb usage — strengthening verbs will improve ATS and recruiter perception."
        if score >= 50
        else "Weak action verb usage — passive language reduces ATS keyword strength and impact."
    )

    return ActionVerbAnalysis(
        score=score,
        strong_verbs_found=strong[:15],
        weak_phrases_found=weak,
        strong_verb_count=strong_count,
        weak_phrase_count=weak_count,
        assessment=assessment,
        issues=issues,
        recommendations=recommendations,
    )


def _count_total_bullets(text: str) -> int:
    return max(_count_bullet_points(text), 1)


def _analyze_achievement_impact(text: str) -> AchievementImpactAnalysis:
    total = _count_total_bullets(text)
    quantified = 0
    issues = []
    recommendations = []

    bullet_lines = re.findall(r"(?m)^\s*(?:[•●▪◦‣\-*]\s+)(.+)$", text)
    for line in bullet_lines:
        if _has_quantifiable_metrics(line):
            quantified += 1

    if not bullet_lines and _has_quantifiable_metrics(text):
        quantified = max(1, total // 2)

    ratio = quantified / total if total else 0
    score = round(min(ratio * 100 + (20 if quantified >= 3 else 0), 100), 1)

    if ratio < 0.3:
        issues.append(f"Only {quantified} of ~{total} bullets contain quantifiable metrics")
        recommendations.append("Add percentages, dollar amounts, team sizes, or time savings to bullets")
    elif ratio < 0.6:
        recommendations.append("Increase metric coverage — aim for metrics in at least 60% of bullets")

    if quantified == 0:
        issues.append("No quantified achievements detected — ATS and recruiters favor measurable results")
        recommendations.append("Transform duties into achievements: 'Increased X by Y%' or 'Managed team of Z'")

    assessment = (
        f"Strong achievement focus with {quantified} quantified bullets."
        if score >= 70
        else f"Partial quantification — {quantified}/{total} bullets include metrics."
        if score >= 40
        else "Achievements lack measurable impact — critical for ATS ranking and recruiter appeal."
    )

    return AchievementImpactAnalysis(
        score=score,
        quantified_bullets=quantified,
        total_bullets=total,
        unquantified_bullets=max(total - quantified, 0),
        assessment=assessment,
        issues=issues,
        recommendations=recommendations,
    )


def _analyze_skills_gap(
    text: str,
    job_description_text: Optional[str] = None,
) -> SkillsGapAnalysis:
    resume_skills = extract_skills_from_text(text)
    issues = []
    recommendations = []

    if job_description_text:
        required = extract_skills_from_text(job_description_text)
        jd_keywords = extract_keywords(job_description_text, 20)
        target_skills = list(dict.fromkeys(required + jd_keywords))
        missing = [s for s in target_skills if s.lower() not in text.lower()]
        present = [s for s in target_skills if s.lower() in text.lower()]
        score = (len(present) / len(target_skills) * 100) if target_skills else 50.0
        assessment = (
            f"Strong skill alignment — {len(present)}/{len(target_skills)} required skills present."
            if score >= 70
            else f"Moderate skill gap — missing {len(missing)} skills from job requirements."
            if score >= 40
            else f"Significant skills gap — {len(missing)} required skills not found on resume."
        )
        if missing:
            issues.append(f"Missing {len(missing)} skills required by the job description")
            recommendations.append(
                "Add missing skills to your Skills section and weave them into experience bullets where accurate"
            )
    else:
        present = [kw for kw in INDUSTRY_KEYWORDS if kw in text.lower()]
        missing = [kw for kw in INDUSTRY_KEYWORDS if kw not in text.lower()][:12]
        score = (len(present) / len(INDUSTRY_KEYWORDS) * 100)
        assessment = (
            "Good coverage of industry-standard skills."
            if score >= 50
            else "Limited industry skill keywords — expand technical and professional competencies."
        )
        recommendations.append("Upload a job description for targeted skills gap analysis")

    return SkillsGapAnalysis(
        score=round(score, 1),
        present_skills=resume_skills[:20],
        missing_skills=missing[:15],
        skill_gaps=missing[:10],
        assessment=assessment,
        issues=issues,
        recommendations=recommendations,
    )


def _analyze_readability(text: str) -> ReadabilityAnalysis:
    issues = []
    recommendations = []
    words = text.split()
    word_count = len(words)
    sentences = max(len(re.findall(r"[.!?]+", text)), 1)
    avg_sentence_len = word_count / sentences

    score = 80.0
    prof_score = 85.0

    if avg_sentence_len > 30:
        score -= 15
        issues.append("Sentences are too long — ATS parsers and recruiters prefer concise bullets")
        recommendations.append("Keep bullets to 1-2 lines; break long sentences into separate points")

    if re.search(r"\b(?:i am|i have|my |me )\b", text, re.IGNORECASE):
        prof_score -= 15
        issues.append("First-person pronouns detected — unprofessional for ATS-optimized resumes")
        recommendations.append("Remove 'I', 'my', and 'me' — use implied first person in bullet format")

    if re.search(r"\b(?:awesome|cool|stuff|gonna|wanna|lol)\b", text, re.IGNORECASE):
        prof_score -= 20
        issues.append("Informal language detected")
        recommendations.append("Use formal, professional language throughout")

    exclamation_count = text.count("!")
    if exclamation_count > 2:
        prof_score -= 10
        issues.append("Excessive exclamation marks reduce professionalism")

    if word_count < 150:
        score -= 20
        issues.append("Resume content appears too brief for comprehensive ATS evaluation")

    if word_count > 1200:
        score -= 10
        recommendations.append("Consider trimming to 1-2 pages — overly long resumes may lose ATS focus")

    score = max(min(score, 100), 0)
    prof_score = max(min(prof_score, 100), 0)

    assessment = (
        "Resume is readable, professional, and ATS-parseable."
        if score >= 75 and prof_score >= 75
        else "Readability is acceptable but professionalism or conciseness could improve."
        if score >= 50
        else "Readability and professionalism need improvement for ATS and recruiter review."
    )

    return ReadabilityAnalysis(
        score=round(score, 1),
        professionalism_score=round(prof_score, 1),
        assessment=assessment,
        issues=issues,
        recommendations=recommendations,
    )


def _analyze_industry_relevance(text: str) -> IndustryRelevanceAnalysis:
    relevant = [kw for kw in INDUSTRY_KEYWORDS if kw in text.lower()]
    gaps = [kw for kw in INDUSTRY_KEYWORDS if kw not in text.lower()][:10]
    score = (len(relevant) / len(INDUSTRY_KEYWORDS)) * 100

    issues = []
    recommendations = []
    if score < 40:
        issues.append("Low industry keyword density — resume may not rank for role-specific searches")
        recommendations.append("Add industry-standard tools, methodologies, and domain terms")

    assessment = (
        f"Strong industry relevance with {len(relevant)} standard keywords present."
        if score >= 60
        else "Moderate industry keyword coverage — add more domain-specific terminology."
        if score >= 30
        else "Weak industry relevance — resume lacks standard industry keywords."
    )

    return IndustryRelevanceAnalysis(
        score=round(score, 1),
        relevant_keywords=relevant[:15],
        industry_gaps=gaps,
        assessment=assessment,
        issues=issues,
        recommendations=recommendations,
    )


def _analyze_job_compatibility(
    text: str,
    job_description_text: str,
    keyword_analysis: KeywordAnalysis,
    skills_gap: SkillsGapAnalysis,
) -> JobCompatibilityAnalysis:
    jd_lower = job_description_text.lower()
    text_lower = text.lower()

    title_patterns = re.findall(
        r"(?:seeking|looking for|position|role|title)[:\s]+([^\n.]{5,60})",
        jd_lower,
    )
    aligned = []
    misaligned = []

    if keyword_analysis.matched_keywords:
        aligned.append(f"Keyword match: {len(keyword_analysis.matched_keywords)} terms aligned")

    if skills_gap.present_skills:
        aligned.append(f"Skills present: {', '.join(skills_gap.present_skills[:5])}")

    if keyword_analysis.missing_keywords:
        misaligned.append(
            f"Missing keywords: {', '.join(keyword_analysis.missing_keywords[:5])}"
        )

    if skills_gap.missing_skills:
        misaligned.append(f"Skills gaps: {', '.join(skills_gap.missing_skills[:5])}")

    seniority_terms = ["senior", "lead", "principal", "staff", "manager", "director", "junior", "entry"]
    jd_seniority = [t for t in seniority_terms if t in jd_lower]
    resume_seniority = [t for t in seniority_terms if t in text_lower]
    if jd_seniority and not resume_seniority:
        misaligned.append(f"Job expects {jd_seniority[0]}-level experience — not reflected in resume")

    score = keyword_analysis.keyword_match_score
    if skills_gap.score:
        score = (score + skills_gap.score) / 2

    if score >= 75:
        level = "Strong"
    elif score >= 50:
        level = "Moderate"
    else:
        level = "Weak"

    issues = []
    recommendations = []
    if score < 60:
        issues.append("Resume may not pass automated screening for this specific role")
        recommendations.append("Tailor summary and top bullets to mirror job description language")
        recommendations.append("Reorder skills to prioritize job-required competencies first")

    assessment = (
        f"{level} compatibility ({round(score, 1)}%) with the target job description."
    )

    return JobCompatibilityAnalysis(
        score=round(score, 1),
        compatibility_level=level,
        aligned_areas=aligned[:6],
        misalignment_areas=misaligned[:6],
        assessment=assessment,
        issues=issues,
        recommendations=recommendations,
    )


def _build_coaching_insights(
    section_feedback: list[SectionFeedback],
    keyword_analysis: KeywordAnalysis,
    action_verbs: ActionVerbAnalysis,
    achievements: AchievementImpactAnalysis,
    skills_gap: SkillsGapAnalysis,
    formatting_issues: list[FormattingIssue],
) -> list[CoachingInsight]:
    insights: list[CoachingInsight] = []
    priority_map = {"High": "High", "Medium": "Medium", "Low": "Low"}

    for section in section_feedback:
        if section.score < 70 and section.issues:
            insights.append(CoachingInsight(
                area=section.section_name,
                what_is_wrong=section.issues[0],
                why_it_impacts_ats=(
                    f"ATS systems parse resumes by section. A weak {section.section_name.lower()} "
                    f"section ({section.score:.0f}/100) reduces your ranking and may cause "
                    "recruiters to skip your application."
                ),
                how_to_fix=section.recommendations[0] if section.recommendations else section.assessment,
                expected_improvement=f"Improving this section could raise your ATS score by 5-15 points.",
                priority="High" if section.ats_impact == "High" else priority_map.get(section.ats_impact, "Medium"),
            ))

    if keyword_analysis.missing_keywords:
        insights.append(CoachingInsight(
            area="Keyword Optimization",
            what_is_wrong=f"Missing {len(keyword_analysis.missing_keywords)} job-relevant keywords",
            why_it_impacts_ats=(
                "ATS algorithms score resumes by keyword overlap with job postings. "
                "Each missing keyword reduces your match percentage and may trigger automatic rejection."
            ),
            how_to_fix="Integrate missing keywords naturally into your summary, skills, and experience bullets",
            expected_improvement=f"Adding keywords could improve match score by {min(20, len(keyword_analysis.missing_keywords) * 2)} points.",
            priority="High" if keyword_analysis.keyword_match_score < 50 else "Medium",
        ))

    if action_verbs.score < 60:
        insights.append(CoachingInsight(
            area="Action Verbs",
            what_is_wrong=action_verbs.issues[0] if action_verbs.issues else "Weak verb usage",
            why_it_impacts_ats=action_verbs.why_it_affects_ats,
            how_to_fix=action_verbs.recommendations[0] if action_verbs.recommendations else "Use stronger action verbs",
            expected_improvement="Stronger verbs typically improve both ATS parsing and recruiter engagement by 5-10%.",
            priority="Medium",
        ))

    if achievements.score < 50:
        insights.append(CoachingInsight(
            area="Achievement Impact",
            what_is_wrong=achievements.issues[0] if achievements.issues else "Lack of quantified results",
            why_it_impacts_ats=achievements.why_it_affects_ats,
            how_to_fix=achievements.recommendations[0] if achievements.recommendations else "Add metrics to bullets",
            expected_improvement="Quantified bullets can increase interview callback rates by 40% per industry studies.",
            priority="High",
        ))

    for issue in formatting_issues:
        if issue.ats_impact == "High":
            insights.append(CoachingInsight(
                area="Formatting",
                what_is_wrong=issue.issue,
                why_it_impacts_ats=issue.description,
                how_to_fix=issue.recommendation,
                expected_improvement="Fixing formatting issues prevents ATS parsing failures that zero out your score.",
                priority="Critical",
            ))

    if skills_gap.missing_skills:
        insights.append(CoachingInsight(
            area="Skills Gap",
            what_is_wrong=f"Missing skills: {', '.join(skills_gap.missing_skills[:5])}",
            why_it_impacts_ats=skills_gap.why_it_affects_ats,
            how_to_fix=skills_gap.recommendations[0] if skills_gap.recommendations else "Add missing skills",
            expected_improvement="Closing skill gaps can improve role-specific ATS match by 10-25 points.",
            priority="High" if skills_gap.score < 50 else "Medium",
        ))

    return insights[:12]


def _build_optimization_checklist(
    section_feedback: list[SectionFeedback],
    keyword_analysis: KeywordAnalysis,
    formatting_issues: list[FormattingIssue],
    action_verbs: ActionVerbAnalysis,
    achievements: AchievementImpactAnalysis,
) -> list[ChecklistItem]:
    checklist: list[ChecklistItem] = []

    for section in section_feedback:
        if section.score < 75:
            for rec in section.recommendations[:1]:
                checklist.append(ChecklistItem(
                    item=rec,
                    completed=False,
                    priority="High" if section.ats_impact == "High" else "Medium",
                    category=section.section_name,
                ))

    for kw in keyword_analysis.missing_keywords[:5]:
        checklist.append(ChecklistItem(
            item=f"Add keyword: '{kw}' to resume (if accurate)",
            completed=False,
            priority="High",
            category="Keywords",
        ))

    for issue in formatting_issues:
        checklist.append(ChecklistItem(
            item=issue.recommendation,
            completed=False,
            priority="Critical" if issue.ats_impact == "High" else "Medium",
            category="Formatting",
        ))

    for rec in action_verbs.recommendations[:2]:
        checklist.append(ChecklistItem(
            item=rec,
            completed=False,
            priority="Medium",
            category="Action Verbs",
        ))

    for rec in achievements.recommendations[:2]:
        checklist.append(ChecklistItem(
            item=rec,
            completed=False,
            priority="High",
            category="Achievements",
        ))

    return checklist[:15]


def _enrich_section_feedback(section_feedback: list[SectionFeedback]) -> list[SectionFeedback]:
    """Add ATS impact explanations to section feedback."""
    why_map = {
        "Contact Information": "ATS systems use contact data for candidate identification and CRM integration. Missing fields can prevent your resume from being matched or contacted.",
        "Professional Summary": "The summary is heavily weighted by ATS keyword algorithms and is often the first section recruiters read after automated screening.",
        "Work Experience": "Experience sections provide the primary data for seniority matching, skill validation, and achievement scoring in ATS pipelines.",
        "Skills": "Dedicated skills sections are parsed as keyword indexes — critical for passing automated skill-based filters.",
        "Education": "Education credentials are used for minimum qualification checks and degree-based filtering in ATS.",
        "Resume Structure": "Standard section headings allow ATS parsers to categorize content correctly. Non-standard layouts cause misclassification.",
        "Projects": "Projects supplement experience for technical roles and add keyword density for specialized ATS searches.",
        "Certifications": "Certifications trigger credential-based filters and boost credibility scores in regulated industries.",
    }
    enriched = []
    for section in section_feedback:
        data = section.model_dump()
        data["why_it_affects_ats"] = why_map.get(
            section.section_name,
            "This section affects how ATS systems categorize and score your qualifications.",
        )
        enriched.append(SectionFeedback(**data))
    return enriched


def _derive_strengths_weaknesses(
    section_feedback: list[SectionFeedback],
    formatting_issues: list[FormattingIssue],
    keyword_analysis: KeywordAnalysis,
    action_verbs: Optional[ActionVerbAnalysis] = None,
    achievements: Optional[AchievementImpactAnalysis] = None,
) -> tuple[list[str], list[str]]:
    strengths = []
    weaknesses = []

    for section in section_feedback:
        if section.score >= 75:
            strengths.append(f"Strong {section.section_name.lower()}: {section.assessment}")
        elif section.score < 50:
            weaknesses.append(f"Weak {section.section_name.lower()}: {section.assessment}")

    if keyword_analysis.keyword_match_score >= 70:
        strengths.append(f"Good keyword alignment ({keyword_analysis.keyword_match_score:.0f}% match)")
    elif keyword_analysis.missing_keywords:
        weaknesses.append(
            f"Keyword gap: missing {len(keyword_analysis.missing_keywords)} terms that ATS systems look for"
        )

    if action_verbs and action_verbs.score >= 75:
        strengths.append(f"Strong action verb usage ({action_verbs.strong_verb_count} power verbs)")
    elif action_verbs and action_verbs.score < 50:
        weaknesses.append("Weak action verb usage — bullets lack ownership language")

    if achievements and achievements.score >= 70:
        strengths.append(f"Good achievement quantification ({achievements.quantified_bullets} metrics)")
    elif achievements and achievements.score < 40:
        weaknesses.append("Achievements lack measurable impact — add numbers and percentages")

    high_formatting = [i for i in formatting_issues if i.ats_impact == "High"]
    if not high_formatting and not weaknesses:
        strengths.append("No critical ATS formatting issues detected")
    for issue in high_formatting:
        weaknesses.append(f"Formatting risk: {issue.issue}")

    if not strengths:
        strengths.append("Resume contains parseable text content for ATS processing")

    return strengths[:10], weaknesses[:10]


def analyze_resume_ats(
    resume_text: str,
    job_description_text: Optional[str] = None,
) -> ATSAnalysisReport:
    """Run comprehensive ATS analysis on resume text."""
    sections = _detect_sections(resume_text)

    structure_score, structure_feedback = _analyze_structure(sections)
    contact_score, contact_feedback = _analyze_contact(resume_text)
    summary_score, summary_feedback = _analyze_summary(resume_text, sections)
    experience_score, experience_feedback = _analyze_experience(resume_text, sections)
    skills_score, skills_feedback = _analyze_skills(resume_text, sections)
    education_score, education_feedback = _analyze_education(resume_text, sections)
    projects_score, projects_feedback = _analyze_projects(resume_text, sections)
    certifications_score, certifications_feedback = _analyze_certifications(resume_text, sections)

    formatting_score, formatting_issues = _analyze_formatting(resume_text)
    keyword_analysis = _analyze_keywords(resume_text, job_description_text)

    action_verb_analysis = _analyze_action_verbs(resume_text)
    achievement_impact_analysis = _analyze_achievement_impact(resume_text)
    skills_gap_analysis = _analyze_skills_gap(resume_text, job_description_text)
    readability_analysis = _analyze_readability(resume_text)
    industry_relevance_analysis = _analyze_industry_relevance(resume_text)

    job_compatibility_analysis = None
    if job_description_text:
        job_compatibility_analysis = _analyze_job_compatibility(
            resume_text, job_description_text, keyword_analysis, skills_gap_analysis
        )

    category_scores = {
        "resume_structure": structure_score,
        "contact_information": contact_score,
        "professional_summary": summary_score,
        "work_experience": experience_score,
        "skills": skills_score,
        "education": education_score,
        "projects": projects_score,
        "certifications": certifications_score,
        "keyword_optimization": keyword_analysis.keyword_match_score,
        "formatting_readability": formatting_score,
        "action_verbs": action_verb_analysis.score,
        "achievement_impact": achievement_impact_analysis.score,
        "skills_gap": skills_gap_analysis.score,
        "readability_professionalism": (
            readability_analysis.score + readability_analysis.professionalism_score
        ) / 2,
        "industry_relevance": industry_relevance_analysis.score,
    }

    if job_compatibility_analysis:
        category_scores["job_compatibility"] = job_compatibility_analysis.score

    section_feedback = _enrich_section_feedback([
        structure_feedback,
        contact_feedback,
        summary_feedback,
        experience_feedback,
        skills_feedback,
        education_feedback,
        projects_feedback,
        certifications_feedback,
    ])

    weights = {
        "resume_structure": 0.08,
        "contact_information": 0.05,
        "professional_summary": 0.08,
        "work_experience": 0.15,
        "skills": 0.08,
        "education": 0.05,
        "projects": 0.03,
        "certifications": 0.02,
        "keyword_optimization": 0.10,
        "formatting_readability": 0.07,
        "action_verbs": 0.08,
        "achievement_impact": 0.10,
        "skills_gap": 0.08,
        "readability_professionalism": 0.06,
        "industry_relevance": 0.05,
    }

    if job_compatibility_analysis:
        weights["job_compatibility"] = 0.10
        total = sum(weights.values())
        weights = {k: v / total for k, v in weights.items()}

    overall_score = sum(
        category_scores[key] * weights[key]
        for key in weights
        if key in category_scores
    )
    overall_score = round(min(max(overall_score, 0), 100), 1)

    improvement_suggestions = _build_improvement_suggestions(section_feedback, keyword_analysis)
    roadmap = _build_roadmap(section_feedback, formatting_issues, keyword_analysis)
    strengths, weaknesses = _derive_strengths_weaknesses(
        section_feedback,
        formatting_issues,
        keyword_analysis,
        action_verb_analysis,
        achievement_impact_analysis,
    )
    coaching_insights = _build_coaching_insights(
        section_feedback,
        keyword_analysis,
        action_verb_analysis,
        achievement_impact_analysis,
        skills_gap_analysis,
        formatting_issues,
    )
    optimization_checklist = _build_optimization_checklist(
        section_feedback,
        keyword_analysis,
        formatting_issues,
        action_verb_analysis,
        achievement_impact_analysis,
    )

    return ATSAnalysisReport(
        overall_ats_score=overall_score,
        category_scores={CATEGORY_LABELS[k]: round(v, 1) for k, v in category_scores.items()},
        section_feedback=section_feedback,
        keyword_analysis=keyword_analysis,
        formatting_issues=formatting_issues,
        improvement_suggestions=improvement_suggestions,
        strengths=strengths,
        weaknesses=weaknesses,
        roadmap=roadmap,
        coaching_insights=coaching_insights,
        action_verb_analysis=action_verb_analysis,
        achievement_impact_analysis=achievement_impact_analysis,
        skills_gap_analysis=skills_gap_analysis,
        readability_analysis=readability_analysis,
        industry_relevance_analysis=industry_relevance_analysis,
        job_compatibility_analysis=job_compatibility_analysis,
        optimization_checklist=optimization_checklist,
    )
