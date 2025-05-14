import DashboardSummary from '@/components/DashboardSummary'
import Link from 'next/link'

export default async function DashboardPage() {
  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-gray-500 mt-1">
          Welcome to your Telepro-AI dashboard
        </p>
      </header>

      {/* Dashboard summary with key metrics and recent campaigns */}
      <DashboardSummary />

      {/* Quick Actions Section */}
      <section>
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <QuickActionCard
            title="Create New Campaign"
            description="Set up a new campaign to engage with your patients"
            icon="📣"
            link="/campaigns/new"
          />
          <QuickActionCard
            title="Generate ML Segments"
            description="Use AI to automatically create patient segments"
            icon="🧠"
            link="/segments/ml"
          />
          <QuickActionCard
            title="Import Patient Data"
            description="Add new patients or update existing records"
            icon="📋"
            link="/patients/import"
          />
        </div>
      </section>

      {/* Resources Section */}
      <section className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-5 border-b border-gray-200">
          <h2 className="text-lg font-medium text-gray-900">
            Resources & Documentation
          </h2>
        </div>
        <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          <ResourceCard
            title="User Guide"
            description="Learn how to use all the features of Telepro-AI effectively"
            link="#"
          />
          <ResourceCard
            title="API Documentation"
            description="Technical details for integrating with our API"
            link="http://localhost:8000/api/redoc"
          />
          <ResourceCard
            title="Best Practices"
            description="Tips for maximizing engagement and response rates"
            link="#"
          />
          <ResourceCard
            title="Compliance Guidelines"
            description="Understand healthcare communication regulations"
            link="#"
          />
        </div>
      </section>
    </div>
  )
}

function QuickActionCard({
  title,
  description,
  icon,
  link,
}: {
  title: string
  description: string
  icon: string
  link: string
}) {
  return (
    <Link
      href={link}
      className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
    >
      <div className="flex items-start">
        <div className="flex-shrink-0 mr-4">
          <span className="text-2xl">{icon}</span>
        </div>
        <div>
          <h3 className="text-lg font-medium text-gray-900">
            {title}
          </h3>
          <p className="mt-1 text-sm text-gray-500">{description}</p>
        </div>
      </div>
    </Link>
  )
}

function ResourceCard({
  title,
  description,
  link,
}: {
  title: string
  description: string
  link: string
}) {
  return (
    <a
      href={link}
      className="block p-4 border border-gray-200 rounded-lg hover:bg-blue-50 transition-colors"
    >
      <h3 className="font-medium text-blue-600">{title}</h3>
      <p className="mt-1 text-sm text-gray-600">{description}</p>
    </a>
  )
}
