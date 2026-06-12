"""CrewAI agents for resume analysis and enhancement"""

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from app.core.config import settings
import json


# Initialize LLM
def get_llm():
    """Get LLM instance"""
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
        base_url=settings.OPENAI_BASE_URL
    )


class ResumeAnalysisAgents:
    """Resume Analysis Agents"""

    def __init__(self):
        self.llm = get_llm()

    def resume_analyzer_agent(self) -> Agent:
        """Resume Analyzer Agent"""
        return Agent(
            role="Resume Analyzer",
            goal="Analyze resume content and extract key information including work experience, education, skills, and achievements",
            backstory="Expert resume analyst with deep understanding of resume structure and content analysis",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )

    def ats_analyzer_agent(self) -> Agent:
        """ATS Analyzer Agent"""
        return Agent(
            role="ATS Analyzer",
            goal="Analyze resume for ATS compatibility and calculate scores based on keyword matching and formatting",
            backstory="Specialized in Applicant Tracking System optimization with knowledge of ATS algorithms and best practices",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )

    def resume_rewriter_agent(self) -> Agent:
        """Resume Rewriter Agent"""
        return Agent(
            role="Resume Rewriter",
            goal="Rewrite resume sections to improve clarity, impact, and keyword optimization",
            backstory="Expert writer skilled in crafting compelling resume content with strong action verbs and quantifiable achievements",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )

    def final_reviewer_agent(self) -> Agent:
        """Final Reviewer Agent"""
        return Agent(
            role="Final Reviewer",
            goal="Review and finalize enhanced resume ensuring quality, consistency, and relevance",
            backstory="Senior HR consultant with expertise in resume quality assessment and best practices",
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
        )


class ResumeAnalysisTasks:
    """Resume Analysis Tasks"""

    @staticmethod
    def analyze_resume_task(agent: Agent, resume_text: str, job_description: str = None) -> Task:
        """Analyze resume task"""
        description = f"""
        Analyze the following resume and extract key information:
        
        Resume Content:
        {resume_text}
        
        Please extract and structure the following:
        1. Professional summary/objective
        2. Work experience (companies, positions, duration, key responsibilities)
        3. Education (schools, degrees, graduation dates)
        4. Skills (technical and soft skills)
        5. Certifications and licenses
        6. Key achievements and metrics
        
        Return the analysis as a JSON object with these keys: summary, experience, education, skills, certifications, achievements
        """

        if job_description:
            description += f"""
        
        Also consider the following job description for relevance analysis:
        {job_description}
        
        Identify how the resume aligns with the job requirements.
        """

        return Task(
            description=description,
            agent=agent,
            expected_output="JSON object with structured resume analysis including all extracted sections and job alignment (if job description provided)"
        )

    @staticmethod
    def ats_analysis_task(agent: Agent, resume_text: str, job_description: str = None) -> Task:
        """ATS analysis task"""
        description = f"""
        Analyze the following resume for ATS compatibility:
        
        Resume Content:
        {resume_text}
        
        Evaluate:
        1. ATS Score (0-100): Based on formatting, keyword usage, section clarity
        2. Missing keywords (if job description provided)
        3. Missing skills (if job description provided)
        4. Strengths: What the resume does well for ATS
        5. Weaknesses: What could be improved
        6. Recommendations: Specific improvements for ATS optimization
        
        Return as JSON with keys: ats_score, keyword_match_score, missing_keywords, missing_skills, strengths, weaknesses, recommendations
        """

        if job_description:
            description += f"""
        
        Job Description to match against:
        {job_description}
        """

        return Task(
            description=description,
            agent=agent,
            expected_output="JSON object with ATS analysis including scores, missing elements, and recommendations"
        )

    @staticmethod
    def rewrite_resume_task(agent: Agent, resume_text: str, analysis_data: dict, job_description: str = None) -> Task:
        """Rewrite resume task"""
        description = f"""
        Based on the following analysis, rewrite and enhance the resume:
        
        Original Resume:
        {resume_text}
        
        Analysis Data:
        {json.dumps(analysis_data, indent=2)}
        
        Please:
        1. Rewrite the professional summary to be more compelling and ATS-friendly
        2. Enhance experience bullets with strong action verbs and quantifiable results
        3. Highlight missing skills from the job description (if applicable)
        4. Improve overall structure and formatting
        5. Ensure all content is ATS-compatible
        
        Return as JSON with keys: enhanced_summary, enhanced_experience, enhanced_full_content, improvements_made
        """

        if job_description:
            description += f"""
        
        Target Job Description:
        {job_description}
        
        Align content specifically to this job requirements.
        """

        return Task(
            description=description,
            agent=agent,
            expected_output="JSON object with rewritten resume sections and list of improvements made"
        )

    @staticmethod
    def final_review_task(agent: Agent, original_resume: str, enhanced_resume: str, analysis_data: dict) -> Task:
        """Final review task"""
        description = f"""
        Review and finalize the enhanced resume:
        
        Original Resume:
        {original_resume}
        
        Enhanced Resume:
        {enhanced_resume}
        
        Analysis Data:
        {json.dumps(analysis_data, indent=2)}
        
        Please:
        1. Verify quality and consistency of enhancements
        2. Ensure no information loss from original
        3. Check for grammatical errors and formatting issues
        4. Confirm ATS compatibility
        5. Provide overall assessment and final recommendations
        6. Flag any concerns or issues found
        
        Return as JSON with keys: quality_score, is_ready, issues_found, recommendations, final_notes
        """

        return Task(
            description=description,
            agent=agent,
            expected_output="JSON object with final review assessment, quality score, and readiness status"
        )


class ResumeAnalysisCrew:
    """Resume Analysis Crew Coordinator"""

    def __init__(self):
        self.agents_factory = ResumeAnalysisAgents()
        self.tasks_factory = ResumeAnalysisTasks()

    def execute_workflow(
        self,
        resume_text: str,
        job_description: str = None
    ) -> dict:
        """Execute the resume analysis workflow"""

        # Initialize agents
        resume_analyzer = self.agents_factory.resume_analyzer_agent()
        ats_analyzer = self.agents_factory.ats_analyzer_agent()
        resume_rewriter = self.agents_factory.resume_rewriter_agent()
        final_reviewer = self.agents_factory.final_reviewer_agent()

        # Create tasks
        analyze_task = self.tasks_factory.analyze_resume_task(
            resume_analyzer, resume_text, job_description
        )
        
        ats_task = self.tasks_factory.ats_analysis_task(
            ats_analyzer, resume_text, job_description
        )
        
        rewrite_task = self.tasks_factory.rewrite_resume_task(
            resume_rewriter, resume_text, {}, job_description
        )
        
        review_task = self.tasks_factory.final_review_task(
            final_reviewer, resume_text, "", {}
        )

        # Create crew with sequential execution
        crew = Crew(
            agents=[resume_analyzer, ats_analyzer, resume_rewriter, final_reviewer],
            tasks=[analyze_task, ats_task, rewrite_task, review_task],
            verbose=True,
        )

        # Execute workflow
        result = crew.kickoff()
        
        return {
            "status": "success",
            "output": result,
            "resume_text": resume_text,
        }


def analyze_resume(resume_text: str, job_description: str = None) -> dict:
    """Analyze resume using CrewAI"""
    crew = ResumeAnalysisCrew()
    return crew.execute_workflow(resume_text, job_description)
