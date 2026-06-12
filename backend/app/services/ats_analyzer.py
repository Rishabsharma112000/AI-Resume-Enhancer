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
    "formatting_readability": "Formatting & Readability",
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


def _derive_strengths_weaknesses(
    section_feedback: list[SectionFeedback],
    formatting_issues: list[FormattingIssue],
    keyword_analysis: KeywordAnalysis,
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

    high_formatting = [i for i in formatting_issues if i.ats_impact == "High"]
    if not high_formatting and not weaknesses:
        strengths.append("No critical ATS formatting issues detected")
    for issue in high_formatting:
        weaknesses.append(f"Formatting risk: {issue.issue}")

    if not strengths:
        strengths.append("Resume contains parseable text content for ATS processing")

    return strengths[:8], weaknesses[:8]


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
    }

    section_feedback = [
        structure_feedback,
        contact_feedback,
        summary_feedback,
        experience_feedback,
        skills_feedback,
        education_feedback,
        projects_feedback,
        certifications_feedback,
    ]

    weights = {
        "resume_structure": 0.12,
        "contact_information": 0.08,
        "professional_summary": 0.10,
        "work_experience": 0.20,
        "skills": 0.12,
        "education": 0.08,
        "projects": 0.05,
        "certifications": 0.03,
        "keyword_optimization": 0.12,
        "formatting_readability": 0.10,
    }

    overall_score = sum(
        category_scores[key] * weights[key]
        for key in weights
    )
    overall_score = round(min(max(overall_score, 0), 100), 1)

    improvement_suggestions = _build_improvement_suggestions(section_feedback, keyword_analysis)
    roadmap = _build_roadmap(section_feedback, formatting_issues, keyword_analysis)
    strengths, weaknesses = _derive_strengths_weaknesses(
        section_feedback, formatting_issues, keyword_analysis
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
    )
