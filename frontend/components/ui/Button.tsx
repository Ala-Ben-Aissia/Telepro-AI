import { cn } from '@/lib/utils'
import { ButtonHTMLAttributes } from 'react'

type ButtonVariant =
  | 'primary'
  | 'secondary'
  | 'outline'
  | 'ghost'
  | 'link'
  | 'destructive'
type ButtonSize = 'default' | 'sm' | 'lg' | 'icon'

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode
  variant?: ButtonVariant
  size?: ButtonSize
  className?: string
  disabled?: boolean
}

/**
 * Button component with multiple variants
 */
export function Button({
  children,
  variant = 'primary',
  size = 'default',
  className,
  disabled = false,
  type = 'button',
  ...props
}: ButtonProps) {
  return (
    <button
      type={type}
      disabled={disabled}
      className={cn(
        // Base styles
        'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
        'disabled:opacity-50 disabled:pointer-events-none',

        // Size variants
        size === 'default' ? 'h-10 py-2 px-4' : '',
        size === 'sm' ? 'h-8 px-3 text-sm' : '',
        size === 'lg' ? 'h-12 px-6 text-lg' : '',
        size === 'icon' ? 'h-10 w-10' : '',

        // Style variants
        variant === 'primary'
          ? 'bg-primary text-primary-foreground hover:bg-primary-600 dark:hover:bg-primary-400'
          : '',
        variant === 'secondary'
          ? 'bg-secondary text-secondary-foreground hover:bg-secondary-500 dark:hover:bg-secondary-300'
          : '',
        variant === 'outline'
          ? 'border border-input bg-background hover:bg-muted hover:text-foreground'
          : '',
        variant === 'ghost'
          ? 'hover:bg-muted hover:text-foreground'
          : '',
        variant === 'link'
          ? 'text-primary underline-offset-4 hover:underline'
          : '',
        variant === 'destructive'
          ? 'bg-destructive text-destructive-foreground hover:bg-destructive/90'
          : '',

        className || ''
      )}
      {...props}
    >
      {children}
    </button>
  )
}
