import { ChevronRight } from 'lucide-react'
import { ReactNode } from 'react'

type ColorVariant = 'primary' | 'secondary' | 'accent'

interface ColorVariantStyles {
  bg: string
  shadow: string
  text: string
  hover: string
}

interface FeatureCardProps {
  icon: ReactNode
  title: string
  description: string
  color: ColorVariant
}

const colorVariants: Record<ColorVariant, ColorVariantStyles> = {
  primary: {
    bg: 'from-primary-500 to-primary-600',
    shadow: 'shadow-primary-100',
    text: 'text-primary-600',
    hover: 'group-hover:text-primary-700',
  },
  secondary: {
    bg: 'from-secondary-500 to-secondary-600',
    shadow: 'shadow-secondary-100',
    text: 'text-secondary-600',
    hover: 'group-hover:text-secondary-700',
  },
  accent: {
    bg: 'from-accent-500 to-accent-600',
    shadow: 'shadow-accent-100',
    text: 'text-accent-600',
    hover: 'group-hover:text-accent-700',
  },
}

export function FeatureCard({
  icon,
  title,
  description,
  color,
}: FeatureCardProps) {
  return (
    <div className="group bg-white p-8 rounded-3xl shadow-xl border border-gray-100 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
      <div
        className={`bg-gradient-to-br ${colorVariants[color].bg} text-white rounded-2xl p-4 inline-block mb-6 shadow-lg ${colorVariants[color].shadow}`}
      >
        {icon}
      </div>
      <h3 className="text-2xl font-semibold text-gray-900 mb-4">
        {title}
      </h3>
      <p className="text-gray-600 leading-relaxed mb-6">
        {description}
      </p>
      <div
        className={`flex items-center ${colorVariants[color].text} font-medium ${colorVariants[color].hover} transition-colors`}
      >
        <span>Learn more</span>
        <ChevronRight className="h-5 w-5 ml-1 group-hover:ml-2 transition-all" />
      </div>
    </div>
  )
}
