import { cn } from '@/lib/utils'
import { ReactNode } from 'react'

type Props = {
  className?: string
  children: ReactNode
}

/**
 * Card Component
 */
export function Card({ className, children }: Props) {
  return (
    <div
      className={cn(
        'rounded-lg border border-border bg-card text-card-foreground shadow-subtle',
        className || ''
      )}
    >
      {children}
    </div>
  )
}

/**
 * Card Header
 */
export function CardHeader({ className, ...props }: Props) {
  return (
    <div
      className={cn('p-6 flex flex-col space-y-1.5', className || '')}
      {...props}
    />
  )
}

/**
 * Card Title
 */
export function CardTitle({ className, ...props }: Props) {
  return (
    <h3
      className={cn(
        'text-lg font-semibold leading-none tracking-tight',
        className || ''
      )}
      {...props}
    />
  )
}

/**
 * Card Description
 */
export function CardDescription({ className, ...props }: Props) {
  return (
    <p
      className={cn('text-sm text-muted-foreground', className || '')}
      {...props}
    />
  )
}

/**
 * Card Content
 */
export function CardContent({ className, ...props }: Props) {
  return (
    <div className={cn('p-6 pt-0', className || '')} {...props} />
  )
}

/**
 * Card Footer
 */
export function CardFooter({ className, ...props }: Props) {
  return (
    <div
      className={cn('flex items-center p-6 pt-0', className || '')}
      {...props}
    />
  )
}
