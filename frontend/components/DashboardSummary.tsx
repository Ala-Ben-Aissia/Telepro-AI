'use client'

import Link from 'next/link'
import { useEffect, useState } from 'react'

interface Campaign {
  campaign_id: number
  title: string
  category: string
  start_date: string
  end_date: string
  is_active: boolean
  total_communications: number
  response_rate: number
  read_rate: number
  avg_response_time_hours: number
  segments: []
}

type Channel = 'EMAIL' | 'SMS' | 'CALL' | 'NONE'

interface ChannelMetric {
  total: number
  responded: number
  read: number
  response_rate: number
  read_rate: number
  avg_response_time_hours: number
}

type ChannelMetrics = Record<Channel, ChannelMetric>

type TimePeriod = 'morning' | 'afternoon' | 'evening' | 'night'

interface TimeMetric {
  total: number
  responded: number
  read: number
  response_rate: number
  read_rate: number
  avg_response_time_hours: number
}

type TimeMetrics = Record<TimePeriod, TimeMetric>

export interface AnalyticsData {
  engagement_overview: {
    total_patients: number
    active_patients: number
    active_percentage: number
    high_engagement_patients: number
    high_engagement_percentage: number
    low_engagement_patients: number
    low_engagement_percentage: number
    total_communications: number
    response_rate: number
    read_rate: number
    avg_response_time_hours: number
    period_days: number
  }
  campaign_performance: {
    campaigns: Campaign[]
    overall_metrics: {
      total_campaigns: number
      total_communications: number
      overall_response_rate: number
      overall_read_rate: number
    }
    period_days: number
  }
  communication_channels: {
    channel_metrics: ChannelMetrics
    best_response_channel: Channel | null
    fastest_response_channel: Channel | null
    period_days: number
  }
  time_of_day: {
    time_metrics: TimeMetrics
  }
  // patientMetrics: {
  //   total_patients: number;
  //   active_patients: number;
  //   inactive_patients: number;
  //   average_engagement: number;
  // };
  // campaignMetrics: {
  //   active_campaigns: number;
  //   total_sent: number;
  //   delivered_rate: number;
  //   response_rate: number;
  // };
  // recentCampaigns: {
  //   id: number;
  //   title: string;
  //   is_active: boolean;
  //   start_date: string;
  //   end_date: string;
  //   response_rate: number;
  // }[];
}

export default function DashboardSummary() {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(
    null
  )
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/analytics/dashboard`
        )
        if (!response.ok)
          throw new Error('Failed to fetch dashboard data')
        const data = await response.json()

        setAnalytics({
          engagement_overview: data.engagement_overview || {},
          campaign_performance: data.campaign_performance || {},
          communication_channels: data.communication_channels || {},
          time_of_day: data.time_of_day || {},
        })
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchDashboardData()
  }, [])

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-pulse text-center">
          <div className="h-12 w-12 mx-auto mb-4 rounded-full bg-blue-200"></div>
          <div className="h-4 w-32 mx-auto rounded bg-blue-200"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Patients"
          value={analytics?.engagement_overview?.total_patients || 0}
          description="Registered patients"
          trend="up"
          link="/patients"
        />
        <StatCard
          title="Active Campaigns"
          value={
            analytics?.campaign_performance?.campaigns.filter(
              (c) => c.is_active
            ).length || 0
          }
          description="Running campaigns"
          trend="none"
          link="/campaigns?status=active"
        />
        <StatCard
          title="Response Rate"
          value={`${(
            (analytics?.campaign_performance?.overall_metrics
              ?.overall_response_rate || 0) * 100
          ).toFixed(1)}%`}
          description="Average across campaigns"
          trend={
            (analytics?.campaign_performance?.overall_metrics
              .overall_response_rate || 0) *
              100 >
            50
              ? 'up'
              : 'down'
          }
          link="/campaigns"
        />
        <StatCard
          title="Inactive Patients"
          value={
            analytics?.engagement_overview?.low_engagement_patients ||
            0
          }
          description="No response in 90+ days"
          trend="down"
          link="/patients?filter=inactive"
        />
      </div>

      {/* Recent Campaigns */}
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-5 border-b border-gray-200 flex justify-between items-center">
          <div>
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Recent Campaigns
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              Overview of your latest campaigns
            </p>
          </div>
          <Link
            href="/campaigns"
            className="text-sm font-medium text-blue-600 hover:text-blue-500"
          >
            View all
          </Link>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr key={Math.random()}>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Campaign Name
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
                  Timeline
                </th>
                <th
                  scope="col"
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Response Rate
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {analytics?.campaign_performance?.campaigns &&
              analytics.campaign_performance.campaigns.length > 0 ? (
                analytics.campaign_performance.campaigns.map(
                  (campaign) => (
                    <tr
                      key={campaign.campaign_id}
                      className="hover:bg-gray-50"
                    >
                      <td className="px-6 py-4 whitespace-nowrap">
                        <Link
                          href={`/campaigns/${campaign.campaign_id}`}
                          className="text-sm font-medium text-blue-600 hover:text-blue-900"
                        >
                          {campaign.title}
                        </Link>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            campaign.is_active
                              ? 'bg-green-100 text-green-800'
                              : 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          {campaign.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(
                          campaign.start_date
                        ).toLocaleDateString()}{' '}
                        -{' '}
                        {new Date(
                          campaign.end_date
                        ).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2 max-w-[100px]">
                            <div
                              className={`h-2.5 rounded-full ${
                                Number(campaign.response_rate) * 100 <
                                30
                                  ? 'bg-red-600'
                                  : Number(campaign.response_rate) *
                                      100 <
                                    70
                                  ? 'bg-yellow-400'
                                  : 'bg-green-600'
                              }`}
                              style={{
                                width: `${(
                                  Number(campaign.response_rate) * 100
                                ).toFixed(2)}%`,
                              }}
                            ></div>
                          </div>
                          <span className="text-sm text-gray-700">
                            {(
                              Number(campaign.response_rate) * 100
                            ).toFixed(2)}
                            %
                          </span>
                        </div>
                      </td>
                    </tr>
                  )
                )
              ) : (
                <tr>
                  <td
                    colSpan={4}
                    className="px-6 py-4 whitespace-nowrap text-sm text-center text-gray-500"
                  >
                    No recent campaigns found
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

interface StatCardProps {
  title: string
  value: number | string
  description: string
  trend: 'up' | 'down' | 'none'
  link: string
}

function StatCard({
  title,
  value,
  description,
  trend,
  link,
}: StatCardProps) {
  return (
    <Link
      href={link}
      className="bg-white rounded-lg shadow overflow-hidden hover:shadow-md transition-shadow"
    >
      <div className="p-5">
        <div className="flex justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500 truncate">
              {title}
            </p>
            <p className="mt-1 text-3xl font-semibold text-gray-900">
              {value}
            </p>
          </div>
          <div>
            {trend === 'up' && (
              <span className="inline-flex items-center p-1 rounded-full bg-green-100 text-green-800">
                <svg
                  className="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 10l7-7m0 0l7 7m-7-7v18"
                  />
                </svg>
              </span>
            )}
            {trend === 'down' && (
              <span className="inline-flex items-center p-1 rounded-full bg-red-100 text-red-800">
                <svg
                  className="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 14l-7 7m0 0l-7-7m7 7V3"
                  />
                </svg>
              </span>
            )}
          </div>
        </div>
        <p className="mt-1 text-sm text-gray-500">{description}</p>
      </div>
    </Link>
  )
}
