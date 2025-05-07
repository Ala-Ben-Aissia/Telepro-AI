import Navigation from '@/components/Navigation'
import { PropsWithChildren } from 'react'

export default function LayoutPage({ children }: PropsWithChildren) {
  return (
    <>
      <div className="flex min-h-screen">
        <Navigation />
        <main className="flex-1 p-6">{children}</main>
      </div>
    </>
  )
}
