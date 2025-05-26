import {
  getPatient,
  getPatientCommunications,
  getPatientPreferences,
} from '@/app/api/actions'
import Link from 'next/link'

export const dynamic = 'force-dynamic'
export const revalidate = 0

export default async function PatientDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const patientId = (await params).id
  const patient = await getPatient(patientId)
  const communications = await getPatientCommunications(patientId)
  const { consents } = await getPatientPreferences(patientId)

  if (!patient) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh]">
        <h1 className="text-2xl font-bold mb-4">Patient Not Found</h1>
        <p className="text-gray-600 mb-4">
          The patient with ID {patientId} could not be found.
        </p>
        <Link
          href="/patients"
          className="text-blue-600 hover:underline"
        >
          Return to Patient List
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <header className="flex justify-between items-center">
        <div className="flex items-center gap-4">
          <Link
            href="/patients"
            className="text-blue-600 hover:underline"
          >
            &larr; Back to Patients
          </Link>
          <h1 className="text-2xl font-bold">Patient Details</h1>
        </div>
      </header>

      {/* Patient overview card */}
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Patient Information
          </h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Personal details and communication preferences.
          </p>
        </div>
        <div className="border-t border-gray-200">
          <dl>
            <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">
                Patient ID
              </dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {patient.id}
              </dd>
            </div>
            <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">
                Email
              </dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {patient.email}
                {patient.email_verified && (
                  <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Verified
                  </span>
                )}
              </dd>
            </div>
            <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">
                Phone
              </dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {patient.phone_number || 'Not provided'}
                {patient.phone_number && patient.phone_verified && (
                  <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Verified
                  </span>
                )}
              </dd>
            </div>
            <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">
                Demographics
              </dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <span className="block text-xs text-gray-500">
                      Gender
                    </span>
                    <span>{patient.gender || 'Not specified'}</span>
                  </div>
                  <div>
                    <span className="block text-xs text-gray-500">
                      Age Group
                    </span>
                    <span>
                      {patient.age_group || 'Not specified'}
                    </span>
                  </div>
                  <div>
                    <span className="block text-xs text-gray-500">
                      Language
                    </span>
                    <span>
                      {patient.language_preference || 'Not specified'}
                    </span>
                  </div>
                </div>
              </dd>
            </div>
            <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">
                Location
              </dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                {patient.location || 'Not specified'}
                {patient.postal_code && ` (${patient.postal_code})`}
              </dd>
            </div>
            <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">
                Contact Preferences
              </dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <span
                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    patient.preferred_contact_methods === 'EMAIL'
                      ? 'bg-blue-100 text-blue-800'
                      : patient.preferred_contact_methods === 'SMS'
                      ? 'bg-green-100 text-green-800'
                      : patient.preferred_contact_methods === 'CALL'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {patient.preferred_contact_methods}
                </span>

                {patient.contact_time_preferences &&
                  Object.keys(patient.contact_time_preferences)
                    .length > 0 && (
                    <div className="mt-2">
                      <span className="block text-xs text-gray-500 mb-1">
                        Preferred Contact Times
                      </span>
                      <div className="text-sm">
                        {JSON.stringify(
                          patient.contact_time_preferences
                        )}
                      </div>
                    </div>
                  )}
              </dd>
            </div>
            <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
              <dt className="text-sm font-medium text-gray-500">
                Engagement
              </dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                <div className="flex items-center">
                  <div className="w-32 bg-gray-200 rounded-full h-2.5">
                    <div
                      className={`h-2.5 rounded-full ${
                        patient.engagement_score < 0.3
                          ? 'bg-red-600'
                          : patient.engagement_score < 0.7
                          ? 'bg-yellow-400'
                          : 'bg-green-600'
                      }`}
                      style={{
                        width: `${patient.engagement_score * 100}%`,
                      }}
                    ></div>
                  </div>
                  <span className="ml-2 text-sm font-medium text-gray-700">
                    {(patient.engagement_score * 100).toFixed(1)}%
                  </span>
                </div>

                <div className="mt-2">
                  <span className="block text-xs text-gray-500 mb-1">
                    Last Response
                  </span>
                  <span>
                    {patient.last_campaign_response
                      ? new Date(
                          patient.last_campaign_response
                        ).toLocaleDateString()
                      : 'Never'}
                  </span>
                </div>
              </dd>
            </div>
          </dl>
        </div>
      </div>

      {/* Consent Records */}
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Consent Records
          </h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Patient&apos;s consent for different types of data
            processing and communications
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
                  Type
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Status
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Granted On
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Method
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {consents && consents.length > 0 ? (
                consents.map((consent) => (
                  <tr key={consent.pk}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {consent.consent_type.replace('_', ' ')}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          consent.granted
                            ? 'bg-green-100 text-green-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {consent.granted ? 'Granted' : 'Denied'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {new Date(
                        consent.timestamp
                      ).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {consent.consent_method.replace('_', ' ')}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan={4}
                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center"
                  >
                    No consent records found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Communication History */}
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 className="text-lg leading-6 font-medium text-gray-900">
            Communication History
          </h3>
          <p className="mt-1 max-w-2xl text-sm text-gray-500">
            Recent communications with the patient
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
                  Campaign
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Channel
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Status
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Sent
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Response
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {communications && communications.length > 0 ? (
                communications.map((comm) => (
                  <tr key={comm.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {comm.campaign || 'Unknown Campaign'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          comm.communication_type === 'EMAIL'
                            ? 'bg-blue-100 text-blue-800'
                            : comm.communication_type === 'SMS'
                            ? 'bg-green-100 text-green-800'
                            : comm.communication_type === 'CALL'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {comm.communication_type}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          comm.status === 'DELIVERED' ||
                          comm.status === 'READ' ||
                          comm.status === 'RESPONDED'
                            ? 'bg-green-100 text-green-800'
                            : comm.status === 'FAILED'
                            ? 'bg-red-100 text-red-800'
                            : 'bg-yellow-100 text-yellow-800'
                        }`}
                      >
                        {comm.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {comm.sent_at
                        ? new Date(comm.sent_at).toLocaleDateString()
                        : 'Not sent'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {comm.response ? (
                        <span className="text-green-600 font-medium">
                          {comm.response}
                        </span>
                      ) : (
                        <span className="text-gray-400">–</span>
                      )}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan={5}
                    className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center"
                  >
                    No communication history found
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
