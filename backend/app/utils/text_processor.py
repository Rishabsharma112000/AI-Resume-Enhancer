"""Text processing utilities"""

import re


def extract_email(text: str) -> str:
    """Extract email from text"""
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def extract_phone(text: str) -> str:
    """Extract phone number from text"""
    pattern = r"(\+1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}"
    match = re.search(pattern, text)
    return match.group(0) if match else ""


def extract_sections(text: str) -> dict:
    """Extract common resume sections"""
    sections = {
        "summary": "",
        "experience": "",
        "education": "",
        "skills": "",
        "projects": "",
        "certifications": ""
    }
    
    # Define section patterns
    section_patterns = {
        "summary": r"(?:PROFESSIONAL\s+SUMMARY|SUMMARY|OBJECTIVE|PROFILE)",
        "experience": r"(?:WORK\s+EXPERIENCE|EXPERIENCE|PROFESSIONAL\s+EXPERIENCE)",
        "education": r"(?:EDUCATION|ACADEMIC)",
        "skills": r"(?:SKILLS|TECHNICAL\s+SKILLS)",
        "projects": r"(?:PROJECTS|PORTFOLIO)",
        "certifications": r"(?:CERTIFICATIONS|LICENSES)"
    }
    
    # Extract sections (simple approach)
    text_upper = text.upper()
    for section, pattern in section_patterns.items():
        match = re.search(pattern, text_upper)
        if match:
            start_idx = text_upper.index(match.group(0))
            # Find next section or end of text
            sections[section] = text[start_idx:min(start_idx + 1000, len(text))]
    
    return sections


def extract_skills_from_text(text: str) -> list:
    """Extract potential skills from text"""
    # Common technical and professional skills
    common_skills = {
        "python", "java", "javascript", "c++", "c#", "go", "rust", "php", "ruby",
        "sql", "nosql", "mongodb", "postgresql", "mysql", "aws", "azure", "gcp",
        "docker", "kubernetes", "git", "jenkins", "terraform", "ansible",
        "react", "angular", "vue", "node.js", "express", "django", "flask",
        "spring", "spring boot", "hibernate", "jpa", "rest", "graphql", "api",
        "machine learning", "deep learning", "nlp", "computer vision",
        "agile", "scrum", "kanban", "jira", "confluence",
        "leadership", "communication", "problem solving", "team work"
    }
    
    text_lower = text.lower()
    found_skills = []
    
    for skill in common_skills:
        if skill in text_lower:
            found_skills.append(skill)
    
    return found_skills


def generate_ats_score(resume_text: str, job_description_text: str = None) -> float:
    """Generate ATS score"""
    score = 0.0
    
    # Check for common ATS-friendly elements
    checks = {
        "email": extract_email(resume_text) != "",
        "phone": extract_phone(resume_text) != "",
        "clear_sections": len(extract_sections(resume_text)) >= 3,
        "bullet_points": resume_text.count("•") >= 5 or resume_text.count("-") >= 5,
        "proper_formatting": not (resume_text.count("\n") < 5),
    }
    
    # Calculate base score
    base_score = sum(checks.values()) * 20
    score = base_score
    
    # If job description provided, add keyword match score
    if job_description_text:
        jd_keywords = extract_skills_from_text(job_description_text)
        resume_keywords = extract_skills_from_text(resume_text)
        
        if jd_keywords:
            matches = len([k for k in jd_keywords if k in resume_keywords])
            keyword_match = (matches / len(jd_keywords)) * 100
            score = (score + keyword_match) / 2
    
    return min(score, 100)
