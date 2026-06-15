import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Devices from './pages/Devices'
import TestCases from './pages/TestCases'
import Reports from './pages/Reports'
import Settings from './pages/Settings'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/devices" element={<Devices />} />
          <Route path="/tests" element={<TestCases />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
