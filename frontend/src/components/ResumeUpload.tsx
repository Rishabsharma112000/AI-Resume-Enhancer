import { useState } from 'react'
import { Upload, Loader } from 'lucide-react'
import toast from 'react-hot-toast'
import { resumeService } from '../services/authService'

interface ResumeUploadProps {
  onUploadSuccess: (resume: any) => void
}

export default function ResumeUpload({ onUploadSuccess }: ResumeUploadProps) {
  const [loading, setLoading] = useState(false)
  const [dragActive, setDragActive] = useState(false)

  const handleFile = async (file: File) => {
    if (!file.name.match(/\.(pdf|docx?|doc)$/i)) {
      toast.error('Only PDF and DOCX files are allowed')
      return
    }

    if (file.size > 10 * 1024 * 1024) {
      toast.error('File size must be less than 10MB')
      return
    }

    setLoading(true)
    try {
      const resume = await resumeService.uploadResume(file)
      toast.success('Resume uploaded successfully')
      onUploadSuccess(resume)
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to upload resume')
    } finally {
      setLoading(false)
    }
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const files = e.dataTransfer.files
    if (files && files[0]) {
      handleFile(files[0])
    }
  }

  return (
    <div
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      className={`border-2 border-dashed rounded-lg p-8 text-center transition ${
        dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
      }`}
    >
      <input
        type="file"
        id="resume-upload"
        className="hidden"
        accept=".pdf,.docx,.doc"
        onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
        disabled={loading}
      />

      {loading ? (
        <div className="flex items-center justify-center space-x-2">
          <Loader className="w-5 h-5 animate-spin" />
          <span>Uploading...</span>
        </div>
      ) : (
        <>
          <Upload className="w-10 h-10 mx-auto mb-3 text-gray-400" />
          <p className="mb-2 text-gray-700 font-medium">
            Drag and drop your resume here
          </p>
          <p className="text-gray-500 text-sm mb-4">
            Supported formats: PDF, DOCX (Max 10MB)
          </p>
          <label htmlFor="resume-upload" className="inline-block">
            <button
              type="button"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
              onClick={() => document.getElementById('resume-upload')?.click()}
            >
              Choose File
            </button>
          </label>
        </>
      )}
    </div>
  )
}
