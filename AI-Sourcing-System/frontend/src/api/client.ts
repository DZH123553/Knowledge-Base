import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 30000,
})

export default api

// Dashboard
export const getDashboardStats = () => api.get('/dashboard/stats')
export const getRecentActivity = () => api.get('/dashboard/recent-activity')
export const getSectorTop5 = () => api.get('/dashboard/sector-top5')

// Signals
export const listSignals = (params?: any) => api.get('/signals', { params })
export const getSignalStats = () => api.get('/signals/stats')
export const createSignal = (data: any) => api.post('/signals', data)

// Companies
export const listCompanies = (params?: any) => api.get('/companies', { params })
export const getCompanyStats = () => api.get('/companies/stats')
export const createCompany = (data: any) => api.post('/companies', data)
export const updateCompany = (id: string, data: any) => api.patch(`/companies/${id}`, data)

// IC Meetings
export const listICMeetings = (params?: any) => api.get('/ic-meetings', { params })
export const getWeeklyRanking = (week?: number) => api.get('/ic-meetings/weekly-ranking', { params: { week } })

// Reports
export const listInvestmentReports = (params?: any) => api.get('/reports/investment', { params })
export const listRiskReports = (params?: any) => api.get('/reports/risk', { params })

// Agents
export const getAgentConfig = () => api.get('/agents/config')
export const processSignal = (signalId: string) => api.post(`/agents/process-signal/${signalId}`)
export const autoTriggerIC = (data: any) => api.post('/agents/auto-ic', data)
export const submitHumanFeedback = (data: any) => api.post('/agents/human-feedback', data)
export const batchProcess = (data: any) => api.post('/agents/batch-process', data)
