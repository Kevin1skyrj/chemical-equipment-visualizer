import { useMemo, useState } from 'react'
import UploadForm from './components/UploadForm'
import LatestSummary from './components/LatestSummary'
import HistoryList from './components/HistoryList'
import LoginScreen from './components/LoginScreen'
import useDatasets from './hooks/useDatasets.js'
import useAuth from './hooks/useAuth.js'
import { API_BASE_URL } from './lib/api.js'

const HAS_UPLOAD_KEY = 'cev-has-uploaded'

const App = () => {
  const { credentials, saveCredentials, clearCredentials } = useAuth()
  const authKey =
    credentials?.username && credentials?.password
      ? `${credentials.username}:${credentials.password}`
      : null
  const isAuthenticated = Boolean(authKey)
  const { latest, history, isLoading, error, refresh } = useDatasets(isAuthenticated ? authKey : null)
  const [hasUploaded, setHasUploaded] = useState(() => {
    if (typeof window === 'undefined') return false
    return localStorage.getItem(HAS_UPLOAD_KEY) === 'true'
  })
  const canUpload = isAuthenticated

  const latestForViewer = useMemo(() => (hasUploaded ? latest : null), [hasUploaded, latest])

  const handleUploadSuccess = () => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(HAS_UPLOAD_KEY, 'true')
    }
    setHasUploaded(true)
    refresh()
  }

  const handleSignOut = () => {
    clearCredentials()
    if (typeof window !== 'undefined') {
      localStorage.removeItem(HAS_UPLOAD_KEY)
    }
    setHasUploaded(false)
    refresh()
  }

  if (!isAuthenticated) {
    return <LoginScreen onSave={saveCredentials} />
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-gray-50 to-blue-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        {credentials?.username && (
          <div className="flex justify-end">
            <button
              type="button"
              onClick={handleSignOut}
              className="inline-flex items-center gap-2 rounded-full border border-blue-200 bg-white/90 px-4 py-1.5 text-sm font-semibold text-blue-700 shadow-sm transition hover:border-blue-400 hover:bg-white hover:text-blue-900"
            >
              <span className="h-2 w-2 rounded-full bg-green-500" aria-hidden="true" />
              Signed in as {credentials.username}
              <span className="text-gray-400" aria-hidden="true">
                ·
              </span>
              <span className="underline">Sign out</span>
            </button>
          </div>
        )}
        <header className="text-center space-y-3 mb-6 bg-white rounded-2xl p-8 shadow-xl border border-blue-100">
          <div className="inline-block bg-blue-100 px-4 py-2 rounded-full mb-2">
            <p className="text-sm uppercase tracking-widest text-blue-700 font-bold">
              Chemical Equipment Parameter Visualizer
            </p>
          </div>
          <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 tracking-tight">
            Hybrid Web + Desktop Dashboard
          </h1>
          <p className="text-lg md:text-xl text-gray-600 max-w-2xl mx-auto">
            Upload CSV files, review analytics, and download PDF insights.
          </p>
        </header>

        <UploadForm
          onUploaded={handleUploadSuccess}
          disabled={!canUpload}
          disabledMessage="Sign in to enable uploads."
        />

        <LatestSummary dataset={latestForViewer} isLoading={isLoading} error={error} />

        <HistoryList history={history} onRefresh={refresh} />
      </div>
    </div>
  )
}

export default App