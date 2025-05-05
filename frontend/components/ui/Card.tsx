import React from 'react'
import { cn } from '@/lib/utils'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'bordered'
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'default', ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'rounded-lg bg-white shadow-sm dark:bg-card-background dark:shadow-md dark:shadow-black/5',
          variant === 'bordered' &&
            'border border-gray-200 dark:border-gray-800',
          className
        )}
        {...props}
      />
    )
  }
)
Card.displayName = 'Card'

interface CardHeaderProps
  extends React.HTMLAttributes<HTMLDivElement> {}

const CardHeader = React.forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'px-6 py-4 border-b border-gray-100 dark:border-gray-800',
          className
        )}
        {...props}
      />
    )
  }
)
CardHeader.displayName = 'CardHeader'

interface CardTitleProps
  extends React.HTMLAttributes<HTMLHeadingElement> {}

const CardTitle = React.forwardRef<
  HTMLHeadingElement,
  CardTitleProps
>(({ className, ...props }, ref) => {
  return (
    <h3
      ref={ref}
      className={cn(
        'text-lg font-semibold text-gray-900 dark:text-gray-100',
        className
      )}
      {...props}
    />
  )
})
CardTitle.displayName = 'CardTitle'

interface CardDescriptionProps
  extends React.HTMLAttributes<HTMLParagraphElement> {}

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  CardDescriptionProps
>(({ className, ...props }, ref) => {
  return (
    <p
      ref={ref}
      className={cn(
        'text-sm text-gray-500 dark:text-gray-400',
        className
      )}
      {...props}
    />
  )
})
CardDescription.displayName = 'CardDescription'

interface CardContentProps
  extends React.HTMLAttributes<HTMLDivElement> {}

const CardContent = React.forwardRef<
  HTMLDivElement,
  CardContentProps
>(({ className, ...props }, ref) => {
  return (
    <div
      ref={ref}
      className={cn('px-6 py-4', className)}
      {...props}
    />
  )
})
CardContent.displayName = 'CardContent'

interface CardFooterProps
  extends React.HTMLAttributes<HTMLDivElement> {}

const CardFooter = React.forwardRef<HTMLDivElement, CardFooterProps>(
  ({ className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'px-6 py-4 border-t border-gray-100 dark:border-gray-800',
          className
        )}
        {...props}
      />
    )
  }
)
CardFooter.displayName = 'CardFooter'

export {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
}
