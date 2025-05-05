/**
 * Conditionally join class names together
 *
 * @param  {...string} classes - CSS class names to join
 * @returns {string} - Joined class names
 */
export function cn(...classes: string[]): string {
  return classes.filter(Boolean).join(' ')
}

/**
 * Format a date to a locale string
 *
 * @param {Date|string|number} date - Date to format
 * @param {Intl.DateTimeFormatOptions} options - Format options
 * @returns {string} - Formatted date
 */
export function formatDate(
  date: Date | string | number,
  options: Intl.DateTimeFormatOptions = {}
): string {
  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }

  const mergedOptions = { ...defaultOptions, ...options }
  return new Date(date).toLocaleDateString(undefined, mergedOptions)
}

/**
 * Format a number as currency
 *
 * @param {number} amount - Amount to format
 * @param {string} currency - Currency code (e.g., 'USD')
 * @returns {string} - Formatted currency string
 */
export function formatCurrency(
  amount: number,
  currency: string = 'USD'
): string {
  return new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency,
  }).format(amount)
}

/**
 * Truncate text to a specific length
 *
 * @param {string} text - Text to truncate
 * @param {number} length - Maximum length
 * @returns {string} - Truncated text
 */
export function truncateText(
  text: string,
  length: number = 100
): string {
  if (!text || text.length <= length) return text
  return text.slice(0, length).trim() + '...'
}

/**
 * Debounce a function call
 *
 * @param {Function} fn - Function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {Function} - Debounced function
 */
export function debounce<T extends (...args: unknown[]) => void>(
  fn: T,
  delay: number = 300
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout | undefined
  return (...args: Parameters<T>) => {
    if (timeoutId) clearTimeout(timeoutId)
    timeoutId = setTimeout(() => {
      fn(...args)
    }, delay)
  }
}

/**
 * Generate a random ID
 *
 * @param {number} length - Length of the ID
 * @returns {string} - Random ID
 */
export function generateId(length: number = 8): string {
  return Math.random()
    .toString(36)
    .substring(2, length + 2)
}

/**
 * Check if an element is in viewport
 *
 * @param {HTMLElement} element - Element to check
 * @param {number} offset - Offset in pixels
 * @returns {boolean} - Whether element is in viewport
 */
export function isElementInViewport(
  element: HTMLElement,
  offset: number = 0
): boolean {
  if (!element) return false

  const rect = element.getBoundingClientRect()

  return (
    rect.top >= 0 - offset &&
    rect.left >= 0 - offset &&
    rect.bottom <=
      (window.innerHeight || document.documentElement.clientHeight) +
        offset &&
    rect.right <=
      (window.innerWidth || document.documentElement.clientWidth) +
        offset
  )
}
