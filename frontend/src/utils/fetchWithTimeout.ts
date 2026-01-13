/**
 * Fetch with timeout to prevent hanging requests
 * @param url - The URL to fetch
 * @param options - Fetch options
 * @param timeout - Timeout in milliseconds (default: 30000ms = 30s)
 * @returns Promise<Response>
 */
export async function fetchWithTimeout(
  url: string,
  options: RequestInit = {},
  timeout: number = 30000
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    return response;
  } catch (error: any) {
    clearTimeout(timeoutId);

    if (error.name === 'AbortError') {
      throw new Error(
        `Request timeout after ${timeout / 1000}s. The server might be slow or down. Please try again.`
      );
    }

    // Network error or other fetch errors
    if (error.message.includes('Failed to fetch')) {
      throw new Error(
        'Network error: Unable to connect to the server. Please check your internet connection and try again.'
      );
    }

    throw error;
  }
}

/**
 * Helper to handle API responses with proper error messages
 */
export async function handleApiResponse<T>(response: Response): Promise<T> {
  const contentType = response.headers.get('content-type');

  // Handle non-JSON responses
  if (!contentType || !contentType.includes('application/json')) {
    if (!response.ok) {
      throw new Error(
        `Server error (${response.status}): Expected JSON but received ${contentType}. This might indicate the backend is down or misconfigured.`
      );
    }

    throw new Error('Invalid response format from server');
  }

  const data = await response.json();

  if (!response.ok) {
    // Handle specific error formats from backend
    const errorMsg = data.suggestion
      ? `${data.error}\n\n💡 Suggestion: ${data.suggestion}`
      : data.error || data.message || `Request failed with status ${response.status}`;

    throw new Error(errorMsg);
  }

  return data;
}
