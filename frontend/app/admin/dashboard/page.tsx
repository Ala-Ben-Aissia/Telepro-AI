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
import {
  DashboardStats,
  RecentCampaign,
  AnalyticsResponse,
} from '@/types'
import {
  BarChart3,
  Users,
  MessageCircle,
  Settings,
  FileText,
  CheckCircle2,
} from 'lucide-react'

export default function AdminDashboardPage() {
  const router = useRouter()
  const [user, setUser] = useState(AuthService.getCurrentUser())
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [recentCampaigns, setRecentCampaigns] = useState<
    RecentCampaign[]
  >([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // State for expanded sections
  const [expandedCampaigns, setExpandedCampaigns] = useState(false)
  const [expandedActions, setExpandedActions] = useState(false)

  // Number of items to show in collapsed view
  const campaignsToShow = expandedCampaigns
    ? recentCampaigns.length
    : 3

  useEffect(() => {
    // Set user from localStorage
    setUser(AuthService.getCurrentUser())

    // Fetch dashboard data
    const fetchData = async () => {
      setIsLoading(true)
      setError(null)

      try {
        // Fetch analytics data from API
        const analyticsData = await ApiClient.get<AnalyticsResponse>(
          '/campaigns/analytics/dashboard'
        )

        // Extract stats from the analytics data
        const statsData: DashboardStats = {
          totalPatients:
            analyticsData.engagement_overview.total_patients,
          activeCampaigns:
            analyticsData.campaign_performance.campaigns.filter(
              (c) => c.is_active
            ).length,
          communicationsSent:
            analyticsData.campaign_performance.overall_metrics
              .total_communications,
          responseRate:
            analyticsData.campaign_performance.overall_metrics
              .overall_response_rate * 100,
          readRate:
            analyticsData.campaign_performance.overall_metrics
              .overall_read_rate * 100,
          avgResponseTimeHours:
            analyticsData.engagement_overview.avg_response_time_hours,
        }
        setStats(statsData)

        // Convert campaign performance data to RecentCampaign format
        const campaignsData: RecentCampaign[] =
          analyticsData.campaign_performance.campaigns.map(
            (campaign) => ({
              id: campaign.campaign_id.toString(),
              title: campaign.title,
              start_date: campaign.start_date,
              end_date: campaign.end_date,
              is_active: campaign.is_active,
              target_count: campaign.total_communications,
              sent_count: campaign.total_communications,
              response_count: Math.round(
                campaign.total_communications * campaign.response_rate
              ),
            })
          )
        setRecentCampaigns(campaignsData)
      } catch (err) {
        console.error('Error fetching admin dashboard data:', err)
        setError(
          'Failed to load dashboard data. Please try again later.'
        )
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, [router])

  if (isLoading) {
    return (
      <ProtectedRoute allowedUserTypes={['STAFF']}>
        <AppLayout userType={user?.user_type}>
          <div className="flex justify-center items-center h-64">
            <Loading text="Loading admin dashboard..." />
          </div>
        </AppLayout>
      </ProtectedRoute>
    )
  }

  return (
    <ProtectedRoute allowedUserTypes={['STAFF']}>
      <AppLayout userType={user?.user_type}>
        <div className="space-y-10">
          <div className="flex justify-between items-center mb-2">
            <h1 className="text-3xl font-extrabold text-gray-900 tracking-tight flex items-center gap-2">
              <BarChart3 className="h-7 w-7 text-primary-700" /> Admin
              Dashboard
            </h1>
            <Button
              variant="outline"
              onClick={() => {
                AuthService.logout()
                router.push('/')
              }}
              className="font-semibold"
            >
              Logout
            </Button>
          </div>

          {error && (
            <div className="bg-red-50 text-red-500 p-4 rounded-md font-semibold">
              {error}
            </div>
          )}

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
            <Card className="rounded-2xl shadow-md border border-gray-100 flex flex-col items-center text-center p-6">
              <Users className="h-8 w-8 text-primary-700 mb-2" />
              <CardContent className="pt-2">
                <p className="text-sm font-medium text-gray-500">
                  Total Patients
                </p>
                <p className="mt-2 text-3xl font-extrabold text-primary-700">
                  {stats?.totalPatients.toLocaleString()}
                </p>
              </CardContent>
            </Card>
            <Card className="rounded-2xl shadow-md border border-gray-100 flex flex-col items-center text-center p-6">
              <MessageCircle className="h-8 w-8 text-secondary-700 mb-2" />
              <CardContent className="pt-2">
                <p className="text-sm font-medium text-gray-500">
                  Active Campaigns
                </p>
                <p className="mt-2 text-3xl font-extrabold text-primary-700">
                  {stats?.activeCampaigns}
                </p>
              </CardContent>
            </Card>
            <Card className="rounded-2xl shadow-md border border-gray-100 flex flex-col items-center text-center p-6">
              <FileText className="h-8 w-8 text-accent-700 mb-2" />
              <CardContent className="pt-2">
                <p className="text-sm font-medium text-gray-500">
                  Communications Sent
                </p>
                <p className="mt-2 text-3xl font-extrabold text-primary-700">
                  {stats?.communicationsSent.toLocaleString()}
                </p>
              </CardContent>
            </Card>
            <Card className="rounded-2xl shadow-md border border-gray-100 flex flex-col items-center text-center p-6">
              <CheckCircle2 className="h-8 w-8 text-green-700 mb-2" />
              <CardContent className="pt-2">
                <p className="text-sm font-medium text-gray-500">
                  Response Rate
                </p>
                <p className="mt-2 text-3xl font-extrabold text-primary-700">
                  {stats?.responseRate.toFixed(1)}%
                </p>
              </CardContent>
            </Card>
            <Card className="rounded-2xl shadow-md border border-gray-100 flex flex-col items-center text-center p-6">
              <BarChart3 className="h-8 w-8 text-accent-700 mb-2" />
              <CardContent className="pt-2">
                <p className="text-sm font-medium text-gray-500">
                  Read Rate
                </p>
                <p className="mt-2 text-3xl font-extrabold text-primary-700">
                  {stats?.readRate ? stats.readRate.toFixed(1) : 0}%
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Recent Campaigns */}
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle>Recent Campaigns</CardTitle>
                <Button
                  variant="outline"
                  onClick={() => router.push('/admin/campaigns')}
                >
                  Go to Campaigns
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full text-sm text-left">
                  <thead className="text-xs text-gray-700 uppercase bg-gray-50">
                    <tr>
                      <th className="px-6 py-3">Campaign</th>
                      <th className="px-6 py-3">Status</th>
                      <th className="px-6 py-3">Period</th>
                      <th className="px-6 py-3">Target</th>
                      <th className="px-6 py-3">Sent</th>
                      <th className="px-6 py-3">Response Rate</th>
                      <th className="px-6 py-3">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recentCampaigns
                      .slice(0, campaignsToShow)
                      .map((campaign) => (
                        <tr
                          key={campaign.id}
                          className="bg-white border-b"
                        >
                          <td className="px-6 py-4 font-medium text-gray-900">
                            {campaign.title.length > 50
                              ? campaign.title.slice(0, 50) + '...'
                              : campaign.title}
                          </td>
                          <td className="px-6 py-4">
                            <span
                              className={`px-2 py-1 text-xs rounded-full ${
                                campaign.is_active
                                  ? 'bg-green-100 text-green-800'
                                  : 'bg-gray-100 text-gray-800'
                              }`}
                            >
                              {campaign.is_active
                                ? 'Active'
                                : 'Completed'}
                            </span>
                          </td>
                          <td className="px-6 py-4">
                            {new Date(
                              campaign.start_date || ''
                            ).toLocaleDateString()}{' '}
                            -{' '}
                            {new Date(
                              campaign.end_date || ''
                            ).toLocaleDateString()}
                          </td>
                          <td className="px-6 py-4">
                            {campaign.target_count}
                          </td>
                          <td className="px-6 py-4">
                            {campaign.sent_count}
                          </td>
                          <td className="px-6 py-4">
                            {Math.round(
                              (campaign.response_count /
                                campaign.target_count) *
                                100
                            )}
                            %
                          </td>
                          <td className="px-6 py-4">
                            <Button
                              variant="link"
                              onClick={() =>
                                router.push(
                                  `/admin/campaigns/${campaign.id}`
                                )
                              }
                            >
                              Details
                            </Button>
                          </td>
                        </tr>
                      ))}
                  </tbody>
                </table>

                {recentCampaigns.length > 3 && (
                  <div className="mt-4 text-center">
                    <Button
                      variant="link"
                      onClick={() =>
                        setExpandedCampaigns(!expandedCampaigns)
                      }
                    >
                      {expandedCampaigns
                        ? 'Show Less'
                        : 'View All Campaigns'}
                    </Button>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle>Quick Actions</CardTitle>
                <Button
                  variant="link"
                  onClick={() => setExpandedActions(!expandedActions)}
                >
                  {expandedActions ? 'Show Less' : 'View All'}
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div
                className={`grid grid-cols-1 md:grid-cols-3 gap-6 ${
                  expandedActions
                    ? 'max-h-none'
                    : 'max-h-[300px] overflow-hidden'
                } transition-all duration-300`}
              >
                <div className="p-4 border border-gray-100 rounded-lg">
                  <div className="text-center space-y-4">
                    <div className="mx-auto w-12 h-12 flex items-center justify-center rounded-full bg-primary-100">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-6 w-6 text-primary-700"
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
                    </div>
                    <h3 className="text-lg font-medium">
                      New Campaign
                    </h3>
                    <p className="text-sm text-gray-500">
                      Create a new campaign to reach out to patients
                    </p>
                    <Button
                      variant="outline"
                      onClick={() =>
                        router.push('/admin/campaigns/new')
                      }
                    >
                      Create Campaign
                    </Button>
                  </div>
                </div>

                <div className="p-4 border border-gray-100 rounded-lg">
                  <div className="text-center space-y-4">
                    <div className="mx-auto w-12 h-12 flex items-center justify-center rounded-full bg-secondary-100">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-6 w-6 text-secondary-700"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                        />
                      </svg>
                    </div>
                    <h3 className="text-lg font-medium">
                      Patient Segments
                    </h3>
                    <p className="text-sm text-gray-500">
                      Manage patient segments for targeted campaigns
                    </p>
                    <Button
                      variant="outline"
                      onClick={() => router.push('/admin/segments')}
                    >
                      Manage Segments
                    </Button>
                  </div>
                </div>

                <div className="p-4 border border-gray-100 rounded-lg">
                  <div className="text-center space-y-4">
                    <div className="mx-auto w-12 h-12 flex items-center justify-center rounded-full bg-accent-100">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="h-6 w-6 text-accent-600"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                        />
                      </svg>
                    </div>
                    <h3 className="text-lg font-medium">Analytics</h3>
                    <p className="text-sm text-gray-500">
                      View detailed analytics and campaign performance
                    </p>
                    <Button
                      variant="outline"
                      onClick={() => router.push('/admin/analytics')}
                    >
                      View Analytics
                    </Button>
                  </div>
                </div>

                {expandedActions && (
                  <>
                    <div className="p-4 border border-gray-100 rounded-lg">
                      <div className="text-center space-y-4">
                        <div className="mx-auto w-12 h-12 flex items-center justify-center rounded-full bg-green-100">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="h-6 w-6 text-green-700"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                            />
                          </svg>
                        </div>
                        <h3 className="text-lg font-medium">
                          Templates
                        </h3>
                        <p className="text-sm text-gray-500">
                          Manage communication templates
                        </p>
                        <Button
                          variant="outline"
                          onClick={() =>
                            router.push('/admin/templates')
                          }
                        >
                          Manage Templates
                        </Button>
                      </div>
                    </div>

                    <div className="p-4 border border-gray-100 rounded-lg">
                      <div className="text-center space-y-4">
                        <div className="mx-auto w-12 h-12 flex items-center justify-center rounded-full bg-purple-100">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            className="h-6 w-6 text-purple-700"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
                            />
                          </svg>
                        </div>
                        <h3 className="text-lg font-medium">
                          Settings
                        </h3>
                        <p className="text-sm text-gray-500">
                          Configure system settings
                        </p>
                        <Button
                          variant="outline"
                          onClick={() =>
                            router.push('/admin/settings')
                          }
                        >
                          System Settings
                        </Button>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </AppLayout>
    </ProtectedRoute>
  )
}
