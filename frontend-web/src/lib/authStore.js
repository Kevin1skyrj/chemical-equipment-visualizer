const STORAGE_KEY = 'cev-basic-auth'

let runtimeCredentials = null

const readFromStorage = () => {
  if (typeof window === 'undefined') {
    return null
  }
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    const parsed = JSON.parse(raw)
    if (parsed?.username && parsed?.password) {
      return parsed
    }
  } catch (error) {
    console.warn('Failed to parse stored credentials', error)
  }
  return null
}

export const getAuthCredentials = () => {
  if (runtimeCredentials?.username && runtimeCredentials?.password) {
    return runtimeCredentials
  }
  const stored = readFromStorage()
  if (stored) {
    runtimeCredentials = stored
    return stored
  }
  return null
}

export const setAuthCredentials = (username, password) => {
  if (!username || !password) {
    return clearAuthCredentials()
  }
  runtimeCredentials = { username, password, source: 'user' }
  if (typeof window !== 'undefined') {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(runtimeCredentials))
  }
  return runtimeCredentials
}

export const clearAuthCredentials = () => {
  runtimeCredentials = null
  if (typeof window !== 'undefined') {
    window.localStorage.removeItem(STORAGE_KEY)
  }
  return null
}
