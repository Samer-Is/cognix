import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './stores/authStore'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import ChatPage from './pages/ChatPage'
import DomainsPage from './pages/DomainsPage'

function App() {
  const { isAuthenticated } = useAuthStore()

  return (
    <BrowserRouter>
      <Routes>
        <Route 
          path="/login" 
          element={isAuthenticated ? <Navigate to="/chat" /> : <LoginPage />} 
        />
        <Route 
          path="/register" 
          element={isAuthenticated ? <Navigate to="/chat" /> : <RegisterPage />} 
        />
        <Route 
          path="/dashboard" 
          element={isAuthenticated ? <DashboardPage /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/chat" 
          element={isAuthenticated ? <ChatPage /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/domains" 
          element={isAuthenticated ? <DomainsPage /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/" 
          element={<Navigate to={isAuthenticated ? "/chat" : "/login"} />} 
        />
      </Routes>
    </BrowserRouter>
  )
}

export default App
