import { Button } from '@/components/button'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/card'
import Link from 'next/link'
import { Suspense } from 'react'
import ConsentForm from '@/components/ConsentForm'
import {
  getCampaign,
  getCurrentUser,
  getPatientConsents,
  getPatientPreferences,
  logout,
} from '../api/actions'
import {
  ShieldCheck,
  UserCircle,
  Calendar,
  Eye,
  Bell,
  CheckCircle2,
  AlertTriangle,
  LogOutIcon,
} from 'lucide-react'

export default async function PatientPage() {
  const patient = await getCurrentUser()
  console.log({ patient })
  if (!patient) return
  const preferences = await getPatientPreferences(patient.id)

  const consents = await getPatientConsents(patient.id)

  const campaigns = preferences?.campaign_preferences.map(
    async (campaignId) => {
      const campaign = await getCampaign(campaignId)
      return campaign
    },
  )

  return (
    <div className="relative">
      {/* Decorative Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none -z-10">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-100 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div
          className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-100 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"
          style={{ animationDelay: '2s' }}
        />
      </div>

      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8 relative">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <aside className="lg:col-span-1">
            <Card className="sticky top-24 border border-blue-100 shadow-md overflow-hidden">
              <CardHeader className="pb-3">
                <CardTitle className="text-xl text-blue-900 flex items-center gap-2">
                  <UserCircle className="h-5 w-5 text-blue-600" />
                  Your Profile
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 pt-0">
                <div className="p-4 rounded-lg bg-blue-50 border border-blue-100">
                  <p className="text-gray-700 text-sm">
                    Manage your health preferences securely and
                    easily.
                  </p>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <Calendar className="h-4 w-4 text-indigo-500" />
                    <span>
                      Last updated:{' '}
                      {consents &&
                        new Date(
                          consents[0]?.timestamp || Date.now(),
                        ).toLocaleDateString('en-US', {
                          day: 'numeric',
                          month: 'long',
                          year: 'numeric',
                        })}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 text-sm">
                    {patient?.has_active_consent ? (
                      <CheckCircle2 className="h-4 w-4 text-green-500" />
                    ) : (
                      <AlertTriangle className="h-4 w-4 text-amber-500" />
                    )}
                    <span
                      className={
                        patient?.has_active_consent
                          ? 'text-green-700'
                          : 'text-amber-700'
                      }
                    >
                      Status:{' '}
                      {patient?.has_active_consent
                        ? 'Active'
                        : 'Consent Required'}
                    </span>
                  </div>
                </div>

                <Button
                  variant="outline"
                  className="w-full border-blue-600 text-blue-600 hover:bg-blue-50 transition-colors"
                >
                  Update Profile
                </Button>
              </CardContent>
              <div className=" bottom-0 w-full p-4 border-t border-gray-200">
                <button
                  className={`flex items-center p-2 w-full text-gray-700 hover:bg-gray-100 rounded-md`}
                  onClick={logout}
                >
                  <span className="mr-3 flex gap-2 items-center">
                    Logout <LogOutIcon />
                  </span>
                </button>
              </div>
            </Card>
          </aside>

          {/* Main Content */}
          <main className="lg:col-span-3 space-y-8">
            {/* Consent Dashboard */}
            <section>
              <Card className="border border-blue-100 shadow-md overflow-hidden">
                <CardHeader className="pb-3">
                  <CardTitle className="text-xl text-blue-900 flex items-center gap-2">
                    <ShieldCheck className="h-5 w-5 text-blue-600" />
                    Your Consent Management
                  </CardTitle>
                </CardHeader>
                <CardContent className="pt-0">
                  <p className="text-gray-600 mb-6">
                    Control your communication preferences and
                    campaign settings with complete transparency.
                  </p>
                  <Suspense
                    fallback={
                      <div className="flex items-center justify-center py-10">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                        <span className="ml-3 text-gray-600">
                          Loading your preferences...
                        </span>
                      </div>
                    }
                  >
                    <ConsentForm
                      consents={consents}
                      preferences={preferences || {}}
                    />
                  </Suspense>
                </CardContent>
              </Card>
            </section>

            {/* Campaigns Section */}
            <section>
              <div className="flex items-center gap-2 mb-4">
                <Calendar className="h-5 w-5 text-indigo-600" />
                <h2 className="text-2xl font-bold text-blue-900">
                  Health Campaigns
                </h2>
              </div>

              <div className="grid md:grid-cols-2 gap-5">
                {campaigns?.map(async (campaign) => {
                  const camp = await campaign
                  if (!camp) return null

                  return (
                    <Card
                      key={camp.id}
                      className="group border border-blue-100 shadow-md hover:shadow-lg transition-all duration-300 overflow-hidden"
                    >
                      <CardContent className="p-6">
                        <div className="mb-4">
                          <div className="inline-flex p-2 bg-blue-50 rounded-lg border border-blue-100">
                            <Eye className="h-5 w-5 text-indigo-600" />
                          </div>
                        </div>
                        <h3 className="text-lg font-semibold text-blue-900 mb-2 group-hover:text-indigo-700 transition-colors">
                          {camp.title}
                        </h3>
                        <p className="text-gray-600 mb-4 text-sm">
                          {camp.description}
                        </p>
                        <div className="flex gap-3 mt-4">
                          <Link href="/patient/campaigns/vaccination">
                            <Button className="bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm">
                              Explore
                            </Button>
                          </Link>
                          <Link href="/patient/campaigns/vaccination/consent">
                            <Button
                              variant="outline"
                              className="border-blue-600 text-blue-600 hover:bg-blue-50"
                            >
                              Consent
                            </Button>
                          </Link>
                        </div>
                      </CardContent>
                    </Card>
                  )
                })}

                {/* Empty State if no campaigns */}
                {(!campaigns || campaigns.length === 0) && (
                  <div className="col-span-2 p-8 text-center rounded-lg border border-blue-100 bg-blue-50">
                    <Bell className="h-10 w-10 text-blue-400 mx-auto mb-3" />
                    <h3 className="text-lg font-medium text-blue-900 mb-2">
                      No Active Campaigns
                    </h3>
                    <p className="text-gray-600 mb-4">
                      You don&apos;t have any active health campaigns
                      at the moment.
                    </p>
                  </div>
                )}
              </div>
            </section>

            {/* Communication Preferences Preview
            <section className="mt-8">
              <div className="flex items-center gap-2 mb-4">
                <Globe className="h-5 w-5 text-indigo-600" />
                <h2 className="text-2xl font-bold text-blue-900">
                  Communication Preferences
                </h2>
              </div>

              <Card className="border border-blue-100 shadow-md overflow-hidden">
                <CardContent className="p-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <h3 className="text-md font-semibold text-blue-900 flex items-center gap-2">
                        <Bell className="h-4 w-4 text-indigo-500" />
                        Notification Settings
                      </h3>
                      <div className="space-y-2">
                        <div className="flex items-center justify-between p-3 rounded-md bg-blue-50 border border-blue-100">
                          <span className="text-gray-700 text-sm">
                            Appointment Reminders
                          </span>
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Enabled
                          </span>
                        </div>
                        <div className="flex items-center justify-between p-3 rounded-md bg-blue-50 border border-blue-100">
                          <span className="text-gray-700 text-sm">
                            Test Results
                          </span>
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                            Enabled
                          </span>
                        </div>
                        <div className="flex items-center justify-between p-3 rounded-md bg-blue-50 border border-blue-100">
                          <span className="text-gray-700 text-sm">
                            Newsletters
                          </span>
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                            Disabled
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-4">
                      <h3 className="text-md font-semibold text-blue-900 flex items-center gap-2">
                        <Globe className="h-4 w-4 text-indigo-500" />
                        Contact Preferences
                      </h3>
                      <div className="space-y-2">
                        <div className="flex items-center justify-between p-3 rounded-md bg-blue-50 border border-blue-100">
                          <span className="text-gray-700 text-sm">
                            Preferred Language
                          </span>
                          <span className="text-sm text-blue-700">
                            English
                          </span>
                        </div>
                        <div className="flex items-center justify-between p-3 rounded-md bg-blue-50 border border-blue-100">
                          <span className="text-gray-700 text-sm">
                            Contact Method
                          </span>
                          <span className="text-sm text-blue-700">
                            Email
                          </span>
                        </div>
                      </div>

                      <div className="mt-4">
                        <Link href="/patient/preferences">
                          <Button
                            variant="outline"
                            className="w-full border-indigo-600 text-indigo-600 hover:bg-indigo-50"
                          >
                            Manage Preferences
                          </Button>
                        </Link>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </section> */}
          </main>
        </div>
      </div>
    </div>
  )
}
