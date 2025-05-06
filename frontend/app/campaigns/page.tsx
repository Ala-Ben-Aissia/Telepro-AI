import { getCampaigns } from '@/app/api/actions'
import Link from 'next/link'

export const dynamic = 'force-dynamic'
export const revalidate = 0

export default async function CampaignsPage({
  searchParams,
}: {
  searchParams: Promise<{
    [key: string]: 'active' | 'inactive' | 'all'
  }>
}) {
  // Extract filter params from URL query string
  const params = await searchParams
  const status =
    typeof params.status === 'string' ? params.status : 'all'
  // Fetch campaigns with filters
  const campaigns = await getCampaigns(status)

  return (
    <div className="space-y-8">
      <header className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">Campaigns</h1>
          <p className="text-gray-600">
            Manage and view teleprospection campaigns
          </p>
        </div>

        <div className="flex gap-4">
          {/* Filter buttons */}
          <div className="flex space-x-2">
            <Link
              href="/campaigns"
              className={`px-3 p-2 rounded-full text-sm ${
                status === 'all'
                  ? 'bg-blue-100 text-blue-800'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              All
            </Link>
            <Link
              href="/campaigns?status=active"
              className={`px-3 p-2 rounded-full text-sm ${
                status === 'active'
                  ? 'bg-green-100 text-green-800'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              Active
            </Link>
            <Link
              href="/campaigns?status=inactive"
              className={`px-3 p-2 rounded-full text-sm ${
                status === 'inactive'
                  ? 'bg-red-100 text-red-800'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              Inactive
            </Link>
          </div>

          {/* Create campaign button */}
          <Link
            href="/campaigns/new"
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4 mr-2"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
            New Campaign
          </Link>
        </div>
      </header>

      {/* Campaigns Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {campaigns.length > 0 ? (
          campaigns.map((campaign) => (
            <Link
              key={campaign.id}
              href={`/campaigns/${campaign.id}`}
              className="bg-white rounded-lg shadow hover:shadow-md transition-shadow duration-200"
            >
              <div className="p-6 border-b border-gray-200">
                <div className="flex justify-between items-start">
                  <h2 className="text-xl font-semibold text-gray-900 line-clamp-1">
                    {campaign.title}
                  </h2>
                  <span
                    className={`px-2 p-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      campaign.is_active
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {campaign.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                <p className="mt-2 text-sm text-gray-600 line-clamp-2">
                  {campaign.description}
                </p>
              </div>

              <div className="p-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-xs text-gray-500 font-medium">
                      Start Date
                    </div>
                    <div className="mt-1">
                      {new Date(
                        campaign.start_date
                      ).toLocaleDateString()}
                    </div>
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 font-medium">
                      End Date
                    </div>
                    <div className="mt-1">
                      {new Date(
                        campaign.end_date
                      ).toLocaleDateString()}
                    </div>
                  </div>
                </div>

                <div className="mt-4">
                  <div className="text-xs text-gray-500 font-medium">
                    Target Demographics
                  </div>
                  <div className="mt-1 flex flex-wrap gap-2">
                    {campaign.target_age_groups.length > 0 &&
                      campaign.target_age_groups.map(
                        (age: string) => (
                          <span
                            key={age}
                            className="px-2 p-2 bg-blue-50 text-blue-700 rounded-full text-xs"
                          >
                            {age}
                          </span>
                        )
                      )}
                    {campaign.target_languages.length > 0 &&
                      campaign.target_languages.map(
                        (lang: string) => (
                          <span
                            key={lang}
                            className="px-2 p-2 bg-purple-50 text-purple-700 rounded-full text-xs"
                          >
                            {lang}
                          </span>
                        )
                      )}
                    {campaign.target_locations.length > 0 &&
                      campaign.target_locations.map(
                        (location: string) => (
                          <span
                            key={location}
                            className="px-2 p-2 bg-yellow-50 text-yellow-700 rounded-full text-xs"
                          >
                            {location}
                          </span>
                        )
                      )}
                  </div>
                </div>
              </div>
            </Link>
          ))
        ) : (
          <div className="col-span-3 bg-white rounded-lg shadow p-10 text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              No campaigns found
            </h3>
            <p className="text-gray-600 mb-6">
              Create your first campaign to start engaging with
              patients
            </p>
            <Link
              href="/campaigns/new"
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4 mr-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 4v16m8-8H4"
                />
              </svg>
              New Campaign
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}
