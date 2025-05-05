'use client'

import React from 'react'
import Link from 'next/link'
import { cn } from '@/lib/utils'

interface AppLayoutProps {
  children: React.ReactNode
  userType?: 'STAFF' | 'PATIENT'
}

export function AppLayout({ children, userType }: AppLayoutProps) {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10 dark:bg-gray-900 dark:border-gray-800">
        <div className="container mx-auto px-4 py-3 flex items-center justify-between">
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-primary-700 font-bold text-xl dark:text-primary-400">
              Telepro-AI
            </span>
          </Link>
          <nav className="hidden md:flex items-center space-x-6">
            {userType === 'STAFF' ? (
              <>
                <NavLink href="/admin/dashboard">Dashboard</NavLink>
                <NavLink href="/admin/patients">Patients</NavLink>
                <NavLink href="/admin/campaigns">Campaigns</NavLink>
                <NavLink href="/admin/analytics">Analytics</NavLink>
              </>
            ) : userType === 'PATIENT' ? (
              <>
                <NavLink href="/dashboard">Dashboard</NavLink>
                <NavLink href="/preferences">Preferences</NavLink>
                <NavLink href="/communications">
                  Communications
                </NavLink>
              </>
            ) : (
              <>
                <NavLink href="/login">Login</NavLink>
                <NavLink href="/register">Register</NavLink>
              </>
            )}
          </nav>
          {userType && (
            <div className="flex items-center space-x-4">
              <button className="text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200">
                <span className="sr-only">User menu</span>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
              </button>
            </div>
          )}
        </div>
      </header>
      <main className="flex-1 container mx-auto px-4 py-8">
        {children}
      </main>
      <footer className="bg-white border-t border-gray-200 py-6 dark:bg-gray-900 dark:border-gray-800">
        <div className="container mx-auto px-4 text-center text-gray-500 text-sm dark:text-gray-400">
          &copy; {new Date().getFullYear()} Telepro-AI. All rights
          reserved.
        </div>
      </footer>
    </div>
  )
}

interface NavLinkProps
  extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  href: string
  children: React.ReactNode
}

function NavLink({
  href,
  children,
  className,
  ...props
}: NavLinkProps) {
  return (
    <Link
      href={href}
      className={cn(
        'text-gray-600 hover:text-primary-700 font-medium dark:text-gray-300 dark:hover:text-primary-400',
        className
      )}
      {...props}
    >
      {children}
    </Link>
  )
}
