import apiClient from './api'
import { LoginRequest, RegisterRequest, AuthResponse } from '../types'

export const authService = {
  login: async (credentials: LoginRequest): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/login', credentials)
    return response.data
  },

  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/register', data)
    return response.data
  },

  getCurrentUser: async () => {
    const response = await apiClient.get('/users/me')
    return response.data
  },

  updateProfile: async (data: any) => {
    const response = await apiClient.put('/users/me', data)
    return response.data
  },
}

export const resumeService = {
  uploadResume: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await apiClient.post('/resumes/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  listResumes: async () => {
    const response = await apiClient.get('/resumes/')
    return response.data
  },

  getResume: async (id: number) => {
    const response = await apiClient.get(`/resumes/${id}`)
    return response.data
  },

  deleteResume: async (id: number) => {
    await apiClient.delete(`/resumes/${id}`)
  },
}

export const jobDescriptionService = {
  createJobDescription: async (data: any) => {
    const response = await apiClient.post('/job-descriptions/', data)
    return response.data
  },

  uploadJobDescription: async (file: File, title: string, company?: string) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('title', title)
    if (company) formData.append('company', company)
    const response = await apiClient.post('/job-descriptions/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  listJobDescriptions: async () => {
    const response = await apiClient.get('/job-descriptions/')
    return response.data
  },

  getJobDescription: async (id: number) => {
    const response = await apiClient.get(`/job-descriptions/${id}`)
    return response.data
  },

  deleteJobDescription: async (id: number) => {
    await apiClient.delete(`/job-descriptions/${id}`)
  },
}

export const analysisService = {
  analyzeResume: async (resumeId: number, jobDescriptionId?: number) => {
    const response = await apiClient.post('/analysis/analyze', {
      resume_id: resumeId,
      job_description_id: jobDescriptionId,
    })
    return response.data
  },

  getAnalysis: async (id: number) => {
    const response = await apiClient.get(`/analysis/${id}`)
    return response.data
  },

  enhanceResume: async (analysisId: number) => {
    const response = await apiClient.post('/analysis/enhance', {
      analysis_id: analysisId,
    })
    return response.data
  },

  getEnhancedResume: async (id: number) => {
    const response = await apiClient.get(`/analysis/enhanced/${id}`)
    return response.data
  },
}
