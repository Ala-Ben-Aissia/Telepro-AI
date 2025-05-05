import * as React from 'react'
import { cn } from '@/lib/utils'

interface InputProps extends React.ComponentProps<'input'> {
  label?: string
  error?: string
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, label, error, id, ...props }, ref) => {
    return (
      <div className="space-y-2 w-full">
        {label && (
          <label
            htmlFor={id}
            className="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-1"
          >
            {label}
          </label>
        )}
        <input
          ref={ref}
          type={type}
          id={id}
          data-slot="input"
          className={cn(
            'file:text-foreground placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground border-input flex h-12 w-full min-w-0 rounded-lg border bg-white dark:bg-gray-900 px-4 py-3 text-base shadow-xs transition-[color,box-shadow] outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50',
            'focus-visible:border-primary-500 focus-visible:ring-2 focus-visible:ring-primary-200',
            error ? 'border-red-500 focus-visible:ring-red-200' : '',
            className || ''
          )}
          aria-invalid={!!error}
          {...props}
        />
        {error && (
          <p className="text-xs text-red-500 font-medium mt-1">
            {error}
          </p>
        )}
      </div>
    )
  }
)
Input.displayName = 'Input'

export { Input }
