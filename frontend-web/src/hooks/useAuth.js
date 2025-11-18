import { useCallback, useEffect, useState } from 'react'
import {
  clearAuthCredentials,
  getAuthCredentials,
  setAuthCredentials,
} from '../lib/authStore'

const useAuth = () => {
  const [credentials, setCredentials] = useState(() => getAuthCredentials())

  useEffect(() => {
    setCredentials(getAuthCredentials())
  }, [])

  const save = useCallback((username, password) => {
    const trimmedUser = username?.trim()
    const trimmedPass = password?.trim()
    if (!trimmedUser || !trimmedPass) {
      setCredentials(clearAuthCredentials())
      return { success: false, message: 'Username and password are required.' }
    }
    const stored = setAuthCredentials(trimmedUser, trimmedPass)
    setCredentials(stored)
    return { success: true, message: 'Credentials saved. They are stored locally in this browser.' }
  }, [])

  const reset = useCallback(() => {
    setCredentials(clearAuthCredentials())
  }, [])

  return {
    credentials,
    saveCredentials: save,
    clearCredentials: reset,
  }
}

export default useAuth
