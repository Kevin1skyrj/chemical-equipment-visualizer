import axios from 'axios'
import { getAuthCredentials } from './authStore'

const defaultBaseUrl = 'http://127.0.0.1:8000/api'
const baseURL = import.meta.env.VITE_API_BASE_URL || defaultBaseUrl

const client = axios.create({
  baseURL,
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
