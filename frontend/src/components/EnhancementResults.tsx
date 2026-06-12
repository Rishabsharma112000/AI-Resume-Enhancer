import { useState } from 'react'
import { Download, ArrowLeftRight, Sparkles, ChevronDown, ChevronUp } from 'lucide-react'
import { EnhancedResume } from '../types'

interface EnhancementResultsProps {
  enhanced: EnhancedResume
  originalAtsScore?: number
}

function downloadText(content: string, filename: string) {
  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

export default function EnhancementResults({
  enhanced,
  originalAtsScore,
}: EnhancementResultsProps) {
  const [viewMode, setViewMode] = useState<'enhanced' | 'original' | 'compare'>('compare')
  const [expandedChanges, setExpandedChanges] = useState<Record<number, boolean>>({})

  const content = enhanced.enhanced_full_content || ''
  const original = enhanced.original_content || ''

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-emerald-500 to-teal-600 text-white rounded-lg p-6">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <Sparkles className="w-5 h-5" />
              <p className="text-emerald-100 text-sm font-medium">AI-Enhanced Resume Ready</p>
            </div>
            <p className="text-2xl font-bold">Version {enhanced.version}</p>
            {enhanced.estimated_ats_score_gain ? (
              <p className="text-emerald-100 text-sm mt-1">
                Estimated ATS score gain: +{enhanced.estimated_ats_score_gain} points
                {originalAtsScore ? ` (from ${Math.round(originalAtsScore)})` : ''}
              </p>
            ) : null}
          </div>
          <button
            onClick={() =>
              downloadText(
                content,
                `enhanced-resume-v${enhanced.version}.txt`
              )
            }
            disabled={!content}
            className="flex items-center space-x-2 px-5 py-3 bg-white text-emerald-700 rounded-lg hover:bg-emerald-50 transition font-medium disabled:opacity-50"
          >
            <Download className="w-5 h-5" />
            <span>Download Enhanced Resume</span>
          </button>
        </div>
      </div>

      <div className="flex space-x-2 border-b border-gray-200 pb-2">
        {(['compare', 'enhanced', 'original'] as const).map((mode) => (
          <button
            key={mode}
            onClick={() => setViewMode(mode)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
              viewMode === mode
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {mode === 'compare' ? 'Before vs After' : mode === 'enhanced' ? 'Enhanced' : 'Original'}
          </button>
        ))}
      </div>

      {viewMode === 'compare' ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div className="bg-white rounded-lg border border-orange-200 p-4">
            <div className="flex items-center space-x-2 mb-3">
              <ArrowLeftRight className="w-4 h-4 text-orange-600" />
              <h4 className="font-semibold text-gray-800">Before (Original)</h4>
            </div>
            <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans max-h-96 overflow-y-auto bg-orange-50 p-3 rounded">
              {original || 'Original content not available'}
            </pre>
          </div>
          <div className="bg-white rounded-lg border border-green-200 p-4">
            <div className="flex items-center space-x-2 mb-3">
              <Sparkles className="w-4 h-4 text-green-600" />
              <h4 className="font-semibold text-gray-800">After (Enhanced)</h4>
            </div>
            <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans max-h-96 overflow-y-auto bg-green-50 p-3 rounded">
              {content || 'Enhanced content not available'}
            </pre>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans max-h-[500px] overflow-y-auto">
            {viewMode === 'enhanced' ? content : original}
          </pre>
        </div>
      )}

      {enhanced.improvements_made && enhanced.improvements_made.length > 0 && (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="font-semibold text-gray-800 mb-4">Changes Made ({enhanced.improvements_made.length})</h3>
          <div className="space-y-3">
            {enhanced.improvements_made.map((change, idx) => (
              <div key={idx} className="border border-gray-200 rounded-lg overflow-hidden">
                <button
                  onClick={() =>
                    setExpandedChanges((prev) => ({ ...prev, [idx]: !prev[idx] }))
                  }
                  className="w-full p-4 flex items-center justify-between hover:bg-gray-50 transition text-left"
                >
                  <div>
                    <span className="text-xs font-medium text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
                      {change.section}
                    </span>
                    <p className="font-medium text-gray-800 mt-1">{change.change}</p>
                  </div>
                  {expandedChanges[idx] ? (
                    <ChevronUp className="w-5 h-5 text-gray-400 shrink-0" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-gray-400 shrink-0" />
                  )}
                </button>
                {expandedChanges[idx] && (change.before || change.after) && (
                  <div className="px-4 pb-4 grid grid-cols-1 md:grid-cols-2 gap-3 border-t border-gray-100 pt-3">
                    {change.before && (
                      <div className="bg-orange-50 p-3 rounded text-sm">
                        <p className="text-xs font-medium text-orange-700 mb-1">Before</p>
                        <p className="text-gray-700 whitespace-pre-wrap">{change.before}</p>
                      </div>
                    )}
                    {change.after && (
                      <div className="bg-green-50 p-3 rounded text-sm">
                        <p className="text-xs font-medium text-green-700 mb-1">After</p>
                        <p className="text-gray-700 whitespace-pre-wrap">{change.after}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
