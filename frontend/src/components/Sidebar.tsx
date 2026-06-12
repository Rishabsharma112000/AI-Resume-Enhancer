import { Link, useLocation } from 'react-router-dom'
import { Home, Settings } from 'lucide-react'

export default function Sidebar() {
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <aside className="w-64 bg-gray-900 text-white p-6">
      <div className="mb-8">
        <h2 className="text-xl font-bold">Navigation</h2>
      </div>

      <nav className="space-y-4">
        <Link
          to="/"
          className={`flex items-center space-x-3 px-4 py-2 rounded-lg transition ${
            isActive('/') ? 'bg-blue-600' : 'hover:bg-gray-800'
          }`}
        >
          <Home className="w-5 h-5" />
          <span>Dashboard</span>
        </Link>

        <Link
          to="/profile"
          className={`flex items-center space-x-3 px-4 py-2 rounded-lg transition ${
            isActive('/profile') ? 'bg-blue-600' : 'hover:bg-gray-800'
          }`}
        >
          <Settings className="w-5 h-5" />
          <span>Profile</span>
        </Link>
      </nav>
    </aside>
  )
}
