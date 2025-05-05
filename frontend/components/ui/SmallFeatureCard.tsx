// Small Feature Card Component
export function SmallFeatureCard({
  icon,
  title,
  description,
  color,
}) {
  const colorVariants = {
    primary: {
      bg: 'bg-primary-50/50',
      border: 'border-primary-100/50',
      text: 'text-primary-600',
    },
    secondary: {
      bg: 'bg-secondary-50/50',
      border: 'border-secondary-100/50',
      text: 'text-secondary-600',
    },
    accent: {
      bg: 'bg-accent-300/5',
      border: 'border-accent-400/10',
      text: 'text-accent-600',
    },
  }

  return (
    <div
      className={`p-6 rounded-xl ${colorVariants[color].bg} ${colorVariants[color].border} border group hover:shadow-lg transition-all duration-300`}
    >
      <div className="flex items-start gap-4">
        <div
          className={`p-2 rounded-lg bg-white ${colorVariants[color].text} shadow-sm`}
        >
          {icon}
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            {title}
          </h3>
          <p className="text-gray-600 text-sm">{description}</p>
        </div>
      </div>
    </div>
  )
}
