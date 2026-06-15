function TestCases() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Test Cases</h1>
        <button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
          Create Test
        </button>
      </div>
      <div className="bg-white rounded-lg shadow p-6">
        <p className="text-gray-600">No test cases yet</p>
      </div>
    </div>
  )
}

export default TestCases
