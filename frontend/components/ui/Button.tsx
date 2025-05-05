import React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none',
  {
    variants: {
      variant: {
        default:
          'bg-primary-500 text-white hover:bg-primary-600 dark:bg-primary-600 dark:hover:bg-primary-700',
        secondary:
          'bg-secondary-500 text-white hover:bg-secondary-600 dark:bg-secondary-600 dark:hover:bg-secondary-700',
        accent:
          'bg-accent-400 text-white hover:bg-accent-500 dark:bg-accent-500 dark:hover:bg-accent-600',
        outline:
          'border border-primary-200 bg-transparent hover:bg-primary-50 text-primary-700 dark:border-primary-700 dark:text-primary-400 dark:hover:bg-primary-900/30',
        ghost:
          'bg-transparent hover:bg-primary-50 text-primary-700 dark:text-primary-400 dark:hover:bg-primary-900/30',
        link: 'bg-transparent underline-offset-4 hover:underline text-primary-700 hover:bg-transparent dark:text-primary-400',
        destructive:
          'bg-red-500 text-white hover:bg-red-600 dark:bg-red-700 dark:hover:bg-red-800',
      },
      size: {
        default: 'h-10 py-2 px-4',
        sm: 'h-8 px-3 text-xs',
        lg: 'h-12 px-6 text-base',
        icon: 'h-10 w-10',
      },
      fullWidth: {
        true: 'w-full',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
      fullWidth: false,
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant,
      size,
      fullWidth,
      asChild = false,
      ...props
    },
    ref
  ) => {
    return (
      <button
        className={cn(
          buttonVariants({ variant, size, fullWidth, className })
        )}
        ref={ref}
        {...props}
      />
    )
  }
)

Button.displayName = 'Button'

export { Button, buttonVariants }
