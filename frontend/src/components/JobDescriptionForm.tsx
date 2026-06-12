import { useState } from 'react'
import { Upload, Plus } from 'lucide-react'
import toast from 'react-hot-toast'
import { jobDescriptionService } from '../services/authService'

interface JobDescriptionFormProps {
  onSuccess: (jd: any) => void
}

export default function JobDescriptionForm({ onSuccess }: JobDescriptionFormProps) {
  const [tab, setTab] = useState<'text' | 'file'>('text')
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    content: '',
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.title || !formData.content) {
      toast.error('Please fill in title and content')
      return
    }

    setLoading(true)
    try {
      const jd = await jobDescriptionService.createJobDescription(formData)
      toast.success('Job description created')
      onSuccess(jd)
      setFormData({ title: '', company: '', content: '' })
    } catch (error: any) {
      toast.error('Failed to create job description')
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setLoading(true)
    try {
      const jd = await jobDescriptionService.uploadJobDescription(
        file,
        formData.title || file.name,
        formData.company
      )
      toast.success('Job description uploaded')
      onSuccess(jd)
      setFormData({ title: '', company: '', content: '' })
    } catch (error: any) {
      toast.error('Failed to upload job description')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Add Job Description</h3>

      {/* Tabs */}
      <div className="flex space-x-4 mb-6 border-b border-gray-200">
        <button
          onClick={() => setTab('text')}
          className={`pb-2 font-medium ${
            tab === 'text'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          Paste Text
        </button>
        <button
          onClick={() => setTab('file')}
          className={`pb-2 font-medium ${
            tab === 'file'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          Upload File
        </button>
      </div>

      {tab === 'text' ? (
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            name="title"
            placeholder="Job Title"
            value={formData.title}
            onChange={handleInputChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
            required
          />

          <input
            type="text"
            name="company"
            placeholder="Company (Optional)"
            value={formData.company}
            onChange={handleInputChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
          />

          <textarea
            name="content"
            placeholder="Paste job description here..."
            value={formData.content}
            onChange={handleInputChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 h-32 resize-none"
            required
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50 flex items-center justify-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>{loading ? 'Creating...' : 'Add Job Description'}</span>
          </button>
        </form>
      ) : (
        <div>
          <input
            type="text"
            name="title"
            placeholder="Job Title"
            value={formData.title}
            onChange={handleInputChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 mb-4"
            required
          />

          <input
            type="text"
            name="company"
            placeholder="Company (Optional)"
            value={formData.company}
            onChange={handleInputChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 mb-4"
          />

          <label className="flex items-center justify-center w-full px-4 py-8 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-blue-500 transition">
            <div className="flex items-center space-x-2 text-gray-600">
              <Upload className="w-5 h-5" />
              <span>Click to upload or drag</span>
            </div>
            <input
              type="file"
              className="hidden"
              accept=".pdf,.docx,.doc"
              onChange={handleFileUpload}
              disabled={loading}
            />
          </label>
        </div>
      )}
    </div>
  )
}
