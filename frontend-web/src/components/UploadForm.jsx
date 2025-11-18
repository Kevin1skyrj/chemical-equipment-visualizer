import { useRef, useState } from 'react'
import { uploadDataset } from '../lib/api'

const UploadForm = ({ onUploaded, disabled = false, disabledMessage = '' }) => {
  const [name, setName] = useState('')
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState({ type: null, message: '' })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const fileInputRef = useRef(null)

  const resetForm = () => {
    setName('')
    setFile(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    if (disabled) {
      setStatus({ type: 'error', message: disabledMessage || 'Enter credentials first.' })
      return
    }
    if (!file) {
      setStatus({ type: 'error', message: 'Please select a CSV file.' })
      return
    }
    const formData = new FormData()
    formData.append('file', file)
    if (name.trim()) {
      formData.append('name', name.trim())
    }

    setIsSubmitting(true)
    setStatus({ type: null, message: '' })

    try {
      await uploadDataset(formData)
      setStatus({ type: 'success', message: 'Upload successful!' })
      resetForm()
      onUploaded?.()
    } catch (error) {
      const detail = error?.response?.data?.detail || error.message
      setStatus({ type: 'error', message: detail })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white shadow-sm rounded-lg p-4 border border-gray-100"
    >
      <h2 className="text-lg font-semibold mb-3">Upload CSV</h2>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="flex flex-col text-sm">
          Dataset Name (optional)
          <input
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            className="mt-1 rounded border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Sample Equipment Run"
          />
        </label>
        <div className="flex flex-col text-sm">
          <span>CSV File</span>
          <input
            ref={fileInputRef}
            id="dataset-file"
            type="file"
            accept=".csv"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
            className="sr-only"
          />
          <div className="mt-1 flex flex-wrap items-center gap-3">
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="px-3 py-2 border border-gray-300 rounded bg-white hover:bg-gray-50"
            >
              Choose File
            </button>
            <span className="text-sm text-gray-600">
              {file ? file.name : 'No file selected'}
            </span>
          </div>
        </div>
      </div>
      <div className="mt-4 flex items-center gap-3">
        <button
          type="submit"
          disabled={isSubmitting || disabled}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {isSubmitting ? 'Uploading…' : 'Upload'}
        </button>
        {status.message && (
          <p
            className={`text-sm ${
              status.type === 'error' ? 'text-red-600' : 'text-green-600'
            }`}
          >
            {status.message}
          </p>
        )}
      </div>
      {disabled && !status.message && (
        <p className="mt-2 text-sm text-amber-600">{disabledMessage}</p>
      )}
    </form>
  )
}

export default UploadForm
