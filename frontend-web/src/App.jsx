import { useMemo, useState } from 'react'
import UploadForm from './components/UploadForm'
import LatestSummary from './components/LatestSummary'
import HistoryList from './components/HistoryList'
import CredentialsForm from './components/CredentialsForm'
import useDatasets from './hooks/useDatasets'
import useAuth from './hooks/useAuth'

const HAS_UPLOAD_KEY = 'cev-has-uploaded'

const App = () => {
  const { credentials, saveCredentials, clearCredentials } = useAuth()
  const authKey =
    credentials?.username && credentials?.password
      ? `${credentials.username}:${credentials.password}`
      : null
  const { latest, history, isLoading, error, refresh } = useDatasets(authKey)
  const [hasUploaded, setHasUploaded] = useState(() => {
    if (typeof window === 'undefined') return false
    return localStorage.getItem(HAS_UPLOAD_KEY) === 'true'
  })
  const canUpload = Boolean(authKey)

  const latestForViewer = useMemo(() => (hasUploaded ? latest : null), [hasUploaded, latest])

  const handleUploadSuccess = () => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(HAS_UPLOAD_KEY, 'true')
    }
    setHasUploaded(true)
    refresh()
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto space-y-8">
        <header className="text-center space-y-2 mb-4">
          <p className="text-xs uppercase tracking-widest text-blue-600 font-semibold">
            Chemical Equipment Parameter Visualizer
          </p>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 tracking-tight">
            Hybrid Web + Desktop Dashboard
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Upload CSV files, review analytics, and download PDF insights.
          </p>
        </header>

        <CredentialsForm
          credentials={credentials}
          onSave={saveCredentials}
          onClear={() => {
            clearCredentials()
            refresh()
          }}
          onRefresh={refresh}
        />

        <UploadForm
          onUploaded={handleUploadSuccess}
          disabled={!canUpload}
          disabledMessage="Add backend credentials above to enable uploads."
        />

        <LatestSummary dataset={latestForViewer} isLoading={isLoading} error={error} />

        <HistoryList history={history} onRefresh={refresh} />
      </div>
    </div>
  )
}

export default App