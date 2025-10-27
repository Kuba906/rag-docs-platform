import { useState, useEffect } from 'react';
import RagService from './services/ragService';

function App() {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const health = await RagService.checkHealth();
      setIsHealthy(health.status === 'healthy');
    } catch (error) {
      setIsHealthy(false);
      console.error('Health check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <header className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4">
              RAG Docs Platform
            </h1>
            <p className="text-xl text-gray-300">
              Enterprise Document Search with AI
            </p>
          </header>

          {/* Health Status Card */}
          <div className="card mb-8">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-semibold text-gray-800 dark:text-white">
                API Status
              </h2>
              <div className="flex items-center gap-2">
                {loading ? (
                  <span className="text-gray-500">Checking...</span>
                ) : (
                  <>
                    <div
                      className={`w-3 h-3 rounded-full ${
                        isHealthy ? 'bg-green-500' : 'bg-red-500'
                      }`}
                    />
                    <span
                      className={`font-medium ${
                        isHealthy ? 'text-green-600' : 'text-red-600'
                      }`}
                    >
                      {isHealthy ? 'Connected' : 'Disconnected'}
                    </span>
                  </>
                )}
              </div>
            </div>
          </div>

          {/* Welcome Message */}
          <div className="card text-center">
            <h3 className="text-xl font-semibold text-gray-800 dark:text-white mb-4">
              Welcome to RAG Docs Platform
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              The frontend is successfully configured with:
            </p>
            <ul className="text-left max-w-md mx-auto space-y-2 text-gray-700 dark:text-gray-300">
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span> React 18 + TypeScript
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span> Vite Build Tool
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span> Tailwind CSS
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span> Axios API Client
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span> ESLint + Prettier
              </li>
            </ul>
            <div className="mt-8">
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Ready to build advanced features like document upload, search, and more!
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
