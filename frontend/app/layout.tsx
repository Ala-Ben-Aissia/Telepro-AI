import type { Metadata } from 'next'
import { Geist, Geist_Mono } from 'next/font/google'
import './globals.css'
import Navigation from '@/components/Navigation'
import { Providers } from '@/components/Providers'
import { getCurrentUser } from './api/actions'

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
})

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
})

export const metadata: Metadata = {
  title: 'Telepro-AI | AI-Powered Patient Teleprospection System',
  description:
    'An intelligent system for patient segmentation, proactive identification and optimized healthcare campaigns',
}

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  const user = await getCurrentUser()
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen bg-gray-50`}
      >
        <Providers>
          <div className="flex min-h-screen">
            {user ? <Navigation /> : null}
            {user ? (
              <main className="flex-1 p-6">{children}</main>
            ) : (
              <main className="flex items-center justify-center w-full">
                {children}
              </main>
            )}
          </div>
        </Providers>
      </body>
    </html>
  )
}
