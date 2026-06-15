import { useEffect, useState } from 'react'
import { healthService } from '../services/api'

function Dashboard() {
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await healthService.dashboard()
        setMetrics(response.data.metrics)
      } catch (error) {
        console.error('Failed to fetch metrics:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchMetrics()
  }, [])

  if (loading) return <div>Loading...</div>

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm font-medium">Total Devices</h3>
          <p className="text-3xl font-bold mt-2">{metrics?.total_devices || 0}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm font-medium">Total Tests</h3>
          <p className="text-3xl font-bold mt-2">{metrics?.total_tests || 0}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-gray-500 text-sm font-medium">Success Rate</h3>
          <p className="text-3xl font-bold mt-2">{metrics?.success_rate || '0%'}</p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
