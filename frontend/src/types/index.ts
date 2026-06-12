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
}

export interface ImprovementSuggestion {
  area: string
  current_state: string
  suggestion: string
  example?: string
  ats_impact: 'High' | 'Medium' | 'Low'
}

export interface RoadmapItem {
  title: string
  description: string
  category: 'Critical Fixes' | 'Recommended Improvements' | 'Optional Enhancements'
  estimated_score_gain: number
  priority: number
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

export interface EnhancedResume {
  id: number
  user_id: number
  resume_id: number
  analysis_id?: number
  enhanced_summary?: string
  enhanced_experience?: string
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
