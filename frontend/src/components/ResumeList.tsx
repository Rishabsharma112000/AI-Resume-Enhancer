import { useState } from 'react'
import { Trash2, Eye } from 'lucide-react'
import toast from 'react-hot-toast'
import { resumeService } from '../services/authService'
import { Resume } from '../types'

interface ResumeListProps {
  resumes: Resume[]
  onDelete: (id: number) => void
  onSelect: (resume: Resume) => void
}

export default function ResumeList({ resumes, onDelete, onSelect }: ResumeListProps) {
  const [deleting, setDeleting] = useState<number | null>(null)

  const handleDelete = async (id: number) => {
    setDeleting(id)
    try {
      await resumeService.deleteResume(id)
      toast.success('Resume deleted')
      onDelete(id)
    } catch (error: any) {
      toast.error('Failed to delete resume')
    } finally {
      setDeleting(null)
    }
  }

  if (resumes.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No resumes uploaded yet</p>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      {resumes.map((resume) => (
        <div
          key={resume.id}
          className="flex items-center justify-between p-4 bg-white rounded-lg border border-gray-200 hover:shadow-md transition"
        >
          <div className="flex-1">
            <p className="font-medium text-gray-800">{resume.original_filename}</p>
            <p className="text-sm text-gray-500">
              {(resume.file_size / 1024).toFixed(2)} KB • {resume.file_type.toUpperCase()}
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => onSelect(resume)}
              className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition"
              title="Analyze"
            >
              <Eye className="w-5 h-5" />
            </button>
            <button
              onClick={() => handleDelete(resume.id)}
              disabled={deleting === resume.id}
              className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition disabled:opacity-50"
              title="Delete"
            >
              <Trash2 className="w-5 h-5" />
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
