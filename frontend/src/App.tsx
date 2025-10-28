import { useState, useEffect } from 'react';
import RagService from './services/ragService';
import { DocumentUpload } from './components/DocumentUpload';
import { IngestResponse } from './types';

function App() {
  const [isHealthy, setIsHealthy] = useState<boolean | null>(null);
  const [loading, setLoading] = useState(true);
  const [uploadedDocuments, setUploadedDocuments] = useState<IngestResponse[]>([]);

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

  const handleUploadSuccess = (result: IngestResponse) => {
    setUploadedDocuments((prev) => [...prev, result]);
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

          {/* Document Upload Section */}
          <div className="card mb-8">
            <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-6">
              Upload Documents
            </h2>
            <DocumentUpload
              onUploadSuccess={handleUploadSuccess}
            />
          </div>

          {/* Uploaded Documents List */}
          {uploadedDocuments.length > 0 && (
            <div className="card">
              <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-4">
                Uploaded Documents
              </h2>
              <div className="space-y-3">
                {uploadedDocuments.map((doc, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg"
                  >
                    <div>
                      <p className="font-medium text-gray-800 dark:text-white">
                        {doc.file_id}
                      </p>
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        Tenant: {doc.tenant}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-blue-600 dark:text-blue-400">
                        {doc.chunks} chunks
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
