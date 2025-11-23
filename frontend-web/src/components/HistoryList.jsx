import { downloadDatasetReport, getDatasetDetail } from '../lib/api'
import { useState } from 'react'

const HistoryList = ({ history = [], onRefresh }) => {
  const [selectedDataset, setSelectedDataset] = useState(null)
  const [downloadingIds, setDownloadingIds] = useState(new Set())
  const [error, setError] = useState('')

  const handleDownload = async (dataset) => {
    try {
      setDownloadingIds((prev) => new Set(prev).add(dataset.id))
      const blob = await downloadDatasetReport(dataset.id)
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      const timestamp = new Date(dataset.uploaded_at).toISOString().replace(/[:.]/g, '-')
      link.href = url
      link.download = `${dataset.name || 'dataset'}-${timestamp}.pdf`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (err) {
      setError(err.message)
    } finally {
      setDownloadingIds((prev) => {
        const next = new Set(prev)
        next.delete(dataset.id)
        return next
      })
    }
  }

  const handleSelectDataset = async (dataset) => {
    try {
      setError('')
      const detail = await getDatasetDetail(dataset.id)
      setSelectedDataset(detail)
    } catch (err) {
      setError(err.message)
    }
  }

  if (!history.length) {
    return null
  }

  return (
    <section className="bg-white rounded-xl shadow-lg border border-gray-100 p-6">
      <header className="flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">Upload History</h2>
        <button
          onClick={onRefresh}
          className="text-sm text-blue-600 hover:text-blue-700 cursor-pointer font-medium"
        >
          Refresh
        </button>
      </header>

      {error && <p className="text-sm text-red-600 mt-2">{error}</p>}

      <div className="mt-4 grid gap-3 md:grid-cols-2">
        {history.map((dataset) => (
          <article
            key={dataset.id}
            className={`border rounded-xl p-4 transition-all hover:shadow-md ${
              selectedDataset?.id === dataset.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
            }`}
          >
            <p className="text-sm text-gray-500">
              {new Date(dataset.uploaded_at).toLocaleString()}
            </p>
            <h3 className="font-semibold">{dataset.name}</h3>
            <p className="text-sm text-gray-600">
              Total Records: {dataset.total_records} | Avg Temp: {dataset.avg_temperature}
            </p>
            <div className="flex flex-wrap gap-2 mt-3">
              <button
                onClick={() => handleSelectDataset(dataset)}
                className="text-sm px-3 py-1.5 border border-blue-600 text-blue-600 rounded-lg font-medium hover:bg-blue-50 transition-colors cursor-pointer"
              >
                View Detail
              </button>
              <button
                onClick={() => handleDownload(dataset)}
                disabled={downloadingIds.has(dataset.id)}
                className="text-sm px-3 py-1.5 border border-gray-300 rounded-lg font-medium hover:bg-gray-50 disabled:opacity-60 disabled:cursor-not-allowed transition-colors cursor-pointer"
              >
                {downloadingIds.has(dataset.id) ? 'Preparing…' : 'PDF Report'}
              </button>
            </div>
          </article>
        ))}
      </div>

      {selectedDataset && (
        <div className="mt-4 border-t pt-4">
          <h3 className="font-semibold">{selectedDataset.name} (Detail)</h3>
          <pre className="mt-2 bg-gray-50 p-3 rounded text-xs overflow-auto max-h-64">
            {JSON.stringify(selectedDataset.metrics, null, 2)}
          </pre>
        </div>
      )}
    </section>
  )
}

export default HistoryList
