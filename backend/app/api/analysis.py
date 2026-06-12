"""Analysis routes"""

import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.resume_analysis import ResumeAnalysisCreate, ResumeAnalysisResponse
from app.schemas.enhanced_resume import EnhancedResumeResponse, EnhanceResumeRequest
from app.schemas.ats_analysis import ATSAnalysisReport
from app.models.resume_analysis import ResumeAnalysis
from app.models.enhanced_resume import EnhancedResume
from app.models.resume import Resume
from app.models.job_description import JobDescription
from app.services.ats_analyzer import analyze_resume_ats
from app.services.ai_service import enrich_analysis_with_ai, enhance_resume_with_ai

router = APIRouter(prefix="/analysis", tags=["Analysis"])


def _build_analysis_response(analysis: ResumeAnalysis) -> ResumeAnalysisResponse:
    """Build response with parsed ATS report from stored JSON."""
    ats_report = None
    if analysis.analysis_output:
        try:
            ats_report = ATSAnalysisReport.model_validate_json(analysis.analysis_output)
        except Exception:
            pass

    return ResumeAnalysisResponse(
        id=analysis.id,
        user_id=analysis.user_id,
        resume_id=analysis.resume_id,
        job_description_id=analysis.job_description_id,
        ats_score=analysis.ats_score,
        keyword_match_score=analysis.keyword_match_score,
        missing_skills=analysis.missing_skills,
        missing_keywords=analysis.missing_keywords,
        strengths=analysis.strengths,
        weaknesses=analysis.weaknesses,
        ats_report=ats_report,
        created_at=analysis.created_at,
        updated_at=analysis.updated_at,
    )


def _build_enhanced_response(enhanced: EnhancedResume, original_content: str = "") -> EnhancedResumeResponse:
    """Build enhanced resume response with parsed improvements."""
    improvements = None
    if enhanced.improvements_made:
        try:
            improvements = json.loads(enhanced.improvements_made)
        except (json.JSONDecodeError, TypeError):
            improvements = None

    return EnhancedResumeResponse(
        id=enhanced.id,
        user_id=enhanced.user_id,
        resume_id=enhanced.resume_id,
        analysis_id=enhanced.analysis_id,
        enhanced_summary=enhanced.enhanced_summary,
        enhanced_experience=enhanced.enhanced_experience,
        enhanced_full_content=enhanced.enhanced_full_content,
        improvements_made=improvements,
        estimated_ats_score_gain=float(enhanced.estimated_ats_score_gain or 0),
        original_content=original_content or None,
        version=enhanced.version,
        created_at=enhanced.created_at,
        updated_at=enhanced.updated_at,
    )


@router.post("/analyze", response_model=ResumeAnalysisResponse, status_code=status.HTTP_201_CREATED)
async def analyze_resume(
    analysis_request: ResumeAnalysisCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Analyze a resume with comprehensive ATS evaluation."""

    resume = db.query(Resume).filter(
        Resume.id == analysis_request.resume_id,
        Resume.user_id == current_user.id,
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    job_description = None
    job_description_text = ""
    if analysis_request.job_description_id:
        job_description = db.query(JobDescription).filter(
            JobDescription.id == analysis_request.job_description_id,
            JobDescription.user_id == current_user.id,
        ).first()
        if job_description:
            job_description_text = job_description.content

    report = analyze_resume_ats(resume.raw_text, job_description_text or None)
    report = await enrich_analysis_with_ai(
        report, resume.raw_text, job_description_text or None
    )

    analysis = ResumeAnalysis(
        user_id=current_user.id,
        resume_id=analysis_request.resume_id,
        job_description_id=analysis_request.job_description_id,
        ats_score=report.overall_ats_score,
        keyword_match_score=report.keyword_analysis.keyword_match_score,
        missing_keywords=report.keyword_analysis.missing_keywords,
        missing_skills=report.skills_gap_analysis.missing_skills or report.keyword_analysis.missing_keywords,
        strengths=report.strengths,
        weaknesses=report.weaknesses,
        analysis_output=report.model_dump_json(),
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return _build_analysis_response(analysis)


@router.get("/{analysis_id}", response_model=ResumeAnalysisResponse)
async def get_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get analysis details."""
    analysis = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.id == analysis_id,
        ResumeAnalysis.user_id == current_user.id,
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        )

    return _build_analysis_response(analysis)


@router.post("/enhance", response_model=EnhancedResumeResponse, status_code=status.HTTP_201_CREATED)
async def enhance_resume(
    request: EnhanceResumeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Enhance a resume using AI based on ATS analysis."""

    analysis = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.id == request.analysis_id,
        ResumeAnalysis.user_id == current_user.id,
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        )

    resume = db.query(Resume).filter(
        Resume.id == analysis.resume_id,
        Resume.user_id == current_user.id,
    ).first()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    job_description_text = ""
    if analysis.job_description_id:
        job_description = db.query(JobDescription).filter(
            JobDescription.id == analysis.job_description_id,
            JobDescription.user_id == current_user.id,
        ).first()
        if job_description:
            job_description_text = job_description.content

    ats_report = None
    if analysis.analysis_output:
        try:
            ats_report = ATSAnalysisReport.model_validate_json(analysis.analysis_output)
        except Exception:
            pass

    try:
        result = await enhance_resume_with_ai(
            resume.raw_text,
            ats_report,
            job_description_text or None,
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resume enhancement failed: {exc}",
        ) from exc

    existing_count = db.query(EnhancedResume).filter(
        EnhancedResume.analysis_id == request.analysis_id,
        EnhancedResume.user_id == current_user.id,
    ).count()

    enhanced_resume = EnhancedResume(
        user_id=current_user.id,
        resume_id=analysis.resume_id,
        analysis_id=request.analysis_id,
        enhanced_summary=result.get("enhanced_summary", ""),
        enhanced_experience=result.get("enhanced_experience", ""),
        enhanced_full_content=result.get("enhanced_full_content", ""),
        improvements_made=json.dumps(result.get("improvements_made", [])),
        estimated_ats_score_gain=int(result.get("estimated_ats_score_gain", 0)),
        version=existing_count + 1,
    )

    db.add(enhanced_resume)
    db.commit()
    db.refresh(enhanced_resume)

    return _build_enhanced_response(enhanced_resume, resume.raw_text)


@router.get("/enhanced/{enhanced_id}", response_model=EnhancedResumeResponse)
async def get_enhanced_resume(
    enhanced_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get enhanced resume details."""
    enhanced = db.query(EnhancedResume).filter(
        EnhancedResume.id == enhanced_id,
        EnhancedResume.user_id == current_user.id,
    ).first()

    if not enhanced:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enhanced resume not found",
        )

    resume = db.query(Resume).filter(Resume.id == enhanced.resume_id).first()
    original = resume.raw_text if resume else ""

    return _build_enhanced_response(enhanced, original)
