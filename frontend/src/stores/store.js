import { create } from 'zustand'

export const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('access_token'),
  setUser: (user) => set({ user }),
  setToken: (token) => {
    localStorage.setItem('access_token', token)
    set({ token })
  },
  logout: () => {
    localStorage.removeItem('access_token')
    set({ user: null, token: null })
  },
}))

export const useDeviceStore = create((set) => ({
  devices: [],
  loading: false,
  setDevices: (devices) => set({ devices }),
  setLoading: (loading) => set({ loading }),
}))

export const useTestStore = create((set) => ({
  tests: [],
  results: [],
  loading: false,
  setTests: (tests) => set({ tests }),
  setResults: (results) => set({ results }),
  setLoading: (loading) => set({ loading }),
}))

export const useReportStore = create((set) => ({
  reports: [],
  loading: false,
  setReports: (reports) => set({ reports }),
  setLoading: (loading) => set({ loading }),
}))
