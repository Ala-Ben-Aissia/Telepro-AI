/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  darkMode: 'media', // 'media' for system preference, 'class' for manual toggle
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f5ff',
          100: '#e0ebff',
          200: '#c7d9ff',
          300: '#a4beff',
          400: '#8099ff',
          500: '#5c73ff', // Refined blue
          600: '#4154e6',
          700: '#303dc4', // Rich blue
          800: '#2632a0',
          900: '#1c2582',
        },
        secondary: {
          50: '#f0fdfb',
          100: '#ccf9f0',
          200: '#99f0e5',
          300: '#5ce1d6',
          400: '#36cbc0',
          500: '#20b2a8', // Premium teal
          600: '#198f87',
          700: '#136e68',
          800: '#0e534f',
          900: '#0a3f3c',
        },
        accent: {
          300: '#ffd166', // Softer gold
          400: '#fcb900', // Premium gold
          500: '#f59e0b',
          600: '#d97706',
        },
        surface: {
          50: '#fafbff',
          100: '#f7f8fd',
          200: '#eef0f9',
        },
      },
      fontFamily: {
        sans: ['var(--font-geist-sans)'],
        mono: ['var(--font-geist-mono)'],
      },
      backgroundColor: {
        dark: '#121212',
        'dark-card': '#1e1e1e',
      },
      textColor: {
        dark: {
          primary: '#ffffff',
          secondary: '#a0aec0',
        },
      },
    },
  },
  plugins: [],
}
