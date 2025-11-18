import UploadForm from './components/UploadForm'
import LatestSummary from './components/LatestSummary'
import HistoryList from './components/HistoryList'
import CredentialsForm from './components/CredentialsForm'
import useDatasets from './hooks/useDatasets'
import useAuth from './hooks/useAuth'

const App = () => {
  const { credentials, saveCredentials, clearCredentials } = useAuth()
  const authKey =
    credentials?.username && credentials?.password
      ? `${credentials.username}:${credentials.password}`
      : null
  const { latest, history, isLoading, error, refresh } = useDatasets(authKey)
  const canUpload = Boolean(authKey)

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        <header>
          <p className="text-sm uppercase tracking-wide text-blue-600 font-semibold">
            Chemical Equipment Parameter Visualizer
          </p>
          <h1 className="text-3xl font-bold">Hybrid Web + Desktop Dashboard</h1>
          <p className="text-gray-600">
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
          onUploaded={refresh}
          disabled={!canUpload}
          disabledMessage="Add backend credentials above to enable uploads."
        />

        <LatestSummary dataset={latest} isLoading={isLoading} error={error} />

        <HistoryList history={history} onRefresh={refresh} />
      </div>
    </div>
  )
}

export default App