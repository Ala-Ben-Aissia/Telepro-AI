// Pricing Card Component
export function PricingCard({
  title,
  price,
  description,
  features,
  buttonText,
  color,
  popular,
}) {
  const colorVariants = {
    primary: {
      bg: 'bg-primary-50',
      text: 'text-primary-600',
      border: 'border-primary-200',
      button: 'bg-primary-600 hover:bg-primary-700 text-white',
      badge: 'bg-primary-100 text-primary-700',
    },
    secondary: {
      bg: 'bg-secondary-50',
      text: 'text-secondary-600',
      border: 'border-secondary-200',
      button: 'bg-secondary-600 hover:bg-secondary-700 text-white',
      badge: 'bg-secondary-100 text-secondary-700',
    },
    gray: {
      bg: 'bg-gray-50',
      text: 'text-gray-600',
      border: 'border-gray-200',
      button: 'bg-gray-600 hover:bg-gray-700 text-white',
      badge: 'bg-gray-100 text-gray-700',
    },
  }

  return (
    <div
      className={`relative rounded-2xl ${
        colorVariants[color].bg
      } border ${colorVariants[color].border} p-8 ${
        popular ? 'ring-2 ring-primary-500 shadow-2xl' : 'shadow-xl'
      } transition-all duration-300 hover:-translate-y-1`}
    >
      {popular && (
        <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 px-4 py-1 rounded-full bg-primary-600 text-white text-sm font-bold">
          Most Popular
        </div>
      )}

      <div className="text-center mb-8">
        <h3 className="text-xl font-bold text-gray-900 mb-2">
          {title}
        </h3>
        <div className="text-3xl font-extrabold text-gray-900 mb-2">
          {price}
          <span className="text-sm font-normal text-gray-500">
            /month
          </span>
        </div>
        <p className="text-gray-600 text-sm">{description}</p>
      </div>

      <ul className="space-y-3 mb-8">
        {features.map((feature, index) => (
          <li key={index} className="flex items-center gap-2">
            <Check
              className={`h-5 w-5 ${colorVariants[color].text}`}
            />
            <span className="text-gray-700">{feature}</span>
          </li>
        ))}
      </ul>

      <button
        className={`w-full py-3 px-4 rounded-lg font-semibold ${colorVariants[color].button} shadow-md hover:shadow-lg transition-all duration-300`}
      >
        {buttonText}
      </button>
    </div>
  )
}
