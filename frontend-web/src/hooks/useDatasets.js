import { useCallback, useEffect, useState } from 'react'
import { API_BASE_URL, getDatasetHistory, getLatestDataset } from '../lib/api.js'

const initialState = {
  latest: null,
  history: [],
  isLoading: false,
  error: null,
}

const useDatasets = (authKey) => {
  const [state, setState] = useState(initialState)

  const loadData = useCallback(async () => {
    if (!authKey) {
      setState({ ...initialState, error: 'Enter backend credentials to fetch data.' })
      return
    }
    setState((prev) => ({ ...prev, isLoading: true, error: null }))
    try {
      const [latestResponse, historyResponse] = await Promise.allSettled([
        getLatestDataset(),
        getDatasetHistory(),
      ])

      const latest =
        latestResponse.status === 'fulfilled' ? latestResponse.value : null
      const history =
        historyResponse.status === 'fulfilled' ? historyResponse.value : []

      setState({ latest, history, isLoading: false, error: null })
    } catch (error) {
      let message = 'Unable to fetch datasets. Please try again.'
      if (error?.response?.status === 401) {
        message = 'Invalid username or password. Double-check your Django credentials.'
      } else if (error?.message === 'Network Error') {
        message = `Cannot reach backend at ${API_BASE_URL}. Is it running and reachable?`
      } else if (error?.response?.data?.detail) {
        message = error.response.data.detail
      }
      setState({ ...initialState, error: message, isLoading: false })
    }
  }, [authKey])

  useEffect(() => {
    const id = setTimeout(() => {
      loadData()
    }, 0)

    return () => clearTimeout(id)
  }, [loadData])

  return { ...state, refresh: loadData }
}

export default useDatasets
