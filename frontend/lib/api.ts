import { AuthService } from './auth'

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

// Track if a token refresh is in progress
let isRefreshing = false
let refreshPromise: Promise<string> | null = null

/**
 * Base API client with authentication handling
 */
export const ApiClient = {
  /**
   * Make a GET request to the API
   */
  get: async <T>(
    endpoint: string,
    params?: Record<string, string>
  ): Promise<T> => {
    const url = new URL(`${API_URL}${endpoint}`)

    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        url.searchParams.append(key, value)
      })
    }

    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: await getHeaders(),
      credentials: 'include', // Include cookies in the request
      mode: 'cors',
    })

    return handleResponse<T>(response)
  },

  /**
   * Make a POST request to the API
   */
  post: async <T>(endpoint: string, data: any): Promise<T> => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: await getHeaders(),
      body: JSON.stringify(data),
      credentials: 'include', // Include cookies in the request
      mode: 'cors',
    })

    return handleResponse<T>(response)
  },

  /**
   * Make a PUT request to the API
   */
  put: async <T>(endpoint: string, data: any): Promise<T> => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'PUT',
      headers: await getHeaders(),
      body: JSON.stringify(data),
      credentials: 'include', // Include cookies in the request
      mode: 'cors',
    })

    return handleResponse<T>(response)
  },

  /**
   * Make a PATCH request to the API
   */
  patch: async <T>(endpoint: string, data: any): Promise<T> => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'PATCH',
      headers: await getHeaders(),
      body: JSON.stringify(data),
      credentials: 'include', // Include cookies in the request
      mode: 'cors',
    })

    return handleResponse<T>(response)
  },

  /**
   * Make a DELETE request to the API
   */
  delete: async <T>(endpoint: string): Promise<T> => {
    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'DELETE',
      headers: await getHeaders(),
      credentials: 'include', // Include cookies in the request
      mode: 'cors',
    })

    return handleResponse<T>(response)
  },
}

/**
 * Get headers for API requests, including authentication token if available
 */
async function getHeaders(): Promise<HeadersInit> {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  }

  const token = AuthService.getAccessToken()
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  return headers
}

/**
 * Handle API response, including error handling and token refresh
 */
async function handleResponse<T>(response: Response): Promise<T> {
  // If response is 401 Unauthorized, try to refresh token
  if (response.status === 401) {
    try {
      // Only refresh once at a time to prevent multiple refresh requests
      if (!isRefreshing) {
        isRefreshing = true
        refreshPromise = AuthService.refreshToken()
      }

      // Wait for the refresh to complete
      if (refreshPromise) {
        await refreshPromise
        refreshPromise = null
        isRefreshing = false
      }

      // Retry the original request with the new token
      const newHeaders = await getHeaders()
      // Get the request method from the original response
      // Response doesn't have a method property, so we need to infer it
      const method =
        response.type === 'cors' || response.type === 'basic'
          ? 'GET'
          : 'POST'

      const retryResponse = await fetch(response.url, {
        method,
        headers: newHeaders,
        body: response.bodyUsed
          ? undefined
          : await response.clone().text(),
        credentials: 'include',
        mode: 'cors',
      })

      return handleResponse<T>(retryResponse)
    } catch (error) {
      // If refresh fails, clear refresh state and throw error
      isRefreshing = false
      refreshPromise = null

      // Redirect to login page will be handled by the component
      throw new Error('Session expired. Please login again.')
    }
  }

  // Handle other error responses
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    const errorMessage = errorData.detail || 'An error occurred'
    throw new Error(errorMessage)
  }

  // Parse and return successful response
  return response.json() as Promise<T>
}
