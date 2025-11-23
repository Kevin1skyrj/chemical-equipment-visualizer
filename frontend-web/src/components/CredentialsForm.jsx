import { useState } from 'react'

const CredentialsForm = ({ credentials, onSave, onClear, onRefresh, apiBaseUrl }) => {
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
    <section className="bg-white border border-blue-100 rounded-xl p-6 shadow-lg">
      <header className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-wide text-blue-600 font-semibold">
            Login Required
          </p>
          <h2 className="text-lg font-semibold">Sign in to the Django API</h2>
          <p className="text-sm text-gray-600">
            Enter the Basic Auth username/password created with{' '}
            <code>python manage.py createsuperuser</code>. Requests are sent to{' '}
            <span className="font-semibold">{apiBaseUrl}</span>.
          </p>
          <p className="text-xs text-gray-500 mt-1">
            {credentials?.username ? (
              <span>
                Signed in as <strong>{credentials.username}</strong>
                {credentials?.source === 'env' && ' (deployment preset)'}.
              </span>
            ) : (
              'Not signed in yet. Save valid credentials to unlock uploads and history.'
            )}
          </p>
        </div>
        {credentials?.username && (
          <button
            type="button"
            onClick={() => {
              onClear?.()
              setStatus({ success: false, message: 'Credentials cleared.' })
            }}
            className="text-sm text-red-600 border border-red-200 rounded px-3 py-1 hover:bg-red-50 cursor-pointer"
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
            className="px-5 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors shadow-sm cursor-pointer"
          >
            Login &amp; Save
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
