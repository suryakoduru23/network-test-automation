import { useAuthStore } from '../stores/store'

function Navbar() {
  const { user, logout } = useAuthStore()

  return (
    <nav className="bg-white shadow-sm">
      <div className="px-6 py-4 flex justify-between items-center">
        <h2 className="text-xl font-semibold">Network Test Automation</h2>
        <div className="flex items-center gap-4">
          {user && <span className="text-gray-600">{user.username}</span>}
          <button
            onClick={logout}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
