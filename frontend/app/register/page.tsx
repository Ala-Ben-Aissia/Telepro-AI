'use client'

import React, { useState } from 'react'
import { useRouter } from 'next/navigation'
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
import { UserCog } from 'lucide-react'

export default function RegisterPage() {
  const router = useRouter()
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    phone_number: '',
    password: '',
    password_confirm: '',
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)
  const [generalError, setGeneralError] = useState<string | null>(
    null
  )

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))

    // Clear error for this field when user types
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev }
        delete newErrors[name]
        return newErrors
      })
    }
  }

  const validateForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.username.trim()) {
      newErrors.username = 'Username is required'
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required'
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid'
    }

    if (!formData.password) {
      newErrors.password = 'Password is required'
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters'
    }

    if (formData.password !== formData.password_confirm) {
      newErrors.password_confirm = 'Passwords do not match'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setGeneralError(null)

    if (!validateForm()) {
      return
    }

    setIsLoading(true)

    try {
      await AuthService.register(formData)
      router.push('/dashboard')
    } catch (err) {
      if (err instanceof Error) {
        setGeneralError(err.message)
      } else {
        setGeneralError('Registration failed. Please try again.')
      }
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
                <UserCog className="h-7 w-7 text-primary-700" />
              </div>
              <CardTitle className="text-2xl font-extrabold text-gray-900">
                Create an Account
              </CardTitle>
              <CardDescription className="text-lg text-gray-600 font-medium">
                Register to access Telepro-AI patient services
              </CardDescription>
            </CardHeader>
            <form
              onSubmit={handleSubmit}
              className="px-6 py-8 space-y-6"
            >
              {generalError && (
                <div className="bg-red-50 text-red-500 p-3 rounded-md text-sm font-semibold text-center">
                  {generalError}
                </div>
              )}
              <Input
                label="Username"
                id="username"
                name="username"
                type="text"
                value={formData.username}
                onChange={handleChange}
                error={errors.username}
                required
                autoComplete="username"
              />
              <Input
                label="Email"
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                error={errors.email}
                required
                autoComplete="email"
              />
              <Input
                label="Phone Number (optional)"
                id="phone_number"
                name="phone_number"
                type="tel"
                value={formData.phone_number}
                onChange={handleChange}
                error={errors.phone_number}
                autoComplete="tel"
              />
              <Input
                label="Password"
                id="password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                error={errors.password}
                required
                autoComplete="new-password"
              />
              <Input
                label="Confirm Password"
                id="password_confirm"
                name="password_confirm"
                type="password"
                value={formData.password_confirm}
                onChange={handleChange}
                error={errors.password_confirm}
                required
                autoComplete="new-password"
              />
              <Button
                type="submit"
                disabled={isLoading}
                size="lg"
                className="w-full font-semibold text-lg shadow-md mt-2"
              >
                {isLoading ? 'Creating Account...' : 'Register'}
              </Button>
            </form>
            <CardFooter className="bg-surface-50 dark:bg-gray-900/60 py-5 px-6 flex flex-col items-center">
              <div className="text-center text-base text-gray-700">
                Already have an account?{' '}
                <Link
                  href="/login"
                  className="text-primary-700 hover:text-primary-900 font-semibold underline underline-offset-2"
                >
                  Login here
                </Link>
              </div>
            </CardFooter>
          </Card>
        </div>
      </div>
    </AppLayout>
  )
}
