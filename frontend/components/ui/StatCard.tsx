// Stat Card Component
export function StatCard({ number, label, icon, color }) {
  const colorVariants = {
    primary: 'bg-primary-50 text-primary-600 border-primary-100',
    secondary:
      'bg-secondary-50 text-secondary-600 border-secondary-100',
    accent: 'bg-accent-300/10 text-accent-600 border-accent-400/20',
  }

  return (
    <div
      className={`p-6 rounded-xl ${colorVariants[color]} border backdrop-blur-sm bg-white/80 hover:shadow-lg transition-shadow duration-300 group`}
    >
      <div className="flex items-center gap-4">
        <div className="p-3 rounded-lg bg-white shadow-sm group-hover:shadow-md transition-shadow duration-300">
          {icon}
        </div>
        <div>
          <div className="text-3xl font-bold">{number}</div>
          <div className="text-sm text-gray-600">{label}</div>
        </div>
      </div>
    </div>
  )
}
