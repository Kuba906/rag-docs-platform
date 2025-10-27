// API Response Types

export interface Source {
  text: string;
  score: number;
  metadata?: Record<string, any>;
}

export interface AskResponse {
  answer: string;
  sources: Source[];
  query: string;
  timestamp?: string;
  confidence?: number;
}

export interface IngestResponse {
  message: string;
  file_id: string;
  chunks_count: number;
  filename: string;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
}

export interface Document {
  id: string;
  filename: string;
  size_bytes: number;
  chunk_count: number;
  uploaded_at: string;
  metadata?: Record<string, any>;
}

export interface ApiError {
  detail: string;
  status?: number;
}

// Component Props Types
export interface SearchInputProps {
  onSearch: (query: string) => void;
  isLoading: boolean;
}

export interface AnswerDisplayProps {
  answer: string;
  timestamp?: string;
  confidence?: number;
}

export interface SourcesListProps {
  sources: Source[];
}

export interface DocumentUploadProps {
  onUploadSuccess: (response: IngestResponse) => void;
  onUploadError: (error: string) => void;
}
