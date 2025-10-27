import apiClient from './api';
import { AskResponse, IngestResponse, HealthResponse } from '../types';

/**
 * RAG Platform API Service
 */
export class RagService {
  /**
   * Check API health status
   */
  static async checkHealth(): Promise<HealthResponse> {
    const response = await apiClient.get<HealthResponse>('/healthz');
    return response.data;
  }

  /**
   * Upload and ingest a document
   */
  static async ingestDocument(file: File): Promise<IngestResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post<IngestResponse>('/ingest', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  /**
   * Ask a question
   */
  static async askQuestion(question: string): Promise<AskResponse> {
    const response = await apiClient.post<AskResponse>('/ask', {
      question,
    });

    return response.data;
  }
}

export default RagService;
