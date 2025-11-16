import api from './api'

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
  full_name?: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export interface UserResponse {
  id: number
  email: string
  username: string
  full_name?: string
  role: string
  is_active: boolean
  created_at: string
}

export const authService = {
  login: async (credentials: LoginRequest): Promise<AuthResponse> => {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)
    
    const response = await api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  register: async (data: RegisterRequest): Promise<UserResponse> => {
    const response = await api.post('/api/auth/register', data)
    return response.data
  },

  getCurrentUser: async (): Promise<UserResponse> => {
    const response = await api.get('/api/auth/me')
    return response.data
  },

  logout: async (): Promise<void> => {
    await api.post('/api/auth/logout')
  },
}
