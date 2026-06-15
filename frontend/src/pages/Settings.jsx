function Settings() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Settings</h1>
      <div className="bg-white rounded-lg shadow p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Email Notifications</label>
          <input type="checkbox" className="w-4 h-4" />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2">Alert Severity</label>
          <select className="border rounded px-3 py-2">
            <option>Critical</option>
            <option>Warning</option>
            <option>Info</option>
          </select>
        </div>
        <button className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
          Save Settings
        </button>
      </div>
    </div>
  )
}

export default Settings
