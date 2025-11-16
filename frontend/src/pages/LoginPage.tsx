import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { useAuthStore } from '../stores/authStore'
import { authService } from '../services/authService'
import { Sparkles } from 'lucide-react'
import { Link, useNavigate } from 'react-router-dom'

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const { setAuth } = useAuthStore()
  const navigate = useNavigate()

  const loginMutation = useMutation({
    mutationFn: authService.login,
    onSuccess: async (data) => {
      // Get user info
      const user = await authService.getCurrentUser()
      setAuth(user, data.access_token)
      navigate('/chat')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    loginMutation.mutate({ username, password })
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-purple-50">
      <div className="max-w-md w-full mx-4">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-600 rounded-2xl mb-4">
            <Sparkles className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">COGNIX AI</h1>
          <p className="text-gray-600 mt-2">Intelligent Multi-Domain Analytics</p>
        </div>

        <div className="card">
          <h2 className="text-2xl font-bold mb-6">Sign In</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input-field"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field"
                required
              />
            </div>

            {loginMutation.isError && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                Invalid username or password
              </div>
            )}

            <button
              type="submit"
              disabled={loginMutation.isPending}
              className="btn-primary w-full"
            >
              {loginMutation.isPending ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <p className="text-center text-sm text-gray-600 mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-primary-600 hover:underline font-medium">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
