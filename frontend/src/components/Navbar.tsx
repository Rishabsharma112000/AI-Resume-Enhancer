import { Link } from 'react-router-dom'
import { LogOut, User } from 'lucide-react'
import { useState } from 'react'
import { useAuth } from '../hooks/useAuth'

export default function Navbar() {
  const { user, logout } = useAuth()
  const [dropdownOpen, setDropdownOpen] = useState(false)

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-8">
          <h1 className="text-2xl font-bold text-blue-600">ResumeBoost AI</h1>
        </div>
        
        <div className="flex items-center space-x-4">
          {user && (
            <div className="relative">
              <button
                onClick={() => setDropdownOpen(!dropdownOpen)}
                className="flex items-center space-x-2 px-3 py-2 rounded-lg hover:bg-gray-100"
              >
                <User className="w-5 h-5" />
                <span className="text-sm font-medium">{user.full_name}</span>
              </button>

              {dropdownOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg z-50">
                  <Link
                    to="/profile"
                    onClick={() => setDropdownOpen(false)}
                    className="flex items-center space-x-2 px-4 py-2 hover:bg-gray-100 rounded-t-lg"
                  >
                    <User className="w-4 h-4" />
                    <span>Profile</span>
                  </Link>
                  <button
                    onClick={() => {
                      logout()
                      setDropdownOpen(false)
                    }}
                    className="w-full flex items-center space-x-2 px-4 py-2 hover:bg-gray-100 rounded-b-lg text-red-600"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Logout</span>
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}
