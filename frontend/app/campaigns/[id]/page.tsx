import {
  getCampaign,
  getCampaignChannelMetrics,
  getCampaignPerformance,
  getSegments,
} from '@/app/api/actions'
import Link from 'next/link'

export const dynamic = 'force-dynamic'
export const revalidate = 0

export default async function CampaignDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const campaignId = parseInt((await params).id, 10)
  const campaign = await getCampaign(campaignId)
  const performance = await getCampaignPerformance(campaignId)
  const channelMetrics = await getCampaignChannelMetrics(
    String(campaignId),
  )
  const segments = await getSegments()

  if (!campaign) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh]">
        <h1 className="text-2xl font-bold mb-4">
          Campaign Not Found
        </h1>
        <p className="text-gray-600 mb-4">
          The campaign with ID {campaignId} could not be found.
        </p>
        <Link
          href="/campaigns"
          className="text-blue-600 hover:underline"
        >
          Return to Campaigns
        </Link>
      </div>
    )
  }

  // Format dates for display
  const startDate = new Date(campaign.start_date).toLocaleDateString()
  const endDate = new Date(campaign.end_date).toLocaleDateString()

  // Calculate campaign status
  const now = new Date()
  const start = new Date(campaign.start_date)
  const end = new Date(campaign.end_date)

  let timeStatus = 'Scheduled'
  if (now > end) {
    timeStatus = 'Completed'
  } else if (now >= start) {
    timeStatus = 'In Progress'
  }

  return (
    <div className="space-y-8">
      <header className="flex justify-between items-center">
        <div className="flex items-center gap-4">
          <Link
            href="/campaigns"
            className="text-blue-600 hover:underline"
          >
            &larr; Back to Campaigns
          </Link>
          <h1 className="text-2xl font-bold">{campaign.title}</h1>
          <div className="flex gap-2">
            <span
              className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                campaign.is_active
                  ? 'bg-green-100 text-green-800'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              {campaign.is_active ? 'Active' : 'Inactive'}
            </span>
            <span
              className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                timeStatus === 'Completed'
                  ? 'bg-blue-100 text-blue-800'
                  : timeStatus === 'In Progress'
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-purple-100 text-purple-800'
              }`}
            >
              {timeStatus}
            </span>
          </div>
        </div>

        <div className="flex space-x-3">
          <Link
            href={`/campaigns/${campaignId}/edit`}
            className="px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Edit
          </Link>
          <form
            action={`/api/campaigns/${campaignId}/send`}
            method="POST"
          >
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700"
              disabled={
                !campaign.is_active || timeStatus === 'Completed'
              }
            >
              Send Campaign
            </button>
          </form>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Campaign Details */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-5 border-b border-gray-200">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Campaign Details
            </h3>
          </div>
          <div className="px-6 py-5">
            <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-6">
              <div>
                <dt className="text-sm font-medium text-gray-500">
                  Description
                </dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {campaign.description}
                </dd>
              </div>

              <div className="sm:col-span-2 border-t border-gray-200 pt-4">
                <dt className="text-sm font-medium text-gray-500">
                  Schedule
                </dt>
                <dd className="mt-1 text-sm text-gray-900">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <span className="block text-xs text-gray-500">
                        Start Date
                      </span>
                      <span>{startDate}</span>
                    </div>
                    <div>
                      <span className="block text-xs text-gray-500">
                        End Date
                      </span>
                      <span>{endDate}</span>
                    </div>
                  </div>
                </dd>
              </div>

              <div className="sm:col-span-2 border-t border-gray-200 pt-4">
                <dt className="text-sm font-medium text-gray-500">
                  Target Audience
                </dt>
                <dd className="mt-1 text-sm text-gray-900">
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                      <span className="block text-xs text-gray-500 mb-1">
                        Age Groups
                      </span>
                      <div className="flex flex-wrap gap-1">
                        {campaign.target_age_groups.length > 0 ? (
                          campaign.target_age_groups.map(
                            (age: string) => (
                              <span
                                key={age}
                                className="px-2 py-1 bg-blue-50 text-blue-700 rounded-full text-xs"
                              >
                                {age}
                              </span>
                            ),
                          )
                        ) : (
                          <span className="text-gray-500">
                            All ages
                          </span>
                        )}
                      </div>
                    </div>
                    <div>
                      <span className="block text-xs text-gray-500 mb-1">
                        Languages
                      </span>
                      <div className="flex flex-wrap gap-1">
                        {campaign.target_languages.length > 0 ? (
                          campaign.target_languages.map(
                            (lang: string) => (
                              <span
                                key={lang}
                                className="px-2 py-1 bg-purple-50 text-purple-700 rounded-full text-xs"
                              >
                                {lang}
                              </span>
                            ),
                          )
                        ) : (
                          <span className="text-gray-500">
                            All languages
                          </span>
                        )}
                      </div>
                    </div>
                    <div>
                      <span className="block text-xs text-gray-500 mb-1">
                        Locations
                      </span>
                      <div className="flex flex-wrap gap-1">
                        {campaign.target_locations.length > 0 ? (
                          campaign.target_locations.map(
                            (location: string) => (
                              <span
                                key={location}
                                className="px-2 py-1 bg-yellow-50 text-yellow-700 rounded-full text-xs"
                              >
                                {location}
                              </span>
                            ),
                          )
                        ) : (
                          <span className="text-gray-500">
                            All locations
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </dd>
              </div>

              <div className="sm:col-span-2 border-t border-gray-200 pt-4">
                <dt className="text-sm font-medium text-gray-500">
                  Message Templates
                </dt>
                <dd className="mt-1 text-sm text-gray-900">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {campaign.email_template && (
                      <div className="bg-gray-50 p-3 rounded">
                        <span className="block text-xs text-gray-500 mb-1">
                          Email Template
                        </span>
                        <p className="whitespace-pre-wrap">
                          {campaign.email_template}
                        </p>
                      </div>
                    )}
                    {campaign.sms_template && (
                      <div className="bg-gray-50 p-3 rounded">
                        <span className="block text-xs text-gray-500 mb-1">
                          SMS Template
                        </span>
                        <p className="whitespace-pre-wrap">
                          {campaign.sms_template}
                        </p>
                      </div>
                    )}
                  </div>
                </dd>
              </div>
            </dl>
          </div>
        </div>

        {/* Campaign Performance */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Performance
              </h3>
            </div>
            <div className="px-6 py-5">
              {performance ? (
                <dl className="space-y-4">
                  <div>
                    <dt className="text-sm font-medium text-gray-500">
                      Messages Sent
                    </dt>
                    <dd className="mt-1 text-3xl font-semibold text-gray-900">
                      {performance.total_sent || 0}
                    </dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">
                      Delivery Rate
                    </dt>
                    <dd className="mt-1 text-gray-900 flex items-center">
                      <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2">
                        <div
                          className="bg-blue-600 h-2.5 rounded-full"
                          style={{
                            width: `${(
                              (performance.delivered /
                                performance.total_sent || 0) * 100
                            ).toFixed(1)}%`,
                          }}
                        ></div>
                      </div>
                      <span>
                        {(
                          (performance.delivered /
                            performance.total_sent || 0) * 100
                        ).toFixed(1)}
                        %
                      </span>
                    </dd>
                  </div>
                  <div>
                    <dt className="text-sm font-medium text-gray-500">
                      Response Rate
                    </dt>
                    <dd className="mt-1 text-gray-900 flex items-center">
                      <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2">
                        <div
                          className="bg-green-600 h-2.5 rounded-full"
                          style={{
                            width: `${performance.response_rate * 100 || 0}%`,
                          }}
                        ></div>
                      </div>
                      <span>
                        {(performance.response_rate * 100).toFixed(
                          1,
                        ) || 0}
                        %
                      </span>
                    </dd>
                  </div>

                  {channelMetrics?.channel_metrics && (
                    <div className="pt-4 border-t border-gray-200">
                      <dt className="text-sm font-medium text-gray-500 mb-2">
                        Channel Performance
                      </dt>
                      <dd className="space-y-2">
                        {Object.entries(
                          channelMetrics?.channel_metrics,
                        ).map(([channel, metrics]) => {
                          console.log({ channel, metrics })
                          return (
                            <div key={channel}>
                              <div className="flex justify-between text-xs">
                                <span className="capitalize">
                                  {channel}
                                </span>
                                <span>
                                  {(
                                    metrics.response_rate * 100
                                  )?.toFixed(1) || 0}
                                  %
                                </span>
                              </div>
                              <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                  className={`h-2 rounded-full ${
                                    channel === 'EMAIL'
                                      ? 'bg-blue-600'
                                      : channel === 'SMS'
                                        ? 'bg-green-600'
                                        : 'bg-yellow-600'
                                  }`}
                                  style={{
                                    width: `${
                                      (
                                        metrics.response_rate * 100
                                      )?.toFixed(1) ||
                                      0 ||
                                      0
                                    }%`,
                                  }}
                                ></div>
                              </div>
                            </div>
                          )
                        })}
                      </dd>
                    </div>
                  )}
                </dl>
              ) : (
                <div className="text-center py-6">
                  <p className="text-gray-500">
                    No performance data available yet
                  </p>
                </div>
              )}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Associated Segments
              </h3>
            </div>
            <div className="px-6 py-5">
              {segments &&
              segments.filter((segment) =>
                segment.campaigns?.includes(campaignId),
              ).length > 0 ? (
                <ul className="divide-y divide-gray-200">
                  {segments
                    .filter((segment) =>
                      segment.campaigns?.includes(campaignId),
                    )
                    .map((segment) => (
                      <li key={segment.id} className="py-3">
                        <Link
                          href={`/segments/${segment.id}`}
                          className="flex justify-between items-center hover:bg-gray-50 p-2 rounded"
                        >
                          <div>
                            <p className="text-sm font-medium text-gray-900">
                              {segment.name}
                            </p>
                            <p className="text-xs text-gray-500 truncate">
                              {segment.description}
                            </p>
                          </div>
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="h-4 w-4 text-gray-400"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M9 5l7 7-7 7"
                            />
                          </svg>
                        </Link>
                      </li>
                    ))}
                </ul>
              ) : (
                <div className="text-center py-6">
                  <p className="text-gray-500 mb-3">
                    No segments associated with this campaign
                  </p>
                  <Link
                    href={`/segments/new?campaignId=${campaignId}`}
                    className="text-blue-600 text-sm hover:underline"
                  >
                    Create a segment
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
