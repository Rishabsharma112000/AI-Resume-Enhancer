import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useAuthStore } from './store/authStore'
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import AnalysisPage from './pages/AnalysisPage'
import ProfilePage from './pages/ProfilePage'

function App() {
  const { user } = useAuthStore()

  return (
    <Router>
      <Toaster position="top-right" />
      <Routes>
        {!user ? (
          <>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="*" element={<Navigate to="/login" />} />
          </>
        ) : (
          <Route element={<Layout />}>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/analysis/:resumeId" element={<AnalysisPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Route>
        )}
      </Routes>
    </Router>
  )
}

export default App
