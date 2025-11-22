import { useState } from 'react'

const CredentialsForm = ({ credentials, onSave, onClear, onRefresh }) => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [status, setStatus] = useState(null)

  const handleSubmit = (event) => {
    event.preventDefault()
    const result = onSave?.(username, password)
    setStatus(result)
    if (result?.success) {
      setUsername('')
      setPassword('')
      onRefresh?.()
    }
  }

  return (
    <section className="bg-white border border-blue-100 rounded-lg p-4 shadow-sm">
      <header className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-wide text-blue-600 font-semibold">
            Backend Authentication
          </p>
          <h2 className="text-lg font-semibold">Connect to Django API</h2>
          <p className="text-sm text-gray-600">
            Use the Basic Auth account you created via{' '}
            <code>python manage.py createsuperuser</code>. The exact reviewer/demo values are
            documented in the README under “Demo Credentials”. Stored locally in this browser only.
            {credentials?.username && (
              <span className="ml-1 text-gray-700 font-medium">
                Currently connected as {credentials.username}.
              </span>
            )}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            Need access? Ask your admin for the shared username/password or create a new Django
            superuser and share it via the screening submission form.
          </p>
        </div>
        {credentials?.username && (
          <button
            type="button"
            onClick={() => {
              onClear?.()
              setStatus({ success: false, message: 'Credentials cleared.' })
            }}
            className="text-sm text-red-600 border border-red-200 rounded px-3 py-1 hover:bg-red-50"
          >
            Clear
          </button>
        )}
      </header>
      <form onSubmit={handleSubmit} className="mt-4 grid gap-3 md:grid-cols-2">
        <label className="text-sm flex flex-col">
          Username
          <input
            type="text"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            className="mt-1 rounded border border-gray-300 px-3 py-2"
            placeholder="admin"
          />
        </label>
        <label className="text-sm flex flex-col">
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            className="mt-1 rounded border border-gray-300 px-3 py-2"
            placeholder="••••••••"
          />
        </label>
        <div className="md:col-span-2 flex items-center gap-3">
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Save Credentials
          </button>
          {status?.message && (
            <span
              className={`text-sm ${status.success ? 'text-green-600' : 'text-red-600'}`}
            >
              {status.message}
            </span>
          )}
        </div>
      </form>
    </section>
  )
}

export default CredentialsForm
