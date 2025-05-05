'use client'

import React, { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { AppLayout } from '@/components/layout/AppLayout'
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from '@/components/ui/Card'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import { AuthService } from '@/lib/auth'
import { LogIn } from 'lucide-react'

export default function LoginPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  })
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  // Check if user is already authenticated
  useEffect(() => {
    if (AuthService.isAuthenticated()) {
      const user = AuthService.getCurrentUser()
      if (user?.user_type === 'STAFF') {
        router.push('/admin/dashboard')
      } else {
        router.push('/dashboard')
      }
    }
  }, [router])

  // Get the callback URL from the query parameters
  useEffect(() => {
    const callbackUrl = searchParams.get('callbackUrl')
    if (callbackUrl) {
      sessionStorage.setItem(
        'redirectAfterLogin',
        decodeURI(callbackUrl)
      )
    }
  }, [searchParams])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)

    try {
      console.log('Attempting login with:', formData.username)

      const user = await AuthService.login(
        formData.username,
        formData.password
      )

      console.log('Login successful:', user)

      // Get the redirect URL from session storage
      let redirectUrl: string | null = null

      try {
        redirectUrl = sessionStorage.getItem('redirectAfterLogin')
        console.log('Redirect URL from session storage:', redirectUrl)
      } catch (sessionError) {
        console.error(
          'Error accessing session storage:',
          sessionError
        )
      }

      // Redirect based on stored URL or user type
      if (redirectUrl) {
        console.log('Redirecting to:', redirectUrl)
        router.push(redirectUrl)
      } else if (user.user_type === 'STAFF') {
        console.log('Redirecting to admin dashboard')
        router.push('/admin/dashboard')
      } else {
        console.log('Redirecting to patient dashboard')
        router.push('/dashboard')
      }
    } catch (err) {
      console.error('Login error:', err)
      setError(
        err instanceof Error
          ? err.message
          : 'Login failed. Please try again.'
      )
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <AppLayout>
      <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-surface-50 to-white dark:from-gray-950 dark:to-gray-900">
        <div className="w-full max-w-md px-4 sm:px-0">
          <Card className="shadow-2xl border border-gray-100 rounded-2xl p-0 overflow-hidden">
            <CardHeader className="flex flex-col items-center gap-2 pb-0 bg-primary-50 dark:bg-primary-950/30 py-8">
              <div className="bg-white dark:bg-gray-900 rounded-full p-3 mb-2 shadow">
                <LogIn className="h-7 w-7 text-primary-700" />
              </div>
              <CardTitle className="text-2xl font-extrabold text-gray-900">
                Login to Telepro-AI
              </CardTitle>
              <CardDescription className="text-lg text-gray-600 font-medium">
                Enter your credentials to access your account
              </CardDescription>
            </CardHeader>
            <form
              onSubmit={handleSubmit}
              className="px-6 py-8 space-y-6"
            >
              {error && (
                <div className="bg-red-50 text-red-500 p-3 rounded-md text-sm font-semibold text-center">
                  {error}
                </div>
              )}
              <Input
                label="Username"
                id="username"
                name="username"
                type="text"
                value={formData.username}
                onChange={handleChange}
                required
                autoComplete="username"
              />
              <Input
                label="Password"
                id="password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                required
                autoComplete="current-password"
              />
              <Button
                type="submit"
                disabled={isLoading}
                size="lg"
                className="w-full font-semibold text-lg shadow-md mt-2"
              >
                {isLoading ? 'Logging in...' : 'Login'}
              </Button>
            </form>
            <CardFooter className="bg-surface-50 dark:bg-gray-900/60 py-5 px-6 flex flex-col items-center">
              <div className="text-center text-base text-gray-700">
                Don&apos;t have an account?{' '}
                <Link
                  href="/register"
                  className="text-primary-700 hover:text-primary-900 font-semibold underline underline-offset-2"
                >
                  Register here
                </Link>
              </div>
            </CardFooter>
          </Card>
        </div>
      </div>
    </AppLayout>
  )
}
