import { useState } from 'react'

const LoginScreen = ({ apiBaseUrl, onSave }) => {
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
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-50 to-white px-4">
      <section className="w-full max-w-md bg-white border border-blue-100 rounded-2xl shadow-xl p-8 space-y-4">
        <header className="space-y-2 text-center">
          <p className="text-xs uppercase tracking-[0.2em] text-blue-500 font-semibold">Secure Access</p>
          <h1 className="text-2xl font-bold text-gray-900">Sign in to continue</h1>
          <p className="text-sm text-gray-600">
            Provide the Django Basic Auth username/password. Requests will target{' '}
            <span className="font-semibold">{apiBaseUrl}</span>.
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
            className="w-full bg-blue-600 text-white py-2.5 rounded-lg font-medium hover:bg-blue-700 transition-colors"
          >
            Sign In
          </button>
          {status?.message && (
            <p className={`text-sm ${status.success ? 'text-green-600' : 'text-red-600'} text-center`}>
              {status.message}
            </p>
          )}
          <p className="text-xs text-gray-500 text-center">
            Tip: On deployments, preset credentials via <code>VITE_API_USERNAME</code> and{' '}
            <code>VITE_API_PASSWORD</code> so reviewers can sign in instantly.
          </p>
        </form>
      </section>
    </main>
  )
}

export default LoginScreen
