import './App.css'
import WorkflowList from "./components/WorkflowList";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">
            Workflow Dashboard
          </h1>
          <span className="text-sm text-gray-500">
            State Management Service
          </span>
        </div>
      </header>

      {/* Main Content Container */}
      <main className="flex-1">
        <div className="max-w-6xl mx-auto p-4">
          
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-2">
              Welcome 👋
            </h2>
            {/* <p className="text-gray-600">
              Your workflow items will appear here.
            </p> */}
            <WorkflowList />
          </div>

        </div>
      </main>

      {/* Footer (Optional but nice touch) */}
      <footer className="bg-white border-t text-center py-3 text-sm text-gray-500">
        © {new Date().getFullYear()} Workflow Service
      </footer>

    </div>
  );
}