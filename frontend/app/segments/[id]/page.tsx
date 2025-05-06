import {
  getSegment,
  getSegmentPatients,
  analyzeSegment,
  getCampaigns,
} from '@/app/api/actions'
import Link from 'next/link'

export const dynamic = 'force-dynamic'
export const revalidate = 0

export default async function SegmentDetailPage({
  params,
}: {
  params: { id: string }
}) {
  const segmentId = parseInt(params.id, 10)
  const segment = await getSegment(segmentId)
  const patients = await getSegmentPatients(segmentId)
  const analysis = await analyzeSegment(segmentId)
  const campaigns = await getCampaigns({ segment_id: segmentId })

  if (!segment) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh]">
        <h1 className="text-2xl font-bold mb-4">Segment Not Found</h1>
        <p className="text-gray-600 mb-4">
          The segment with ID {segmentId} could not be found.
        </p>
        <Link
          href="/segments"
          className="text-blue-600 hover:underline"
        >
          Return to Segments
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <header className="flex justify-between items-center">
        <div className="flex items-center gap-4">
          <Link
            href="/segments"
            className="text-blue-600 hover:underline"
          >
            &larr; Back to Segments
          </Link>
          <h1 className="text-2xl font-bold">{segment.name}</h1>
          <span
            className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
              segment.is_active
                ? 'bg-green-100 text-green-800'
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            {segment.is_active ? 'Active' : 'Inactive'}
          </span>
        </div>

        <div className="flex space-x-3">
          <Link
            href={`/segments/${segmentId}/edit`}
            className="px-4 py-2 bg-white border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            Edit
          </Link>
          <Link
            href={`/campaigns/new?segmentId=${segmentId}`}
            className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700"
          >
            Create Campaign
          </Link>
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Segment Details */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Segment Details
              </h3>
            </div>
            <div className="px-6 py-5">
              <dl className="grid grid-cols-1 gap-x-4 gap-y-6">
                <div>
                  <dt className="text-sm font-medium text-gray-500">
                    Description
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {segment.description}
                  </dd>
                </div>

                <div className="border-t border-gray-200 pt-4">
                  <dt className="text-sm font-medium text-gray-500">
                    Segmentation Criteria
                  </dt>
                  <dd className="mt-1">
                    <div className="bg-gray-50 p-4 rounded overflow-x-auto">
                      <pre className="text-sm text-gray-900 whitespace-pre-wrap">
                        {JSON.stringify(segment.criteria, null, 2)}
                      </pre>
                    </div>
                  </dd>
                </div>

                <div className="border-t border-gray-200 pt-4">
                  <dt className="text-sm font-medium text-gray-500">
                    Created & Updated
                  </dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <span className="block text-xs text-gray-500">
                          Created
                        </span>
                        <span>
                          {new Date(
                            segment.created_at
                          ).toLocaleDateString()}
                        </span>
                      </div>
                      <div>
                        <span className="block text-xs text-gray-500">
                          Last Updated
                        </span>
                        <span>
                          {new Date(
                            segment.updated_at
                          ).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </dd>
                </div>
              </dl>
            </div>
          </div>

          {/* Patient List */}
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Patients in Segment
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Showing {patients.length} patients matching this
                segment's criteria
              </p>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      ID
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Email
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Age Group
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Location
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Engagement
                    </th>
                    <th
                      scope="col"
                      className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      Consent
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {patients.length > 0 ? (
                    patients.map((patient) => (
                      <tr
                        key={patient.id}
                        className="hover:bg-gray-50"
                      >
                        <td className="px-6 py-4 whitespace-nowrap">
                          <Link
                            href={`/patients/${patient.id}`}
                            className="text-blue-600 hover:text-blue-900 text-sm"
                          >
                            {patient.id.substring(0, 8)}...
                          </Link>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {patient.email}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {patient.age_group || 'Not specified'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {patient.location || 'Not specified'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="w-16 bg-gray-200 rounded-full h-2">
                              <div
                                className={`h-2 rounded-full ${
                                  patient.engagement_score < 0.3
                                    ? 'bg-red-600'
                                    : patient.engagement_score < 0.7
                                    ? 'bg-yellow-400'
                                    : 'bg-green-600'
                                }`}
                                style={{
                                  width: `${
                                    patient.engagement_score * 100
                                  }%`,
                                }}
                              ></div>
                            </div>
                            <span className="ml-2 text-xs text-gray-700">
                              {(
                                patient.engagement_score * 100
                              ).toFixed(0)}
                              %
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          <span
                            className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                              patient.has_active_consent
                                ? 'bg-green-100 text-green-800'
                                : 'bg-red-100 text-red-800'
                            }`}
                          >
                            {patient.has_active_consent
                              ? 'Active'
                              : 'Inactive'}
                          </span>
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td
                        colSpan={6}
                        className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center"
                      >
                        No patients found matching this segment's
                        criteria
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            {patients.length > 10 && (
              <div className="px-6 py-4 border-t border-gray-200">
                <Link
                  href={`/patients?segmentId=${segmentId}`}
                  className="text-blue-600 hover:underline text-sm"
                >
                  View all patients in this segment
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          {/* Segment Analysis */}
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Segment Analysis
              </h3>
            </div>
            <div className="px-6 py-5">
              {analysis ? (
                <dl className="space-y-6">
                  <div>
                    <dt className="text-sm font-medium text-gray-500">
                      Patient Count
                    </dt>
                    <dd className="mt-1 text-3xl font-semibold text-gray-900">
                      {analysis.patient_count || 0}
                    </dd>
                  </div>

                  {analysis.demographics && (
                    <div className="pt-4 border-t border-gray-200">
                      <dt className="text-sm font-medium text-gray-500 mb-2">
                        Demographics
                      </dt>
                      <dd className="space-y-3">
                        {analysis.demographics.age_distribution && (
                          <div>
                            <span className="block text-xs text-gray-500 mb-1">
                              Age Distribution
                            </span>
                            <div className="space-y-1">
                              {Object.entries(
                                analysis.demographics.age_distribution
                              ).map(
                                ([age, percentage]: [
                                  string,
                                  unknown
                                ]) => (
                                  <div
                                    key={age}
                                    className="flex items-center text-xs"
                                  >
                                    <span className="w-16">
                                      {age}
                                    </span>
                                    <div className="w-full bg-gray-200 rounded-full h-2 mx-2">
                                      <div
                                        className="bg-blue-600 h-2 rounded-full"
                                        style={{
                                          width: `${percentage}%`,
                                        }}
                                      ></div>
                                    </div>
                                    <span>{percentage}%</span>
                                  </div>
                                )
                              )}
                            </div>
                          </div>
                        )}

                        {analysis.demographics
                          .gender_distribution && (
                          <div>
                            <span className="block text-xs text-gray-500 mb-1">
                              Gender Distribution
                            </span>
                            <div className="space-y-1">
                              {Object.entries(
                                analysis.demographics
                                  .gender_distribution
                              ).map(
                                ([gender, percentage]: [
                                  string,
                                  unknown
                                ]) => (
                                  <div
                                    key={gender}
                                    className="flex items-center text-xs"
                                  >
                                    <span className="w-16">
                                      {gender}
                                    </span>
                                    <div className="w-full bg-gray-200 rounded-full h-2 mx-2">
                                      <div
                                        className="bg-purple-600 h-2 rounded-full"
                                        style={{
                                          width: `${percentage}%`,
                                        }}
                                      ></div>
                                    </div>
                                    <span>{percentage}%</span>
                                  </div>
                                )
                              )}
                            </div>
                          </div>
                        )}

                        {analysis.demographics
                          .location_distribution && (
                          <div>
                            <span className="block text-xs text-gray-500 mb-1">
                              Top Locations
                            </span>
                            <div className="space-y-1">
                              {Object.entries(
                                analysis.demographics
                                  .location_distribution
                              )
                                .slice(0, 3)
                                .map(
                                  ([location, percentage]: [
                                    string,
                                    unknown
                                  ]) => (
                                    <div
                                      key={location}
                                      className="flex items-center text-xs"
                                    >
                                      <span className="w-16 truncate">
                                        {location}
                                      </span>
                                      <div className="w-full bg-gray-200 rounded-full h-2 mx-2">
                                        <div
                                          className="bg-yellow-600 h-2 rounded-full"
                                          style={{
                                            width: `${percentage}%`,
                                          }}
                                        ></div>
                                      </div>
                                      <span>{percentage}%</span>
                                    </div>
                                  )
                                )}
                            </div>
                          </div>
                        )}
                      </dd>
                    </div>
                  )}

                  {analysis.engagement_metrics && (
                    <div className="pt-4 border-t border-gray-200">
                      <dt className="text-sm font-medium text-gray-500 mb-2">
                        Engagement
                      </dt>
                      <dd className="space-y-3">
                        <div>
                          <span className="block text-xs text-gray-500 mb-1">
                            Avg. Engagement Score
                          </span>
                          <div className="flex items-center">
                            <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2">
                              <div
                                className={`h-2.5 rounded-full ${
                                  analysis.engagement_metrics
                                    .average_engagement < 0.3
                                    ? 'bg-red-600'
                                    : analysis.engagement_metrics
                                        .average_engagement < 0.7
                                    ? 'bg-yellow-400'
                                    : 'bg-green-600'
                                }`}
                                style={{
                                  width: `${
                                    analysis.engagement_metrics
                                      .average_engagement * 100
                                  }%`,
                                }}
                              ></div>
                            </div>
                            <span className="text-sm font-medium">
                              {(
                                analysis.engagement_metrics
                                  .average_engagement * 100
                              ).toFixed(1)}
                              %
                            </span>
                          </div>
                        </div>

                        <div>
                          <span className="block text-xs text-gray-500 mb-1">
                            Response Rate
                          </span>
                          <span className="text-2xl font-medium">
                            {analysis.engagement_metrics.response_rate?.toFixed(
                              1
                            ) || 0}
                            %
                          </span>
                        </div>

                        {analysis.engagement_metrics
                          .preferred_channels && (
                          <div>
                            <span className="block text-xs text-gray-500 mb-1">
                              Preferred Channels
                            </span>
                            <div className="space-y-1">
                              {Object.entries(
                                analysis.engagement_metrics
                                  .preferred_channels
                              ).map(
                                ([channel, percentage]: [
                                  string,
                                  unknown
                                ]) => (
                                  <div
                                    key={channel}
                                    className="flex items-center text-xs"
                                  >
                                    <span className="w-16 capitalize">
                                      {channel.toLowerCase()}
                                    </span>
                                    <div className="w-full bg-gray-200 rounded-full h-2 mx-2">
                                      <div
                                        className={`h-2 rounded-full ${
                                          channel === 'EMAIL'
                                            ? 'bg-blue-600'
                                            : channel === 'SMS'
                                            ? 'bg-green-600'
                                            : 'bg-yellow-600'
                                        }`}
                                        style={{
                                          width: `${percentage}%`,
                                        }}
                                      ></div>
                                    </div>
                                    <span>{percentage}%</span>
                                  </div>
                                )
                              )}
                            </div>
                          </div>
                        )}
                      </dd>
                    </div>
                  )}
                </dl>
              ) : (
                <div className="text-center py-6">
                  <p className="text-gray-500 mb-4">
                    No analysis available for this segment
                  </p>
                  <form
                    action={`/api/segments/${segmentId}/analyze`}
                    method="POST"
                  >
                    <button
                      type="submit"
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
                    >
                      Analyze Segment
                    </button>
                  </form>
                </div>
              )}
            </div>
          </div>

          {/* Associated Campaigns */}
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">
                Associated Campaigns
              </h3>
            </div>
            <div className="px-6 py-5">
              {campaigns && campaigns.length > 0 ? (
                <ul className="divide-y divide-gray-200">
                  {campaigns.map((campaign) => (
                    <li key={campaign.id} className="py-3">
                      <Link
                        href={`/campaigns/${campaign.id}`}
                        className="flex justify-between items-center hover:bg-gray-50 p-2 rounded"
                      >
                        <div>
                          <p className="text-sm font-medium text-gray-900">
                            {campaign.title}
                          </p>
                          <div className="flex items-center mt-1">
                            <span
                              className={`px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                campaign.is_active
                                  ? 'bg-green-100 text-green-800'
                                  : 'bg-gray-100 text-gray-800'
                              }`}
                            >
                              {campaign.is_active
                                ? 'Active'
                                : 'Inactive'}
                            </span>
                            <span className="text-xs text-gray-500 ml-2">
                              {new Date(
                                campaign.start_date
                              ).toLocaleDateString()}{' '}
                              -{' '}
                              {new Date(
                                campaign.end_date
                              ).toLocaleDateString()}
                            </span>
                          </div>
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
                    No campaigns associated with this segment
                  </p>
                  <Link
                    href={`/campaigns/new?segmentId=${segmentId}`}
                    className="text-blue-600 text-sm hover:underline"
                  >
                    Create a campaign
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
