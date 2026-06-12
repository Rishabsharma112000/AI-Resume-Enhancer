import { useAuthStore } from '../store/authStore'
import { useNavigate } from 'react-router-dom'

export const useAuth = () => {
  const { user, token, setAuth, logout } = useAuthStore()
  const navigate = useNavigate()

  const logoutUser = () => {
    logout()
    navigate('/login')
  }

  return {
    user,
    token,
    setAuth,
    logout: logoutUser,
    isAuthenticated: !!token,
  }
}
