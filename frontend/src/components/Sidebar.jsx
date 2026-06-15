import { Link } from 'react-router-dom'

function Sidebar() {
  return (
    <aside className="w-64 bg-gray-900 text-white">
      <div className="p-6">
        <h1 className="text-2xl font-bold">NTAF</h1>
      </div>
      <nav className="mt-6">
        <Link to="/" className="block px-6 py-3 hover:bg-gray-800">
          Dashboard
        </Link>
        <Link to="/devices" className="block px-6 py-3 hover:bg-gray-800">
          Devices
        </Link>
        <Link to="/tests" className="block px-6 py-3 hover:bg-gray-800">
          Tests
        </Link>
        <Link to="/reports" className="block px-6 py-3 hover:bg-gray-800">
          Reports
        </Link>
        <Link to="/settings" className="block px-6 py-3 hover:bg-gray-800">
          Settings
        </Link>
      </nav>
    </aside>
  )
}

export default Sidebar
