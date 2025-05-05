import './globals.css'
import { Geist } from 'next/font/google'

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
})

import { Providers } from './providers'
import { PropsWithChildren } from 'react'

export const metadata = {
  title: 'Telepro-AI',
  description: 'Intelligent telehealth communication platform',
}

export default function RootLayout({ children }: PropsWithChildren) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={geistSans.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
