import { useState } from 'react';
import ReactMarkdown from 'react-markdown';

interface AnswerDisplayProps {
  answer: string;
  timestamp?: string;
  confidence?: number;
}

function AnswerDisplay({ answer, timestamp, confidence }: AnswerDisplayProps) {
  const [copied, setCopied] = useState(false);

  const handleCopyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(answer);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  const getConfidenceBadge = (score: number) => {
    if (score >= 0.8) {
      return { label: 'High', color: 'bg-green-100 text-green-800' };
    } else if (score >= 0.5) {
      return { label: 'Medium', color: 'bg-yellow-100 text-yellow-800' };
    } else {
      return { label: 'Low', color: 'bg-red-100 text-red-800' };
    }
  };

  const formatTimestamp = (ts: string) => {
    const date = new Date(ts);
    return date.toLocaleString();
  };

  if (!answer) {
    return null;
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      {/* Header with metadata */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-white">
            Answer
          </h3>
          {confidence !== undefined && (
            <span
              className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${getConfidenceBadge(confidence).color}`}
            >
              {getConfidenceBadge(confidence).label} Confidence ({Math.round(confidence * 100)}%)
            </span>
          )}
        </div>
        <button
          onClick={handleCopyToClipboard}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
          title="Copy to clipboard"
        >
          {copied ? (
            <>
              <CheckIcon />
              <span>Copied!</span>
            </>
          ) : (
            <>
              <CopyIcon />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>

      {/* Answer content with markdown */}
      <div className="prose prose-sm dark:prose-invert max-w-none text-gray-700 dark:text-gray-300">
        <ReactMarkdown>{answer}</ReactMarkdown>
      </div>

      {/* Timestamp */}
      {timestamp && (
        <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Generated at: {formatTimestamp(timestamp)}
          </p>
        </div>
      )}
    </div>
  );
}

// Copy Icon Component
function CopyIcon() {
  return (
    <svg
      className="w-4 h-4"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
      />
    </svg>
  );
}

// Check Icon Component
function CheckIcon() {
  return (
    <svg
      className="w-4 h-4 text-green-600"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeWidth={2}
        d="M5 13l4 4L19 7"
      />
    </svg>
  );
}

export default AnswerDisplay;
