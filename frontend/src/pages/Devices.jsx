import { useEffect, useState } from 'react'
import { deviceService } from '../services/api'
import { useDeviceStore } from '../stores/store'

function Devices() {
  const { devices, loading, setDevices, setLoading } = useDeviceStore()
  const [newDevice, setNewDevice] = useState(null)

  useEffect(() => {
    const fetchDevices = async () => {
      setLoading(true)
      try {
        const response = await deviceService.getAll()
        setDevices(response.data)
      } catch (error) {
        console.error('Failed to fetch devices:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchDevices()
  }, [])

  const handleTestConnectivity = async (deviceId) => {
    try {
      await deviceService.testConnectivity(deviceId)
      alert('Connectivity test completed')
    } catch (error) {
      alert('Connectivity test failed')
    }
  }

  if (loading) return <div>Loading devices...</div>

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Devices</h1>
        <button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
          Add Device
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-medium">Hostname</th>
              <th className="px-6 py-3 text-left text-sm font-medium">IP Address</th>
              <th className="px-6 py-3 text-left text-sm font-medium">Type</th>
              <th className="px-6 py-3 text-left text-sm font-medium">Status</th>
              <th className="px-6 py-3 text-left text-sm font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            {devices.map((device) => (
              <tr key={device.id} className="border-b hover:bg-gray-50">
                <td className="px-6 py-3">{device.hostname}</td>
                <td className="px-6 py-3">{device.ip_address}</td>
                <td className="px-6 py-3">{device.device_type}</td>
                <td className="px-6 py-3">
                  <span className={`px-2 py-1 rounded text-sm ${
                    device.is_reachable ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {device.is_reachable ? 'Reachable' : 'Unreachable'}
                  </span>
                </td>
                <td className="px-6 py-3 text-sm space-x-2">
                  <button
                    onClick={() => handleTestConnectivity(device.id)}
                    className="text-blue-600 hover:text-blue-900"
                  >
                    Test
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Devices
