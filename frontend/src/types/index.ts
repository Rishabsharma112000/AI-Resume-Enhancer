export interface User {
  id: number
  email: string
  full_name: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Resume {
  id: number
  user_id: number
  filename: string
  original_filename: string
  file_type: string
  file_size: number
  created_at: string
  updated_at: string
}

export interface ResumeDetail extends Resume {
  raw_text?: string
}

export interface JobDescription {
  id: number
  user_id: number
  title: string
  company?: string
  created_at: string
  updated_at: string
}

export interface SectionFeedback {
  section_name: string
  score: number
  assessment: string
  issues: string[]
  missing_information: string[]
  recommendations: string[]
  ats_impact: 'High' | 'Medium' | 'Low'
  why_it_affects_ats?: string
  example_improvement?: string
}

export interface KeywordAnalysis {
  extracted_keywords: string[]
  matched_keywords: string[]
  missing_keywords: string[]
  keyword_gaps: string[]
  keyword_match_score: number
  recommendations: string[]
}

export interface FormattingIssue {
  issue: string
  description: string
  ats_impact: 'High' | 'Medium' | 'Low'
  recommendation: string
  why_it_affects_ats?: string
}

export interface ImprovementSuggestion {
  area: string
  current_state: string
  suggestion: string
  example?: string
  ats_impact: 'High' | 'Medium' | 'Low'
  why_it_affects_ats?: string
  expected_improvement?: string
}

export interface RoadmapItem {
  title: string
  description: string
  category: 'Critical Fixes' | 'Recommended Improvements' | 'Optional Enhancements'
  estimated_score_gain: number
  priority: number
}

export interface CoachingInsight {
  area: string
  what_is_wrong: string
  why_it_impacts_ats: string
  how_to_fix: string
  expected_improvement: string
  priority: 'Critical' | 'High' | 'Medium' | 'Low'
}

export interface ActionVerbAnalysis {
  score: number
  strong_verbs_found: string[]
  weak_phrases_found: string[]
  strong_verb_count: number
  weak_phrase_count: number
  assessment: string
  issues: string[]
  recommendations: string[]
  why_it_affects_ats: string
}

export interface AchievementImpactAnalysis {
  score: number
  quantified_bullets: number
  total_bullets: number
  unquantified_bullets: number
  assessment: string
  issues: string[]
  recommendations: string[]
  why_it_affects_ats: string
}

export interface SkillsGapAnalysis {
  score: number
  present_skills: string[]
  missing_skills: string[]
  skill_gaps: string[]
  assessment: string
  issues: string[]
  recommendations: string[]
  why_it_affects_ats: string
}

export interface ReadabilityAnalysis {
  score: number
  professionalism_score: number
  assessment: string
  issues: string[]
  recommendations: string[]
  why_it_affects_ats: string
}

export interface IndustryRelevanceAnalysis {
  score: number
  relevant_keywords: string[]
  industry_gaps: string[]
  assessment: string
  issues: string[]
  recommendations: string[]
  why_it_affects_ats: string
}

export interface JobCompatibilityAnalysis {
  score: number
  compatibility_level: string
  aligned_areas: string[]
  misalignment_areas: string[]
  assessment: string
  issues: string[]
  recommendations: string[]
  why_it_affects_ats: string
}

export interface ChecklistItem {
  item: string
  completed: boolean
  priority: 'Critical' | 'High' | 'Medium' | 'Low'
  category: string
}

export interface ATSAnalysisReport {
  overall_ats_score: number
  category_scores: Record<string, number>
  section_feedback: SectionFeedback[]
  keyword_analysis: KeywordAnalysis
  formatting_issues: FormattingIssue[]
  improvement_suggestions: ImprovementSuggestion[]
  strengths: string[]
  weaknesses: string[]
  roadmap: RoadmapItem[]
  coaching_insights: CoachingInsight[]
  action_verb_analysis: ActionVerbAnalysis
  achievement_impact_analysis: AchievementImpactAnalysis
  skills_gap_analysis: SkillsGapAnalysis
  readability_analysis: ReadabilityAnalysis
  industry_relevance_analysis: IndustryRelevanceAnalysis
  job_compatibility_analysis?: JobCompatibilityAnalysis
  optimization_checklist: ChecklistItem[]
  ai_enhanced?: boolean
}

export interface ResumeAnalysis {
  id: number
  user_id: number
  resume_id: number
  job_description_id?: number
  ats_score?: number
  keyword_match_score?: number
  missing_skills?: string[]
  missing_keywords?: string[]
  strengths?: string[]
  weaknesses?: string[]
  ats_report?: ATSAnalysisReport
  created_at: string
  updated_at: string
}

export interface ImprovementChange {
  section: string
  change: string
  before?: string
  after?: string
}

export interface EnhancedResume {
  id: number
  user_id: number
  resume_id: number
  analysis_id?: number
  enhanced_summary?: string
  enhanced_experience?: string
  enhanced_full_content?: string
  improvements_made?: ImprovementChange[]
  estimated_ats_score_gain?: number
  original_content?: string
  version: number
  created_at: string
  updated_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  full_name: string
  password: string
}
