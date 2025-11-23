import { useMemo, useState } from 'react'
import { verifyCredentials } from '../lib/api.js'

const LoginScreen = ({ onSave }) => {
  const presetCredentials = useMemo(() => {
    const presetUser = import.meta.env?.VITE_API_USERNAME?.trim()
    const presetPass = import.meta.env?.VITE_API_PASSWORD?.trim()
    if (presetUser && presetPass) {
      return { username: presetUser, password: presetPass }
    }
    return null
  }, [])

  const [username, setUsername] = useState(() => presetCredentials?.username ?? '')
  const [password, setPassword] = useState(() => presetCredentials?.password ?? '')
  const [status, setStatus] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    const trimmedUser = username.trim()
    const trimmedPass = password.trim()
    if (!trimmedUser || !trimmedPass) {
      setStatus({ success: false, message: 'Username and password are required.' })
      return
    }

    setIsSubmitting(true)
    setStatus({ success: false, message: 'Verifying credentials…' })

    try {
      await verifyCredentials(trimmedUser, trimmedPass)
      const result = onSave?.(trimmedUser, trimmedPass)
      setStatus({ success: true, message: 'Credentials verified and saved locally.' })
      if (result?.success) {
        setUsername('')
        setPassword('')
      }
    } catch {
      setStatus({ success: false, message: 'Invalid username or password. Please try again.' })
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-50 to-white px-4">
      <section className="w-full max-w-md bg-white border border-blue-100 rounded-2xl shadow-xl p-8 space-y-4">
        <header className="space-y-2 text-center">
          <p className="text-xs uppercase tracking-[0.2em] text-blue-500 font-semibold">Secure Access</p>
          <h1 className="text-2xl font-bold text-gray-900">Sign in to continue</h1>
          <p className="text-sm text-gray-600">
            Use the Django Basic Auth credentials you share with reviewers. Once signed in you can
            upload CSVs, visualize the data, and download PDF summaries.
          </p>
        </header>

        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="text-sm font-medium text-gray-700 flex flex-col">
            Username
            <input
              type="text"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              className="mt-1 rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="admin"
            />
          </label>
          <label className="text-sm font-medium text-gray-700 flex flex-col">
            Password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="mt-1 rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="••••••••"
            />
          </label>
          <button
            type="submit"
            disabled={isSubmitting}
            className={`w-full bg-blue-600 text-white py-2.5 rounded-lg font-medium transition-colors ${
              isSubmitting ? 'opacity-70 cursor-not-allowed' : 'hover:bg-blue-700'
            }`}
          >
            {isSubmitting ? 'Verifying…' : 'Sign In'}
          </button>
          {status?.message && (
            <p className={`text-sm ${status.success ? 'text-green-600' : 'text-red-600'} text-center`}>
              {status.message}
            </p>
          )}
        </form>

        <div className="space-y-3">
          {presetCredentials ? (
            <div className="bg-blue-50 border border-blue-100 rounded-xl p-4 text-sm text-blue-900">
              <p className="text-xs uppercase tracking-wide text-blue-600 font-semibold mb-1">Hosted demo
                credentials
              </p>
              <p>
                Username: <code>{presetCredentials.username}</code>
              </p>
              <p>
                Password: <code>{presetCredentials.password}</code>
              </p>
              <p className="mt-2 text-[13px] text-blue-800">
                These values ship with the deployed build so reviewers can sign in immediately.
              </p>
            </div>
          ) : (
            <div className="bg-amber-50 border border-amber-100 rounded-xl p-4 text-sm text-amber-900">
              <p className="text-xs uppercase tracking-wide text-amber-600 font-semibold mb-1">Shareable tip</p>
              <p>
                Include reviewer credentials (or set <code>VITE_API_USERNAME</code> /{' '}
                <code>VITE_API_PASSWORD</code>) before deploying so evaluators can log in easily.
              </p>
            </div>
          )}

          <div className="bg-gray-50 border border-gray-100 rounded-xl p-4 text-sm text-gray-700">
            <p className="text-xs uppercase tracking-wide text-gray-500 font-semibold mb-1">Local testing</p>
            <p>
              When running locally, create your own user via <code>python manage.py createsuperuser</code>
              and sign in with that username/password.
            </p>
          </div>
        </div>
      </section>
    </main>
  )
}

export default LoginScreen
