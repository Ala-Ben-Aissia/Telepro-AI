'use client'
import '../../app/globals.css'
import { useState, useEffect, ReactNode } from 'react'
import Link from 'next/link'
import { cn } from '@/lib/utils'
import { ThemeToggle } from '@/components/ThemeToggle'
import {
  User,
  LogIn,
  UserCog,
  Users,
  BarChart3,
  MessageCircle,
  Settings,
  Home,
  Menu,
  X,
} from 'lucide-react'

type AppLayoutProps = {
  children: ReactNode
  userType?: 'STAFF' | 'PATIENT'
}

/**
 * Main application layout wrapper
 */
export function AppLayout({ children, userType }: AppLayoutProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  // Close mobile menu when window resizes
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        setMobileMenuOpen(false)
      }
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return (
    <div className="min-h-screen flex flex-col font-sans bg-surface-50 dark:bg-surface-50">
      <header className="bg-background/80 backdrop-blur-sm border-b border-border sticky top-0 z-20 shadow-subtle">
        <div className="container flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-2 group">
            <Home className="h-6 w-6 text-primary group-hover:scale-110 transition-transform" />
            <span className="text-primary font-extrabold text-xl tracking-tight">
              Telepro-AI
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            {userType === 'STAFF' ? (
              <StaffNavigation />
            ) : userType === 'PATIENT' ? (
              <PatientNavigation />
            ) : (
              <GuestNavigation />
            )}
          </nav>

          <div className="flex items-center gap-3">
            {/* Dark mode toggle using our ThemeProvider component */}
            <ThemeToggle />

            {/* User menu if logged in */}
            {userType && (
              <button className="rounded-full border border-border bg-background/50 p-2 hover:shadow-md transition text-primary">
                <span className="sr-only">User menu</span>
                <User className="h-5 w-5" />
              </button>
            )}

            {/* Mobile menu toggle */}
            <button
              className="md:hidden rounded-md p-2 text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Toggle mobile menu"
            >
              {mobileMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-border bg-background">
            <nav className="flex flex-col py-4">
              {userType === 'STAFF' ? (
                <StaffNavigation mobile />
              ) : userType === 'PATIENT' ? (
                <PatientNavigation mobile />
              ) : (
                <GuestNavigation mobile />
              )}
            </nav>
          </div>
        )}
      </header>

      <main className="flex-1 container py-8">{children}</main>

      <footer className="bg-background/80 backdrop-blur-sm border-t border-border py-6 mt-auto">
        <div className="container text-center text-muted-foreground text-sm">
          &copy; {new Date().getFullYear()} Telepro-AI. All rights
          reserved.
        </div>
      </footer>
    </div>
  )
}

/**
 * Navigation component for staff users
 */
function StaffNavigation({ mobile = false }) {
  return (
    <>
      <NavLink href="/admin/dashboard" mobile={mobile}>
        <BarChart3 className="h-4 w-4 mr-2" />
        Dashboard
      </NavLink>
      <NavLink href="/admin/patients" mobile={mobile}>
        <Users className="h-4 w-4 mr-2" />
        Patients
      </NavLink>
      <NavLink href="/admin/campaigns" mobile={mobile}>
        <MessageCircle className="h-4 w-4 mr-2" />
        Campaigns
      </NavLink>
      <NavLink href="/admin/analytics" mobile={mobile}>
        <BarChart3 className="h-4 w-4 mr-2" />
        Analytics
      </NavLink>
    </>
  )
}

/**
 * Navigation component for patient users
 */
function PatientNavigation({ mobile = false }) {
  return (
    <>
      <NavLink href="/dashboard" mobile={mobile}>
        <User className="h-4 w-4 mr-2" />
        Dashboard
      </NavLink>
      <NavLink href="/preferences" mobile={mobile}>
        <Settings className="h-4 w-4 mr-2" />
        Preferences
      </NavLink>
      <NavLink href="/communications" mobile={mobile}>
        <MessageCircle className="h-4 w-4 mr-2" />
        Communications
      </NavLink>
    </>
  )
}

/**
 * Navigation component for guest users
 */
function GuestNavigation({ mobile = false }) {
  return (
    <>
      <NavLink href="/login" mobile={mobile}>
        <LogIn className="h-4 w-4 mr-2" />
        Login
      </NavLink>
      <NavLink href="/register" mobile={mobile}>
        <UserCog className="h-4 w-4 mr-2" />
        Register
      </NavLink>
    </>
  )
}

type Props = {
  href: string
  children: ReactNode
  className?: string
  mobile: boolean
}

/**
 * Navigation link component
 */
function NavLink({
  href,
  children,
  className = '',
  mobile = false,
  ...props
}: Props) {
  return (
    <Link
      href={href}
      className={cn(
        'flex items-center transition-colors',
        mobile
          ? 'px-6 py-3 text-foreground hover:bg-muted w-full'
          : 'text-muted-foreground hover:text-foreground font-medium',
        className
      )}
      {...props}
    >
      {children}
    </Link>
  )
}
