'use client'

import React, { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { AppLayout } from '@/components/layout/AppLayout'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
  CardFooter,
} from '@/components/ui/Card'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import { AuthService } from '@/lib/auth'

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
      <div className="max-w-md mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>Login to Telepro-AI</CardTitle>
            <CardDescription>
              Enter your credentials to access your account
            </CardDescription>
          </CardHeader>
          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4">
              {error && (
                <div className="bg-red-50 text-red-500 p-3 rounded-md text-sm">
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
            </CardContent>
            <CardFooter className="flex flex-col space-y-4">
              <Button type="submit" fullWidth disabled={isLoading}>
                {isLoading ? 'Logging in...' : 'Login'}
              </Button>
              <div className="text-center text-sm">
                Don&apos;t have an account?{' '}
                <Link
                  href="/register"
                  className="text-primary-600 hover:text-primary-700 font-medium"
                >
                  Register here
                </Link>
              </div>
            </CardFooter>
          </form>
        </Card>
      </div>
    </AppLayout>
  )
}
