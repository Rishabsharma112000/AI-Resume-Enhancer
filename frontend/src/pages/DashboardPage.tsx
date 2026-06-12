import { useState, useEffect } from 'react'
import { Loader } from 'lucide-react'
import toast from 'react-hot-toast'
import { resumeService, analysisService, jobDescriptionService } from '../services/authService'
import { Resume, ResumeAnalysis, JobDescription } from '../types'
import ResumeUpload from '../components/ResumeUpload'
import ResumeList from '../components/ResumeList'
import AnalysisResults from '../components/AnalysisResults'
import JobDescriptionForm from '../components/JobDescriptionForm'

export default function DashboardPage() {
  const [resumes, setResumes] = useState<Resume[]>([])
  const [jobDescriptions, setJobDescriptions] = useState<JobDescription[]>([])
  const [selectedResume, setSelectedResume] = useState<Resume | null>(null)
  const [selectedJD, setSelectedJD] = useState<JobDescription | null>(null)
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null)
  const [loading, setLoading] = useState(false)
  const [tab, setTab] = useState<'upload' | 'analyze'>('upload')

  useEffect(() => {
    loadResumes()
    loadJobDescriptions()
  }, [])

  const loadResumes = async () => {
    try {
      const data = await resumeService.listResumes()
      setResumes(data)
    } catch (error) {
      toast.error('Failed to load resumes')
    }
  }

  const loadJobDescriptions = async () => {
    try {
      const data = await jobDescriptionService.listJobDescriptions()
      setJobDescriptions(data)
    } catch (error) {
      toast.error('Failed to load job descriptions')
    }
  }

  const handleAnalyze = async () => {
    if (!selectedResume) {
      toast.error('Please select a resume')
      return
    }

    setLoading(true)
    try {
      const result = await analysisService.analyzeResume(
        selectedResume.id,
        selectedJD?.id
      )
      setAnalysis(result)
      toast.success('Analysis completed')
    } catch (error: any) {
      toast.error('Failed to analyze resume')
    } finally {
      setLoading(false)
    }
  }

  const handleEnhance = async () => {
    if (!analysis) {
      toast.error('Please analyze resume first')
      return
    }

    setLoading(true)
    try {
      await analysisService.enhanceResume(analysis.id)
      toast.success('Resume enhanced! Ready to download.')
      // You can add download functionality here
    } catch (error: any) {
      toast.error('Failed to enhance resume')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Resume Enhancer Dashboard</h1>

      {/* Tabs */}
      <div className="flex space-x-4 mb-6 border-b border-gray-200">
        <button
          onClick={() => setTab('upload')}
          className={`pb-2 font-medium ${
            tab === 'upload'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          Upload Resume
        </button>
        <button
          onClick={() => setTab('analyze')}
          className={`pb-2 font-medium ${
            tab === 'analyze'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          Analyze
        </button>
      </div>

      {tab === 'upload' ? (
        <div className="space-y-8">
          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Upload Your Resume</h2>
            <ResumeUpload onUploadSuccess={(resume) => {
              setResumes([...resumes, resume])
              toast.success('Resume uploaded successfully!')
            }} />
          </div>

          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Resumes</h2>
            <ResumeList
              resumes={resumes}
              onDelete={(id) => setResumes(resumes.filter((r) => r.id !== id))}
              onSelect={(resume) => {
                setSelectedResume(resume)
                setTab('analyze')
              }}
            />
          </div>

          <div>
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Job Descriptions</h2>
            <JobDescriptionForm onSuccess={(jd) => {
              setJobDescriptions([...jobDescriptions, jd])
            }} />
            
            {jobDescriptions.length > 0 && (
              <div className="mt-4 space-y-2">
                {jobDescriptions.map((jd) => (
                  <div
                    key={jd.id}
                    onClick={() => setSelectedJD(jd)}
                    className={`p-4 rounded-lg border-2 cursor-pointer transition ${
                      selectedJD?.id === jd.id
                        ? 'border-blue-600 bg-blue-50'
                        : 'border-gray-200 hover:border-blue-400'
                    }`}
                  >
                    <p className="font-medium text-gray-800">{jd.title}</p>
                    {jd.company && <p className="text-sm text-gray-600">{jd.company}</p>}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Resume Selection */}
          <div className="bg-white rounded-lg p-6 border border-gray-200">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Select Resume to Analyze</h2>
            {resumes.length === 0 ? (
              <p className="text-gray-500">No resumes available. Please upload one first.</p>
            ) : (
              <div className="space-y-2">
                {resumes.map((resume) => (
                  <button
                    key={resume.id}
                    onClick={() => setSelectedResume(resume)}
                    className={`w-full p-4 rounded-lg border-2 text-left transition ${
                      selectedResume?.id === resume.id
                        ? 'border-blue-600 bg-blue-50'
                        : 'border-gray-200 hover:border-blue-400'
                    }`}
                  >
                    <p className="font-medium text-gray-800">{resume.original_filename}</p>
                    <p className="text-sm text-gray-600">{(resume.file_size / 1024).toFixed(2)} KB</p>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Job Description Selection */}
          <div className="bg-white rounded-lg p-6 border border-gray-200">
            <h2 className="text-lg font-semibold text-gray-800 mb-2">Job Description (Optional)</h2>
            <p className="text-sm text-gray-500 mb-4">
              Select a job description for targeted keyword matching and ATS relevance scoring.
            </p>
            {jobDescriptions.length === 0 ? (
              <p className="text-gray-500 text-sm">
                No job descriptions available. Add one on the Upload tab for keyword analysis.
              </p>
            ) : (
              <div className="space-y-2">
                <button
                  onClick={() => setSelectedJD(null)}
                  className={`w-full p-3 rounded-lg border-2 text-left transition ${
                    !selectedJD
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-gray-200 hover:border-blue-400'
                  }`}
                >
                  <p className="font-medium text-gray-800">No job description</p>
                  <p className="text-sm text-gray-500">General ATS analysis only</p>
                </button>
                {jobDescriptions.map((jd) => (
                  <button
                    key={jd.id}
                    onClick={() => setSelectedJD(jd)}
                    className={`w-full p-3 rounded-lg border-2 text-left transition ${
                      selectedJD?.id === jd.id
                        ? 'border-blue-600 bg-blue-50'
                        : 'border-gray-200 hover:border-blue-400'
                    }`}
                  >
                    <p className="font-medium text-gray-800">{jd.title}</p>
                    {jd.company && <p className="text-sm text-gray-600">{jd.company}</p>}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Analysis Buttons */}
          <div className="flex space-x-4">
            <button
              onClick={handleAnalyze}
              disabled={loading || !selectedResume}
              className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 flex items-center justify-center space-x-2 font-medium"
            >
              {loading ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <span>Analyze Resume</span>
              )}
            </button>

            {analysis && (
              <button
                onClick={handleEnhance}
                disabled={loading}
                className="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition disabled:opacity-50 font-medium"
              >
                {loading ? 'Enhancing...' : 'Enhance Resume'}
              </button>
            )}
          </div>

          {/* Analysis Results */}
          {analysis && (
            <div>
              <h2 className="text-lg font-semibold text-gray-800 mb-4">Analysis Results</h2>
              <AnalysisResults analysis={analysis} />
            </div>
          )}
        </div>
      )}
    </div>
  )
}
