import { useNavigate } from 'react-router-dom'
import { LogOut } from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuth } from '../hooks/useAuth'

export default function ProfilePage() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    toast.success('Logged out successfully')
    navigate('/login')
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-md p-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Profile</h1>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-600">Full Name</label>
            <p className="mt-1 text-lg text-gray-800">{user?.full_name}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600">Email</label>
            <p className="mt-1 text-lg text-gray-800">{user?.email}</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600">Member Since</label>
            <p className="mt-1 text-lg text-gray-800">
              {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
            </p>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-200">
          <button
            onClick={handleLogout}
            className="flex items-center space-x-2 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </div>
  )
}
