'use server'

import { revalidatePath } from 'next/cache'
import apiClient from '@/lib/api-client'
import type {
  Patient,
  Campaign,
  PatientSegment,
  CommunicationLog,
  DashboardData,
  ConsentType,
  ConsentMethod,
} from '@/types/models'
import { cookies, cookies as Cookies } from 'next/headers'
import { redirect } from 'next/navigation'

// ----- Patient Actions -----

export async function getPatients(
  filter: 'all' | 'active' | 'inactive'
): Promise<Patient[]> {
  try {
    const accessToken = (await cookies()).get('accessToken')?.value
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/?filter=${filter}`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    )
    return response.data.results
  } catch (error) {
    console.error('Error fetching patients:', error)
    return []
  }
}

export async function getPatient(
  id: string
): Promise<Patient | null> {
  try {
    const accessToken = (await cookies()).get('accessToken')?.value
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    )
    return response.data
  } catch (error) {
    console.error(`Error fetching patient ${id}:`, error)
    return null
  }
}

export async function updatePatient(
  id: string,
  data: Partial<Patient>
): Promise<Patient | null> {
  try {
    const response = await apiClient.patch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/`,
      data
    )
    revalidatePath(`/patients/${id}`)
    revalidatePath('/patients')
    return response.data
  } catch (error) {
    console.error(`Error updating patient ${id}:`, error)
    return null
  }
}

export async function getPatientCampaigns(
  id: string
): Promise<Campaign[]> {
  try {
    const accessToken = (await cookies()).get('accessToken')?.value
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/campaigns/`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    )
    return response.data
  } catch (error) {
    console.error(
      `Error fetching communications for patient ${id}:`,
      error
    )
    return []
  }
}

export async function getPatientCommunications(
  id: string
): Promise<CommunicationLog[]> {
  try {
    const accessToken = (await cookies()).get('accessToken')?.value
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/communications/`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    )
    return response.data
  } catch (error) {
    console.error(
      `Error fetching communications for patient ${id}:`,
      error
    )
    return []
  }
}

export type Preferences = {
  preferred_contact_method: Channel | null
  contact_time_preferences: Record<string, unknown>
  campaign_preferences: number[]
  language_preference: string
}

export async function getPatientPreferences(
  id: string
): Promise<Preferences> {
  try {
    const accessToken = (await cookies()).get('accessToken')?.value
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/preferences/`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    )
    return response.data
  } catch (error) {
    console.error(`Error fetching consents for patient ${id}:`, error)
    return {} as Preferences
  }
}

export type ActiveConsentRecord = {
  consent_type: ConsentType
  granted_at: string
  granted: boolean
  consent_method: ConsentMethod
}

export async function getPatientConsents(
  id: string
): Promise<ActiveConsentRecord[]> {
  try {
    const accessToken = (await cookies()).get('accessToken')?.value
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/active_consents/`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    )
    return response.data
  } catch (error) {
    console.error(`Error fetching consents for patient ${id}:`, error)
    return []
  }
}

export async function updatePatientConsents(
  patientId: string,
  newConsents: Partial<ActiveConsentRecord>[]
): Promise<ActiveConsentRecord[] | null> {
  try {
    const response = await apiClient.patch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${patientId}/active_consents/`,
      { consents: newConsents },
      {
        headers: {
          Authorization: `Bearer ${
            (await cookies()).get('accessToken')?.value
          }`,
        },
      }
    )
    revalidatePath(`/patient`)
    return response.data
  } catch (error) {
    console.error(
      `Error updating consent for patient ${patientId}:`,
      error
    )
    return null
  }
}

// ----- Campaign Actions -----

export async function getCampaigns(
  is_active?: string
): Promise<Campaign[]> {
  try {
    const queryParam =
      is_active === 'all'
        ? ''
        : `?active=${is_active === 'active' ? 'True' : 'False'}`
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns${queryParam}`,
      {
        headers: {
          Authorization: `Bearer ${
            (await cookies()).get('accessToken')?.value
          }`,
        },
      }
    )
    return response.data.results
  } catch (error) {
    console.error('Error fetching campaigns:', error)
    return []
  }
}

export async function getCampaign(
  id: number
): Promise<Campaign | null> {
  const access = (await cookies()).get('accessToken')?.value
  if (!access) return null
  try {
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/${id}/`,
      {
        headers: {
          Authorization: `Bearer ${access}`,
        },
      }
    )
    return response.data
  } catch (error) {
    console.error(`Error fetching campaign ${id}:`, error)
    return null
  }
}

export async function getActiveCampaigns() {}

export async function createCampaign(
  data: Partial<Campaign>
): Promise<Campaign | null> {
  try {
    const response = await apiClient.post(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/`,
      data
    )
    revalidatePath('/campaigns')
    return response.data
  } catch (error) {
    console.error('Error creating campaign:', error)
    return null
  }
}

export async function updateCampaign(
  id: number,
  data: Partial<Campaign>
): Promise<Campaign | null> {
  try {
    const response = await apiClient.patch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/${id}/`,
      data
    )
    revalidatePath(`/campaigns/${id}`)
    revalidatePath('/campaigns')
    return response.data
  } catch (error) {
    console.error(`Error updating campaign ${id}:`, error)
    return null
  }
}

export async function sendCampaign(
  id: number,
  segmentId?: number
): Promise<boolean> {
  try {
    const data = segmentId ? { segment_id: segmentId } : {}
    await apiClient.post(`/api/campaigns/${id}/send/`, data)
    revalidatePath(`/campaigns/${id}`)
    return true
  } catch (error) {
    console.error(`Error sending campaign ${id}:`, error)
    return false
  }
}

type CampaignPerformance = {
  total_sent: number
  delivered: number
  responded: number
  failed: number
  response_rate: number
}

type Channel = 'EMAIL' | 'SMS' | 'CALL' | 'NONE'

type ChannelMetrics = {
  total: number
  responded: number
  read: number
  response_rate: number
  read_rate: number
  avg_response_time_hours: number
}

type CampaignChannels = {
  [key in Channel]?: ChannelMetrics
}

type CampaignChannelMetrics = {
  channel_metrics: CampaignChannels
  best_response_channel: Channel
  fastest_response_channel: Channel | null
  period_days: number
}

export async function getCampaignPerformance(
  id: number
): Promise<CampaignPerformance | null> {
  try {
    const access = (await cookies()).get('accessToken')?.value
    if (!access) return null
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/${id}/effectiveness`,
      { headers: { Authorization: `Bearer ${access}` } }
    )
    return response.data
  } catch (error) {
    console.error(
      `Error fetching performance for campaign ${id}:`,
      error
    )
    return null
  }
}

export async function getCampaignChannelMetrics(
  id: string
): Promise<CampaignChannelMetrics | null> {
  try {
    const access = (await cookies()).get('accessToken')?.value
    if (!access) return null
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/analytics/channel-metrics?campaign_id=${id}`,
      { headers: { getAuthorization: `Bearer ${access}` } }
    )
    return response.data
  } catch (error) {
    console.error(
      `Error fetching channel metrics for campaign ${id}:`,
      error
    )
    return null
  }
}

// ----- Segment Actions -----

export async function getSegments(): Promise<
  PatientSegment[] | null
> {
  try {
    const access = (await cookies()).get('accessToken')?.value
    if (!access) return null
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/segments/`,
      {
        headers: {
          Authorization: `Bearer ${access}`,
        },
      }
    )
    return response.data.results
  } catch (error) {
    console.error('Error fetching segments:', error)
    return []
  }
}

export async function getSegment(
  id: number
): Promise<PatientSegment | null> {
  const access = (await cookies()).get('accessToken')?.value
  if (!access) return null
  try {
    const response = await apiClient.get(
      `/api/campaigns/segments/${id}/`,
      {
        headers: { Authorization: `Bearer ${access}` },
      }
    )
    return response.data
  } catch (error) {
    console.error(`Error fetching segment ${id}:`, error)
    return null
  }
}

export async function createSegment(
  data: Partial<PatientSegment>
): Promise<PatientSegment | null> {
  try {
    const response = await apiClient.post('/api/segments/', data)
    revalidatePath('/segments')
    return response.data
  } catch (error) {
    console.error('Error creating segment:', error)
    return null
  }
}

export async function updateSegment(
  id: number,
  data: Partial<PatientSegment>
): Promise<PatientSegment | null> {
  try {
    const response = await apiClient.patch(
      `/api/segments/${id}/`,
      data
    )
    revalidatePath(`/segments/${id}`)
    revalidatePath('/segments')
    return response.data
  } catch (error) {
    console.error(`Error updating segment ${id}:`, error)
    return null
  }
}

export async function getSegmentPatients(
  id: number
): Promise<Patient[] | null> {
  try {
    const access = (await cookies()).get('accessToken')?.value
    if (!access) return null
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/segments/${id}/patients/`,
      { headers: { Authorization: `Bearer ${access}` } }
    )
    return response.data.results
  } catch (error) {
    console.error(`Error fetching patients for segment ${id}:`, error)
    return []
  }
}

type SegmentStats = {
  status: 'success'
  segment_id: number
  segment_name: string
  patient_count: number
  basic_stats: {
    total_patients: number
    by_age_group: {
      [ageGroup: string]: {
        count: number
        percentage: number
      }
    }
    by_gender: {
      [gender: string]: {
        count: number
        percentage: number
      }
    }
    by_language: {
      [languageCode: string]: {
        count: number
        percentage: number
      }
    }
  }
  engagement_metrics: {
    avg_engagement_score: number
    high_engagement_count: number
    medium_engagement_count: number
    low_engagement_count: number
  }
  communication_preferences: {
    email: number
    sms: number
    call: number
    none: number
  }
  campaign_history: Record<string, Campaign> // or {} if it's always an empty object
}

export async function analyzeSegment(
  id: number
): Promise<SegmentStats | null> {
  try {
    const access = (await cookies()).get('accessToken')?.value
    if (!access) return null
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/segments/${id}/analyze/`,
      { headers: { Authorization: `Bearer ${access}` } }
    )
    return response.data
  } catch (error) {
    console.error(`Error analyzing segment ${id}:`, error)
    return null
  }
}

export async function createMlSegments(params: {
  algorithm: string
  n_clusters: number
  name_prefix: string
}): Promise<PatientSegment[]> {
  try {
    const response = await apiClient.post(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/segments/create_ml_segments/`,
      params
    )
    revalidatePath('/segments')
    return response.data
  } catch (error) {
    console.error('Error creating ML segments:', error)
    return []
  }
}

// ----- Dashboard & Analytics Actions -----

export async function getDashboardData(): Promise<DashboardData | null> {
  try {
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/analytics/dashboard/`
    )
    return response.data
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    return null
  }
}

export async function getInactivePatients(
  days: number = 90
): Promise<Patient[]> {
  try {
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/analytics/inactive_patients/?days=${days}`
    )
    return response.data
  } catch (error) {
    console.error('Error fetching inactive patients:', error)
    return []
  }
}

export async function getEngagementTrends(
  days: number = 90,
  interval: 'day' | 'week' | 'month' = 'week'
): Promise<unknown> {
  try {
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/analytics/engagement_trends/?days=${days}&interval=${interval}`
    )
    return response.data
  } catch (error) {
    console.error('Error fetching engagement trends:', error)
    return null
  }
}

// ----- Auth Actions -----

type Err = { response?: { data?: { detail: string } } }

export async function register(
  username: string,
  email: string,
  password: string,
  passwordConfirm: string
) {
  try {
    await apiClient.post(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/accounts/register/`,
      {
        username,
        email,
        password,
        password_confirm: passwordConfirm,
      }
    )
    return true
  } catch {
    return false
  }
}

export async function login(
  username: string,
  password: string
): Promise<{
  access: string | boolean
  username?: string
  user_type?: 'STAFF' | 'PATIENT'
  error?: string
}> {
  try {
    const response = await apiClient.post(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/accounts/token/`,
      { username, password }
    )
    const cookies = await Cookies()
    cookies.set('accessToken', response.data.access)
    return {
      username: response.data.username,
      access: response.data.access,
      user_type: response.data.user_type,
    }
  } catch (error: unknown) {
    return {
      access: false,
      error:
        (error as Err).response?.data?.detail ||
        'Failed to login. Please check your credentials.',
    }
  }
}

export async function logout(): Promise<boolean> {
  ;(await cookies()).delete('accessToken')
  return redirect('/auth/login')
}

const cache: { user?: Patient } = {}

export async function getCurrentUser(): Promise<Patient | null> {
  try {
    if (cache['user']) return cache['user']
    const accessToken = (await Cookies()).get('accessToken')?.value
    if (!accessToken) return null

    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    )
    const user = response.data.results[0]
    cache['user'] = user
    return user
  } catch (error) {
    console.error('Error fetching current user:', error)
    return null
  }
}
