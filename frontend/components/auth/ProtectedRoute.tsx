'use client'

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { AuthService } from '@/lib/auth'

interface ProtectedRouteProps {
  children: React.ReactNode
  allowedUserTypes?: ('STAFF' | 'PATIENT')[]
}

/**
 * A wrapper component that protects routes based on authentication status and user type
 *
 * @param children The content to render if the user is authenticated and authorized
 * @param allowedUserTypes Optional array of user types that are allowed to access this route
 */
export function ProtectedRoute({
  children,
  allowedUserTypes,
}: ProtectedRouteProps) {
  const router = useRouter()
  const pathname = usePathname()
  const [isAuthorized, setIsAuthorized] = useState<boolean | null>(
    null
  )

  useEffect(() => {
    // Skip auth check during SSR
    if (typeof window === 'undefined') return

    // Function to handle authorization check
    const checkAuthorization = async () => {
      try {
        // Avoid redirect loops by checking the current path
        const isAuthPage =
          pathname === '/login' ||
          pathname === '/register' ||
          pathname === '/'

        // Check if user is authenticated
        const isAuthenticated = AuthService.isAuthenticated()
        const currentUser = AuthService.getCurrentUser()

        console.log('Auth check:', {
          isAuthenticated,
          currentUser,
          pathname,
          isAuthPage,
        })

        // Handle authentication logic
        if (!isAuthenticated) {
          // If not authenticated and not already on an auth page, redirect to login
          if (!isAuthPage) {
            console.log('Not authenticated, redirecting to login')
            // Store the intended destination for post-login redirect
            sessionStorage.setItem('redirectAfterLogin', pathname)
            router.push('/login')
            return
          } else {
            // Already on auth page, no need to redirect
            console.log('On auth page, allowing access')
            setIsAuthorized(true)
            return
          }
        }

        // If authenticated but on an auth page, redirect to appropriate dashboard
        if (isAuthPage) {
          console.log(
            'Authenticated but on auth page, redirecting to dashboard'
          )
          if (currentUser?.user_type === 'STAFF') {
            router.push('/admin/dashboard')
          } else {
            router.push('/dashboard')
          }
          return
        }

        // If allowedUserTypes is specified, check if user type is allowed
        if (allowedUserTypes && currentUser) {
          if (!allowedUserTypes.includes(currentUser.user_type)) {
            console.log(
              'User type not allowed, redirecting to appropriate dashboard'
            )
            // Redirect to appropriate dashboard based on user type
            if (currentUser.user_type === 'STAFF') {
              router.push('/admin/dashboard')
            } else {
              router.push('/dashboard')
            }
            return
          }
        }

        // User is authenticated and authorized
        console.log('User is authenticated and authorized')
        setIsAuthorized(true)
      } catch (error) {
        console.error('Error in authorization check:', error)
        // In case of error, allow access to avoid locking users out
        setIsAuthorized(true)
      }
    }

    checkAuthorization()
  }, [pathname, router, allowedUserTypes])

  // Show nothing while checking authorization to avoid flash of content
  if (isAuthorized === null) {
    return null
  }

  // Render children if authorized
  return <>{children}</>
}
