import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

/**
 * Middleware to handle authentication and route protection
 * This runs on the edge before the page is rendered
 */
export function middleware(request: NextRequest) {
  // Get the pathname from the request
  const { pathname } = request.nextUrl

  // Get the token from cookies (if it exists)
  const token = request.cookies.get('accessToken')?.value

  // Public paths that don't require authentication
  const publicPaths = ['/', '/login', '/register']
  const staticPaths = ['/_next', '/favicon.ico', '/public']

  // Check if the path is public or static
  const isPublicPath = publicPaths.some(
    (path) => pathname === path || pathname.startsWith('/api/')
  )
  const isStaticPath = staticPaths.some((path) =>
    pathname.startsWith(path)
  )

  // Skip middleware for static paths
  if (isStaticPath) {
    return NextResponse.next()
  }

  // If the path is public, allow access
  if (isPublicPath) {
    return NextResponse.next()
  }

  // Let client-side handle more complex auth checks

  // If no token and trying to access protected route, redirect to login
  if (!token) {
    const url = new URL('/login', request.url)
    // Store the original URL to redirect back after login
    url.searchParams.set('callbackUrl', encodeURI(pathname))
    return NextResponse.redirect(url)
  }

  // Allow access to protected routes if token exists
  return NextResponse.next()
}

// Configure which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    '/((?!_next/static|_next/image|favicon.ico|public).*)',
  ],
}
