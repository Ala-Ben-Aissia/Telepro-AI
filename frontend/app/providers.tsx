'use client'

import { ThemeProvider } from '@/components/ThemeProvider'
import { PropsWithChildren } from 'react'

/**
 * Application providers wrapper
 */
export function Providers({ children }: PropsWithChildren) {
  return (
    <ThemeProvider defaultTheme="system" storageKey="telepro-theme">
      {children}
    </ThemeProvider>
  )
}
