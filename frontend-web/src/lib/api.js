import axios from 'axios'
import { getAuthCredentials } from './authStore.js'

const LOCAL_BASE_URL = 'http://127.0.0.1:8000/api'
const PROD_FALLBACK_BASE_URL = 'https://chemical-equipment-visualizer-batm.onrender.com/api'

const resolveBaseUrl = () => {
  if (import.meta?.env?.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }

  if (typeof window !== 'undefined') {
    const host = window.location.hostname
    if (host && host.includes('chemical-equipment-visualizer-inky.vercel.app')) {
      return PROD_FALLBACK_BASE_URL
    }
  }

  return LOCAL_BASE_URL
}

export const API_BASE_URL = resolveBaseUrl()

const client = axios.create({
  baseURL: API_BASE_URL,
})

client.interceptors.request.use((config) => {
  const credentials = getAuthCredentials()
  if (credentials?.username && credentials?.password) {
    const token = btoa(`${credentials.username}:${credentials.password}`)
    config.headers.Authorization = `Basic ${token}`
  } else if (config.headers.Authorization) {
    delete config.headers.Authorization
  }
  return config
})

export const uploadDataset = (formData) =>
  client.post('/datasets/upload/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

export const getLatestDataset = () => client.get('/datasets/latest/').then((res) => res.data)

export const getDatasetHistory = () => client.get('/datasets/history/').then((res) => res.data)

export const downloadDatasetReport = async (datasetId) => {
  const response = await client.get(`/datasets/${datasetId}/report/`, {
    responseType: 'blob',
  })
  return response.data
}

export const getDatasetDetail = (datasetId) =>
  client.get(`/datasets/${datasetId}/`).then((res) => res.data)
