import { useCallback, useEffect, useState } from 'react'
import { getDatasetHistory, getLatestDataset } from '../lib/api.js'

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
      setState({ ...initialState, error: error.message, isLoading: false })
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
