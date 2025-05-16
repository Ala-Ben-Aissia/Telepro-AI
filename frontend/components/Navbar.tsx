'use client'

import { Button } from '@/components/button'
import { Menu, Shield } from 'lucide-react'
import Link from 'next/link'
import { useState } from 'react'

interface NavBarProps {
  user?: {
    role: 'patient' | 'admin'
  }
}

export default function NavBar({ user }: NavBarProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-lg border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <Shield className="w-8 h-8 text-primary-600" />
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-secondary-600">
              Teleprospection AI
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {user?.role === 'patient' ? (
              <Link
                href="/patient"
                className="text-gray-600 hover:text-primary-600 transition-colors"
              >
                My Consents
              </Link>
            ) : (
              <>
                <Link
                  href="/admin/dashboard"
                  className="text-gray-600 hover:text-primary-600 transition-colors"
                >
                  Dashboard
                </Link>
                <Link
                  href="/admin/consents"
                  className="text-gray-600 hover:text-primary-600 transition-colors"
                >
                  Consents
                </Link>
                <Link
                  href="/admin/templates"
                  className="text-gray-600 hover:text-primary-600 transition-colors"
                >
                  Templates
                </Link>
                <Link
                  href="/admin/analytics"
                  className="text-gray-600 hover:text-primary-600 transition-colors"
                >
                  Analytics
                </Link>
              </>
            )}
            <div className="flex items-center space-x-4">
              <Button variant="outline" className="h-9">
                Profile
              </Button>
              <Link href="/auth/login">
                <Button className="h-9 text-primary-100 bg-primary-600 hover:bg-primary-700">
                  {user ? 'Logout' : 'Login'}
                </Button>
              </Link>
            </div>
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2 rounded-lg hover:bg-gray-100"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <Menu className="w-6 h-6 text-gray-600" />
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-100">
            <div className="flex flex-col space-y-4">
              {user?.role === 'patient' ? (
                <Link
                  href="/patient"
                  className="text-gray-600 hover:text-primary-600 transition-colors px-2 py-1"
                >
                  My Consents
                </Link>
              ) : (
                <>
                  <Link
                    href="/admin"
                    className="text-gray-600 hover:text-primary-600 transition-colors px-2 py-1"
                  >
                    Dashboard
                  </Link>
                  <Link
                    href="/admin/consents"
                    className="text-gray-600 hover:text-primary-600 transition-colors px-2 py-1"
                  >
                    Consents
                  </Link>
                  <Link
                    href="/admin/templates"
                    className="text-gray-600 hover:text-primary-600 transition-colors px-2 py-1"
                  >
                    Templates
                  </Link>
                  <Link
                    href="/admin/analytics"
                    className="text-gray-600 hover:text-primary-600 transition-colors px-2 py-1"
                  >
                    Analytics
                  </Link>
                </>
              )}
              <div className="flex flex-col space-y-2 pt-2 border-t border-gray-100">
                <Button
                  variant="outline"
                  className="w-full justify-center h-9"
                >
                  Profile
                </Button>
                <Link href={user ? '/auth/logout' : '/auth/login'}>
                  <Button className="w-full justify-center h-9 text-primary-100 bg-primary-600 hover:bg-primary-700">
                    {user ? 'Logout' : 'Login'}
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}
