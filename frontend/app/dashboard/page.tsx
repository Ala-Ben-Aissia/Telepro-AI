'use client'

import React, { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { AppLayout } from '@/components/layout/AppLayout'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Loading } from '@/components/ui/Loading'
import { AuthService } from '@/lib/auth'
import { ApiClient } from '@/lib/api'
import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import { PatientProfile, CommunicationLog } from '@/types'

export default function DashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState(AuthService.getCurrentUser())
  const [patientProfile, setPatientProfile] =
    useState<PatientProfile | null>(null)
  console.log({ 9999999999999: patientProfile })
  const [recentCommunications, setRecentCommunications] = useState<
    CommunicationLog[]
  >([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // State for expanded communications
  const [expandedCommunications, setExpandedCommunications] =
    useState(false)

  // Number of communications to show in collapsed view
  const communicationsToShow = expandedCommunications
    ? recentCommunications.length
    : 3

  useEffect(() => {
    // Set user from localStorage
    const currentUser = AuthService.getCurrentUser()
    setUser(currentUser)
    console.log('Current user:', currentUser)

    // Fetch patient profile and recent communications
    const fetchData = async () => {
      setIsLoading(true)
      setError(null)

      try {
        // This is a placeholder - in a real app, you would fetch actual data
        // from your API endpoints
        const profileData = await ApiClient.get<{
          results: PatientProfile[]
        }>('/patients/')
        console.log({ profileData })
        if (
          profileData &&
          profileData &&
          profileData.results.length > 0
        ) {
          setPatientProfile(profileData.results[0])
        }

        // Fetch recent communications
        const commsData = await ApiClient.get<CommunicationLog[]>(
          `/patients/${user?.patient_uuid}/communications/`
        )
        console.log({ commsData })
        if (commsData) {
          setRecentCommunications(commsData)
        }
      } catch (err) {
        console.error('Error fetching data:', err)
        setError(
          'Failed to load dashboard data. Please try again later.'
        )
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [router, user?.patient_uuid])

  if (isLoading) {
    return (
      <ProtectedRoute allowedUserTypes={['PATIENT']}>
        <AppLayout userType={user?.user_type}>
          <div className="flex justify-center items-center h-64">
            <Loading text="Loading dashboard..." />
          </div>
        </AppLayout>
      </ProtectedRoute>
    )
  }

  return (
    <ProtectedRoute allowedUserTypes={['PATIENT']}>
      <AppLayout userType={user?.user_type}>
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">
              Patient Dashboard
            </h1>
            <Button
              variant="outline"
              onClick={() => {
                AuthService.logout()
                router.push('/')
              }}
            >
              Logout
            </Button>
          </div>

          {error && (
            <div className="bg-red-50 text-red-500 p-4 rounded-md">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Your Profile</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <p className="text-sm font-medium text-gray-500">
                      Username
                    </p>
                    <p className="mt-1">{user?.username}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">
                      Email
                    </p>
                    <p className="mt-1">{user?.email}</p>
                    {patientProfile &&
                      patientProfile.email_verified === false && (
                        <p className="text-xs text-amber-600 mt-1">
                          Not verified. Please verify your email.
                        </p>
                      )}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">
                      Contact Preference
                    </p>
                    <p className="mt-1">
                      {patientProfile
                        ? patientProfile.preferred_contact_method ||
                          'Not set'
                        : 'Not set'}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">
                      Consent Status
                    </p>
                    <p className="mt-1">
                      {patientProfile &&
                      patientProfile.has_active_consent
                        ? 'Active consent provided'
                        : 'No active consent'}
                    </p>
                  </div>
                  <Button
                    variant="outline"
                    onClick={() => router.push('/profile')}
                  >
                    Update Profile
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Recent Communications</CardTitle>
              </CardHeader>
              <CardContent>
                {recentCommunications.length === 0 ? (
                  <p className="text-gray-500">
                    No recent communications.
                  </p>
                ) : (
                  <div className="space-y-4">
                    {recentCommunications
                      .slice(0, communicationsToShow)
                      .map((comm) => (
                        <div
                          key={comm.id}
                          className="p-3 border border-gray-100 rounded-md"
                        >
                          <div className="flex justify-between">
                            <p className="font-medium">
                              {typeof comm.campaign === 'string'
                                ? comm.campaign
                                : (comm.campaign as any).title ||
                                  'Campaign'}
                            </p>
                            <span
                              className={`text-xs px-2 py-1 rounded-full ${
                                comm.status === 'SENT'
                                  ? 'bg-blue-100 text-blue-800'
                                  : comm.status === 'DELIVERED'
                                  ? 'bg-green-100 text-green-800'
                                  : 'bg-gray-100 text-gray-800'
                              }`}
                            >
                              {comm.status}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 mt-1">
                            {comm.message}
                          </p>
                          <p className="text-xs text-gray-500 mt-2">
                            {new Date(
                              comm.sent_at || ''
                            ).toLocaleDateString()}{' '}
                            via {comm.communication_type}
                          </p>
                        </div>
                      ))}

                    <div className="flex justify-between items-center">
                      {recentCommunications.length > 3 && (
                        <Button
                          variant="link"
                          onClick={() =>
                            setExpandedCommunications(
                              !expandedCommunications
                            )
                          }
                        >
                          {expandedCommunications
                            ? 'Show Less'
                            : 'View More'}
                        </Button>
                      )}

                      <Button
                        variant="link"
                        onClick={() => router.push('/communications')}
                      >
                        Go to Communications
                      </Button>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </AppLayout>
    </ProtectedRoute>
  )
}
