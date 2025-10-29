import { useState, useRef, DragEvent, ChangeEvent } from 'react';
import { ragService } from '../services/ragService';

const ALLOWED_FILE_TYPES = {
  'application/pdf': '.pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
  'application/msword': '.doc',
  'text/plain': '.txt',
};

interface DocumentUploadProps {
  onUploadSuccess?: (result: { tenant: string; file_id: string; chunks: number }) => void;
  onUploadError?: (error: string) => void;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({
  onUploadSuccess,
  onUploadError,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [fileName, setFileName] = useState<string | null>(null);
  const [notification, setNotification] = useState<{
    type: 'success' | 'error';
    message: string;
  } | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): boolean => {
    // Check file type
    if (!Object.keys(ALLOWED_FILE_TYPES).includes(file.type)) {
      const allowedExtensions = Object.values(ALLOWED_FILE_TYPES).join(', ');
      showNotification('error', `Invalid file type. Allowed types: ${allowedExtensions}`);
      return false;
    }

    // Check file size (max 10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
      showNotification('error', 'File size exceeds 10MB limit');
      return false;
    }

    return true;
  };

  const showNotification = (type: 'success' | 'error', message: string) => {
    setNotification({ type, message });
    setTimeout(() => setNotification(null), 5000);
  };

  const handleUpload = async (file: File) => {
    if (!validateFile(file)) {
      return;
    }

    setIsUploading(true);
    setFileName(file.name);
    setUploadProgress(0);

    try {
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const result = await ragService.ingestDocument(file);

      clearInterval(progressInterval);
      setUploadProgress(100);

      showNotification(
        'success',
        `Successfully uploaded ${file.name}. Created ${result.chunks} chunks.`
      );

      if (onUploadSuccess) {
        onUploadSuccess(result);
      }

      // Reset after 2 seconds
      setTimeout(() => {
        setIsUploading(false);
        setUploadProgress(0);
        setFileName(null);
      }, 2000);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Upload failed';
      showNotification('error', errorMessage);

      if (onUploadError) {
        onUploadError(errorMessage);
      }

      setIsUploading(false);
      setUploadProgress(0);
      setFileName(null);
    }
  };

  const handleDragEnter = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    if (files.length > 0) {
      handleUpload(files[0]);
    }
  };

  const handleFileInput = (e: ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleUpload(files[0]);
    }
  };

  const handleClick = () => {
    if (!isUploading && fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Upload Area */}
      <div
        onClick={handleClick}
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-all duration-200 ease-in-out
          ${isDragging ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-300 dark:border-gray-600'}
          ${isUploading ? 'cursor-not-allowed opacity-60' : 'hover:border-blue-400 hover:bg-gray-50 dark:hover:bg-gray-800'}
        `}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept={Object.values(ALLOWED_FILE_TYPES).join(',')}
          onChange={handleFileInput}
          disabled={isUploading}
        />

        <div className="space-y-4">
          {/* Icon */}
          <div className="flex justify-center">
            <svg
              className="w-16 h-16 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
          </div>

          {/* Text */}
          <div>
            <p className="text-lg font-medium text-gray-700 dark:text-gray-300">
              {isUploading ? 'Uploading...' : isDragging ? 'Drop file here' : 'Drag & drop your document'}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              or click to browse
            </p>
            <p className="text-xs text-gray-400 dark:text-gray-500 mt-2">
              Supported formats: PDF, DOCX, TXT (max 10MB)
            </p>
          </div>

          {/* Progress Bar */}
          {isUploading && (
            <div className="space-y-2">
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                <div
                  className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {fileName} - {uploadProgress}%
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Notification Toast */}
      {notification && (
        <div
          className={`
            mt-4 p-4 rounded-lg shadow-lg animate-fade-in
            ${notification.type === 'success' ? 'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800' : 'bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800'}
          `}
        >
          <div className="flex items-start">
            <div className="flex-shrink-0">
              {notification.type === 'success' ? (
                <svg
                  className="w-5 h-5 text-green-600 dark:text-green-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
              ) : (
                <svg
                  className="w-5 h-5 text-red-600 dark:text-red-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              )}
            </div>
            <div className="ml-3">
              <p
                className={`text-sm font-medium ${notification.type === 'success' ? 'text-green-800 dark:text-green-200' : 'text-red-800 dark:text-red-200'}`}
              >
                {notification.message}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
