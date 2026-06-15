import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authService = {
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
  register: (user) => api.post('/auth/register', user),
  logout: () => api.post('/auth/logout'),
}

export const deviceService = {
  getAll: () => api.get('/devices/'),
  getById: (id) => api.get(`/devices/${id}`),
  create: (device) => api.post('/devices/', device),
  update: (id, device) => api.put(`/devices/${id}`, device),
  delete: (id) => api.delete(`/devices/${id}`),
  testConnectivity: (id) => api.post(`/devices/${id}/test-connectivity`),
}

export const testService = {
  run: (testId, deviceId) =>
    api.post('/tests/run', { test_case_id: testId, device_id: deviceId }),
  getHistory: () => api.get('/tests/history'),
}

export const reportService = {
  getAll: () => api.get('/reports/'),
  getById: (id) => api.get(`/reports/${id}`),
  generate: (report) => api.post('/reports/generate', report),
  export: (id, format) => api.get(`/reports/${id}/export?format=${format}`),
}

export const alertService = {
  getAll: () => api.get('/alerts/'),
  getById: (id) => api.get(`/alerts/${id}`),
  update: (id, alert) => api.put(`/alerts/${id}`, alert),
}

export const healthService = {
  check: () => api.get('/health/'),
  dashboard: () => api.get('/health/dashboard'),
}

export default api
