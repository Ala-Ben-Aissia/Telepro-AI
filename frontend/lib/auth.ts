import { jwtDecode } from 'jwt-decode'
import Cookies from 'js-cookie'
import { User, TokenResponse, DecodedToken } from '@/types'

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

// Helper function to safely access localStorage (only in browser)
const safeLocalStorage = {
  getItem: (key: string): string | null => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(key)
    }
    return null
  },
  setItem: (key: string, value: string): void => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(key, value)
    }
  },
  removeItem: (key: string): void => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(key)
    }
  },
}

// Helper function to safely access cookies (only in browser)
const safeCookies = {
  set: (
    key: string,
    value: string,
    options?: Cookies.CookieAttributes
  ): void => {
    if (typeof window !== 'undefined') {
      try {
        Cookies.set(key, value, {
          secure: process.env.NODE_ENV === 'production',
          sameSite: 'strict',
          expires: 7, // 7 days
          path: '/',
          ...options,
        })
      } catch (error) {
        console.error('Error setting cookie:', error)
      }
    }
  },
  get: (key: string): string | undefined => {
    if (typeof window !== 'undefined') {
      try {
        return Cookies.get(key)
      } catch (error) {
        console.error('Error getting cookie:', error)
        return undefined
      }
    }
    return undefined
  },
  remove: (key: string, options?: Cookies.CookieAttributes): void => {
    if (typeof window !== 'undefined') {
      try {
        Cookies.remove(key, {
          path: '/',
          ...options,
        })
      } catch (error) {
        console.error('Error removing cookie:', error)
      }
    }
  },
}

export const AuthService = {
  /**
   * Login user and store tokens in cookies and localStorage
   */
  login: async (
    username: string,
    password: string
  ): Promise<User> => {
    try {
      // API call to authenticate user
      const response = await fetch(`${API_URL}/accounts/token/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
        credentials: 'include',
        mode: 'cors',
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(
          errorData.detail ||
            'Login failed. Please check your credentials.'
        )
      }

      const data: TokenResponse = await response.json()

      // Store tokens in cookies for better security
      safeCookies.set('accessToken', data.access, { expires: 1 }) // 1 day
      safeCookies.set('refreshToken', data.refresh, { expires: 7 }) // 7 days
      // Store user info in localStorage for easy access
      const user: User = {
        user_id: data.user_id,
        username: data.username,
        email: data.email,
        user_type: data.user_type,
        patient_uuid: data.patient_uuid,
      }
      safeLocalStorage.setItem('user', JSON.stringify(user))

      // Check for redirect after login
      if (typeof window !== 'undefined') {
        const redirectPath = sessionStorage.getItem(
          'redirectAfterLogin'
        )
        if (redirectPath) {
          sessionStorage.removeItem('redirectAfterLogin')
          // The redirect will be handled by the component that called login
        }
      }

      return user
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  },

  /**
   * Register a new patient user
   */
  register: async (userData: {
    username: string
    email: string
    password: string
    password_confirm: string
    phone_number?: string
  }): Promise<User> => {
    const response = await fetch(`${API_URL}/accounts/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
      credentials: 'include',
      mode: 'cors',
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(
        Object.values(error).flat().join(', ') ||
          'Registration failed'
      )
    }

    const data = await response.json()

    // Store tokens in cookies
    safeCookies.set('accessToken', data.access, { expires: 1 }) // 1 day
    safeCookies.set('refreshToken', data.refresh, { expires: 7 }) // 7 days

    // Store user info
    const user: User = {
      user_id: data.user_id,
      username: userData.username,
      email: userData.email,
      user_type: 'PATIENT',
      patient_uuid: data.patient_uuid,
    }
    safeLocalStorage.setItem('user', JSON.stringify(user))

    return user
  },

  /**
   * Logout user and remove tokens
   */
  logout: (): void => {
    safeCookies.remove('accessToken')
    safeCookies.remove('refreshToken')
    safeLocalStorage.removeItem('user')

    // Clear any redirect paths
    if (typeof window !== 'undefined') {
      sessionStorage.removeItem('redirectAfterLogin')
    }

    // Redirect to home page will be handled by the component that calls logout
  },

  /**
   * Get current user from localStorage
   */
  getCurrentUser: (): User | null => {
    const userStr = safeLocalStorage.getItem('user')
    if (!userStr) return null

    try {
      return JSON.parse(userStr) as User
    } catch {
      // Ignore parsing errors
      return null
    }
  },

  /**
   * Check if user is authenticated by verifying the token
   */
  isAuthenticated: (): boolean => {
    // First check if we're in a browser environment
    if (typeof window === 'undefined') return false

    try {
      // Check for token in cookies
      const token = safeCookies.get('accessToken')
      if (!token) {
        console.log('No access token found')
        return false
      }

      // No mock token check needed

      // Validate token
      try {
        const decoded = jwtDecode(token) as DecodedToken
        const currentTime = Date.now() / 1000

        // If token is expired but we have a refresh token, consider still authenticated
        // The actual refresh will happen in the API client
        if (decoded.exp <= currentTime) {
          console.log('Token expired, checking for refresh token')
          const hasRefreshToken = !!safeCookies.get('refreshToken')
          if (hasRefreshToken) {
            return true
          }
          console.log('No refresh token found')
          return false
        }

        // Token is valid
        return true
      } catch (decodeError) {
        console.error('Error decoding token:', decodeError)

        // If we can't decode the token, authentication fails
        return false
      }
    } catch (error) {
      console.error('Error in isAuthenticated:', error)
      return false
    }
  },

  /**
   * Get access token from cookies
   */
  getAccessToken: (): string | null => {
    const token = safeCookies.get('accessToken')
    return token || null
  },

  /**
   * Refresh access token using refresh token
   */
  refreshToken: async (): Promise<string> => {
    const refreshToken = safeCookies.get('refreshToken')
    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    const response = await fetch(
      `${API_URL}/accounts/token/refresh/`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh: refreshToken }),
        credentials: 'include',
        mode: 'cors',
      }
    )

    if (!response.ok) {
      // If refresh fails, logout user
      AuthService.logout()
      throw new Error('Session expired. Please login again.')
    }

    const data = await response.json()
    safeCookies.set('accessToken', data.access, { expires: 1 }) // 1 day

    return data.access
  },
}
