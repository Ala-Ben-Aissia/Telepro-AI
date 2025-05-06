import { getPatients } from '@/app/api/actions'
import Link from 'next/link'

export const dynamic = 'force-dynamic'
export const revalidate = 0

export default async function PatientsPage({
  searchParams,
}: {
  searchParams: Promise<{
    [key: string]: 'active' | 'inactive' | 'all'
  }>
}) {
  const params = await searchParams
  // Extract filter params from URL query string
  const filter = params.filter || ''

  // Prepare filters for API call
  // const apiFilters: Record<string, unknown> = {}

  // // Add more filters based on params
  // if (typeof params.age_group === 'string') {
  //   apiFilters.age_group = params.age_group
  // }

  // if (typeof params.gender === 'string') {
  //   apiFilters.gender = params.gender
  // }

  // if (typeof params.location === 'string') {
  //   apiFilters.location = params.location
  // }

  // if (typeof params.has_active_consent === 'string') {
  //   apiFilters.has_active_consent =
  //     params.has_active_consent === 'true'
  // }

  // Fetch patients with filters
  const patients = await getPatients(filter)

  return (
    <div className="space-y-8">
      <header className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">Patients</h1>
          <p className="text-gray-600">
            Manage and view patient information
          </p>
        </div>

        {/* Filter pills */}
        <div className="flex space-x-2">
          <Link
            href="/patients"
            className={`px-3 py-1 rounded-full text-sm ${
              !filter
                ? 'bg-blue-100 text-blue-800'
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            All
          </Link>
          <Link
            href="/patients?filter=active"
            className={`px-3 py-1 rounded-full text-sm ${
              filter === 'active'
                ? 'bg-green-100 text-green-800'
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            Active
          </Link>
          <Link
            href="/patients?filter=inactive"
            className={`px-3 py-1 rounded-full text-sm ${
              filter === 'inactive'
                ? 'bg-red-100 text-red-800'
                : 'bg-gray-100 text-gray-800'
            }`}
          >
            Inactive
          </Link>
        </div>
      </header>

      {/* Patients table */}
      <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Patient List
          </h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Showing {patients.length} patients
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
                  Gender
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
                  Contact Method
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
                  <tr key={patient.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Link
                        href={`/patients/${patient.id}`}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        {patient.id.substring(0, 8)}...
                      </Link>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {patient.email}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {patient.age_group || 'Unknown'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {patient.gender || 'Unknown'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {patient.location || 'Unknown'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          patient.preferred_contact_method === 'EMAIL'
                            ? 'bg-blue-100 text-blue-800'
                            : patient.preferred_contact_method ===
                              'SMS'
                            ? 'bg-green-100 text-green-800'
                            : patient.preferred_contact_method ===
                              'CALL'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {patient.preferred_contact_method}
                      </span>
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
                        <span className="ml-2 text-sm text-gray-700">
                          {(patient.engagement_score * 100).toFixed(
                            0
                          )}
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
                    colSpan={8}
                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center"
                  >
                    No patients found matching the criteria
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
