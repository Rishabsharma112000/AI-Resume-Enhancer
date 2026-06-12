import {
  BarChart,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Target,
  FileText,
  Zap,
  ChevronDown,
  ChevronUp,
  Lightbulb,
  Map,
} from 'lucide-react'
import { useState } from 'react'
import { ResumeAnalysis, SectionFeedback, RoadmapItem } from '../types'

interface AnalysisResultsProps {
  analysis: ResumeAnalysis
}

function ScoreBar({ label, score }: { label: string; score: number }) {
  const color =
    score >= 75 ? 'bg-green-500' : score >= 50 ? 'bg-yellow-500' : 'bg-red-500'
  const textColor =
    score >= 75 ? 'text-green-700' : score >= 50 ? 'text-yellow-700' : 'text-red-700'

  return (
    <div>
      <div className="flex justify-between items-center mb-1">
        <span className="text-sm text-gray-700">{label}</span>
        <span className={`text-sm font-semibold ${textColor}`}>{Math.round(score)}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`${color} h-2 rounded-full transition-all duration-500`}
          style={{ width: `${Math.min(score, 100)}%` }}
        />
      </div>
    </div>
  )
}

function ImpactBadge({ impact }: { impact: 'High' | 'Medium' | 'Low' }) {
  const styles = {
    High: 'bg-red-100 text-red-800 border-red-200',
    Medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    Low: 'bg-green-100 text-green-800 border-green-200',
  }
  return (
    <span className={`px-2 py-0.5 text-xs font-medium rounded-full border ${styles[impact]}`}>
      {impact} Impact
    </span>
  )
}

function SectionCard({ section }: { section: SectionFeedback }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition"
      >
        <div className="flex items-center space-x-3">
          <div
            className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold text-white ${
              section.score >= 75
                ? 'bg-green-500'
                : section.score >= 50
                  ? 'bg-yellow-500'
                  : 'bg-red-500'
            }`}
          >
            {Math.round(section.score)}
          </div>
          <div className="text-left">
            <p className="font-semibold text-gray-800">{section.section_name}</p>
            <p className="text-sm text-gray-500 line-clamp-1">{section.assessment}</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <ImpactBadge impact={section.ats_impact} />
          {expanded ? (
            <ChevronUp className="w-5 h-5 text-gray-400" />
          ) : (
            <ChevronDown className="w-5 h-5 text-gray-400" />
          )}
        </div>
      </button>

      {expanded && (
        <div className="px-4 pb-4 space-y-4 border-t border-gray-100 pt-4">
          {section.issues.length > 0 && (
            <div>
              <p className="text-sm font-medium text-red-700 mb-2">Identified Issues</p>
              <ul className="space-y-1">
                {section.issues.map((issue, idx) => (
                  <li key={idx} className="text-sm text-gray-700 flex items-start">
                    <span className="text-red-500 mr-2">•</span>
                    {issue}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {section.missing_information.length > 0 && (
            <div>
              <p className="text-sm font-medium text-orange-700 mb-2">Missing Information</p>
              <ul className="space-y-1">
                {section.missing_information.map((item, idx) => (
                  <li key={idx} className="text-sm text-gray-700 flex items-start">
                    <span className="text-orange-500 mr-2">!</span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {section.recommendations.length > 0 && (
            <div>
              <p className="text-sm font-medium text-blue-700 mb-2">Recommendations</p>
              <ul className="space-y-1">
                {section.recommendations.map((rec, idx) => (
                  <li key={idx} className="text-sm text-gray-700 flex items-start">
                    <span className="text-blue-500 mr-2">→</span>
                    {rec}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {section.example_improvement && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-3">
              <p className="text-sm font-medium text-green-800 mb-1">Example Improvement</p>
              <p className="text-sm text-green-700 whitespace-pre-line">
                {section.example_improvement}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function RoadmapCard({ item }: { item: RoadmapItem }) {
  const categoryStyles = {
    'Critical Fixes': 'border-red-300 bg-red-50',
    'Recommended Improvements': 'border-yellow-300 bg-yellow-50',
    'Optional Enhancements': 'border-blue-300 bg-blue-50',
  }
  const badgeStyles = {
    'Critical Fixes': 'bg-red-100 text-red-800',
    'Recommended Improvements': 'bg-yellow-100 text-yellow-800',
    'Optional Enhancements': 'bg-blue-100 text-blue-800',
  }

  return (
    <div className={`rounded-lg border p-4 ${categoryStyles[item.category]}`}>
      <div className="flex items-start justify-between mb-2">
        <div>
          <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${badgeStyles[item.category]}`}>
            {item.category}
          </span>
          <h4 className="font-semibold text-gray-800 mt-2">{item.title}</h4>
        </div>
        <div className="text-right shrink-0 ml-4">
          <p className="text-xs text-gray-500">Est. gain</p>
          <p className="text-lg font-bold text-green-600">+{item.estimated_score_gain}</p>
        </div>
      </div>
      <p className="text-sm text-gray-700">{item.description}</p>
    </div>
  )
}

export default function AnalysisResults({ analysis }: AnalysisResultsProps) {
  const report = analysis.ats_report
  const atsScore = report?.overall_ats_score ?? analysis.ats_score ?? 0
  const keywordScore =
    report?.keyword_analysis?.keyword_match_score ?? analysis.keyword_match_score ?? 0

  return (
    <div className="space-y-8">
      {/* Overall Scores */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm font-medium">Overall ATS Score</p>
              <p className="text-5xl font-bold">{Math.round(atsScore)}</p>
              <p className="text-blue-100 text-xs mt-1">out of 100</p>
            </div>
            <BarChart className="w-14 h-14 opacity-20" />
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-500 to-green-600 text-white rounded-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm font-medium">Keyword Match</p>
              <p className="text-5xl font-bold">{Math.round(keywordScore)}%</p>
              <p className="text-green-100 text-xs mt-1">job relevance</p>
            </div>
            <TrendingUp className="w-14 h-14 opacity-20" />
          </div>
        </div>
      </div>

      {/* Category Scores */}
      {report?.category_scores && Object.keys(report.category_scores).length > 0 && (
        <div className="bg-white rounded-lg p-6 border border-gray-200">
          <div className="flex items-center space-x-2 mb-4">
            <Target className="w-5 h-5 text-blue-600" />
            <h3 className="font-semibold text-gray-800">Category Scores</h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {Object.entries(report.category_scores).map(([label, score]) => (
              <ScoreBar key={label} label={label} score={score} />
            ))}
          </div>
        </div>
      )}

      {/* Strengths & Weaknesses */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {(report?.strengths ?? analysis.strengths)?.length ? (
          <div className="bg-white rounded-lg p-6 border border-green-200">
            <div className="flex items-center space-x-2 mb-4">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <h3 className="font-semibold text-gray-800">Strengths</h3>
            </div>
            <ul className="space-y-2">
              {(report?.strengths ?? analysis.strengths ?? []).map((strength, idx) => (
                <li key={idx} className="text-gray-700 flex items-start text-sm">
                  <span className="text-green-600 mr-2 shrink-0">✓</span>
                  <span>{strength}</span>
                </li>
              ))}
            </ul>
          </div>
        ) : null}

        {(report?.weaknesses ?? analysis.weaknesses)?.length ? (
          <div className="bg-white rounded-lg p-6 border border-orange-200">
            <div className="flex items-center space-x-2 mb-4">
              <AlertCircle className="w-5 h-5 text-orange-600" />
              <h3 className="font-semibold text-gray-800">Weaknesses & Risk Areas</h3>
            </div>
            <ul className="space-y-2">
              {(report?.weaknesses ?? analysis.weaknesses ?? []).map((weakness, idx) => (
                <li key={idx} className="text-gray-700 flex items-start text-sm">
                  <span className="text-orange-600 mr-2 shrink-0">!</span>
                  <span>{weakness}</span>
                </li>
              ))}
            </ul>
          </div>
        ) : null}
      </div>

      {/* Section-Level Feedback */}
      {report?.section_feedback && report.section_feedback.length > 0 && (
        <div>
          <div className="flex items-center space-x-2 mb-4">
            <FileText className="w-5 h-5 text-blue-600" />
            <h3 className="font-semibold text-gray-800 text-lg">Section-by-Section Analysis</h3>
          </div>
          <div className="space-y-3">
            {report.section_feedback.map((section, idx) => (
              <SectionCard key={idx} section={section} />
            ))}
          </div>
        </div>
      )}

      {/* Keyword Analysis */}
      {report?.keyword_analysis && (
        <div className="bg-white rounded-lg p-6 border border-gray-200">
          <div className="flex items-center space-x-2 mb-4">
            <Zap className="w-5 h-5 text-purple-600" />
            <h3 className="font-semibold text-gray-800">Keyword & Job Match Analysis</h3>
          </div>

          {report.keyword_analysis.extracted_keywords.length > 0 && (
            <div className="mb-4">
              <p className="text-sm font-medium text-gray-700 mb-2">Extracted Keywords</p>
              <div className="flex flex-wrap gap-2">
                {report.keyword_analysis.extracted_keywords.map((kw, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                  >
                    {kw}
                  </span>
                ))}
              </div>
            </div>
          )}

          {report.keyword_analysis.matched_keywords.length > 0 && (
            <div className="mb-4">
              <p className="text-sm font-medium text-green-700 mb-2">Matched Keywords</p>
              <div className="flex flex-wrap gap-2">
                {report.keyword_analysis.matched_keywords.map((kw, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs"
                  >
                    {kw}
                  </span>
                ))}
              </div>
            </div>
          )}

          {(report.keyword_analysis.missing_keywords.length > 0 ||
            (analysis.missing_keywords && analysis.missing_keywords.length > 0)) && (
            <div className="mb-4">
              <p className="text-sm font-medium text-red-700 mb-2">Missing Keywords (ATS Gaps)</p>
              <div className="flex flex-wrap gap-2">
                {(report.keyword_analysis.missing_keywords.length > 0
                  ? report.keyword_analysis.missing_keywords
                  : analysis.missing_keywords ?? []
                ).map((kw, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs"
                  >
                    {kw}
                  </span>
                ))}
              </div>
            </div>
          )}

          {report.keyword_analysis.recommendations.length > 0 && (
            <ul className="space-y-1 mt-3">
              {report.keyword_analysis.recommendations.map((rec, idx) => (
                <li key={idx} className="text-sm text-gray-700 flex items-start">
                  <span className="text-purple-500 mr-2">→</span>
                  {rec}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* Formatting Issues */}
      {report?.formatting_issues && report.formatting_issues.length > 0 && (
        <div className="bg-white rounded-lg p-6 border border-red-200">
          <div className="flex items-center space-x-2 mb-4">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <h3 className="font-semibold text-gray-800">ATS Formatting & Parsing Issues</h3>
          </div>
          <div className="space-y-3">
            {report.formatting_issues.map((issue, idx) => (
              <div key={idx} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <p className="font-medium text-gray-800">{issue.issue}</p>
                  <ImpactBadge impact={issue.ats_impact} />
                </div>
                <p className="text-sm text-gray-600 mb-2">{issue.description}</p>
                <p className="text-sm text-blue-700">
                  <span className="font-medium">Fix: </span>
                  {issue.recommendation}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Improvement Suggestions */}
      {report?.improvement_suggestions && report.improvement_suggestions.length > 0 && (
        <div className="bg-white rounded-lg p-6 border border-yellow-200">
          <div className="flex items-center space-x-2 mb-4">
            <Lightbulb className="w-5 h-5 text-yellow-600" />
            <h3 className="font-semibold text-gray-800">Content Improvement Suggestions</h3>
          </div>
          <div className="space-y-4">
            {report.improvement_suggestions.map((suggestion, idx) => (
              <div key={idx} className="border-l-4 border-yellow-400 pl-4">
                <div className="flex items-center space-x-2 mb-1">
                  <p className="font-medium text-gray-800">{suggestion.area}</p>
                  <ImpactBadge impact={suggestion.ats_impact} />
                </div>
                <p className="text-sm text-gray-600 mb-1">{suggestion.current_state}</p>
                <p className="text-sm text-gray-800">{suggestion.suggestion}</p>
                {suggestion.example && (
                  <p className="text-sm text-green-700 mt-2 bg-green-50 p-2 rounded">
                    Example: {suggestion.example}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Improvement Roadmap */}
      {report?.roadmap && report.roadmap.length > 0 && (
        <div>
          <div className="flex items-center space-x-2 mb-4">
            <Map className="w-5 h-5 text-indigo-600" />
            <h3 className="font-semibold text-gray-800 text-lg">Actionable Improvement Roadmap</h3>
          </div>
          <div className="space-y-3">
            {report.roadmap.map((item, idx) => (
              <RoadmapCard key={idx} item={item} />
            ))}
          </div>
        </div>
      )}

      {/* Fallback for legacy analyses without ats_report */}
      {!report && analysis.missing_keywords && analysis.missing_keywords.length > 0 && (
        <div className="bg-white rounded-lg p-6 border border-blue-200">
          <h3 className="font-semibold text-gray-800 mb-3">Missing Keywords</h3>
          <div className="flex flex-wrap gap-2">
            {analysis.missing_keywords.map((keyword, idx) => (
              <span
                key={idx}
                className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
              >
                {keyword}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
