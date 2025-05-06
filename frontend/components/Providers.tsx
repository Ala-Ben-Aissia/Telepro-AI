'use client'

import {
  ReactNode,
  createContext,
  useContext,
  useState,
  useEffect,
} from 'react'
import { usePathname, useRouter } from 'next/navigation'
import { getCurrentUser } from '@/app/api/actions'

// Define AuthContext types
type User = {
  id: string
  email: string
  is_staff: boolean
  is_superuser: boolean
} | null

type AuthContextType = {
  user: User
  loading: boolean
}

// Create context with default values
const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
})

// Custom hook to use the auth context
export const useAuth = () => useContext(AuthContext)

export function Providers({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()
  const pathname = usePathname()

  useEffect(() => {
    async function loadUserFromServer() {
      try {
        const userData = await getCurrentUser()
        setUser(userData)
      } catch (error) {
        console.error('Failed to load user data:', error)
        setUser(null)

        // Redirect to login if not on auth page and no user
        if (!pathname.startsWith('/auth/') && !userData) {
          router.push('/auth/login')
        }
      } finally {
        setLoading(false)
      }
    }

    loadUserFromServer()
  }, [pathname, router])

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  )
}
