'use server'

import { revalidatePath } from 'next/cache'
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

// Helper function to create headers with authorization
async function getAuthHeaders(contentType = 'application/json') {
  const accessToken = (await cookies()).get('accessToken')?.value
  const headers: HeadersInit = {
    'Content-Type': contentType,
  }
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`
  }
  return headers
}

// Helper function to handle fetch responses
async function handleResponse<T>(
  response: Response
): Promise<T | null> {
  if (!response.ok) {
    console.error(`HTTP error! status: ${response.status}`)
    return null
  }
  try {
    return await response.json()
  } catch (error) {
    console.error('Error parsing JSON:', error)
    return null
  }
}

// ----- Patient Actions -----

export async function getPatients(
  filter: 'all' | 'active' | 'inactive'
): Promise<Patient[]> {
  try {
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/?filter=${filter}`,
      { headers }
    )
    const data = await handleResponse<{ results: Patient[] }>(
      response
    )
    return data?.results || []
  } catch (error) {
    console.error('Error fetching patients:', error)
    return []
  }
}

export async function getPatient(
  id: string
): Promise<Patient | null> {
  try {
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/`,
      { headers }
    )
    return await handleResponse<Patient>(response)
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
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/`,
      {
        method: 'PATCH',
        headers,
        body: JSON.stringify(data),
      }
    )
    const result = await handleResponse<Patient>(response)
    if (result) {
      revalidatePath(`/patients/${id}`)
      revalidatePath('/patients')
    }
    return result
  } catch (error) {
    console.error(`Error updating patient ${id}:`, error)
    return null
  }
}

export async function getPatientCampaigns(
  id: string
): Promise<Campaign[]> {
  try {
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/campaigns/`,
      { headers }
    )
    return (await handleResponse<Campaign[]>(response)) || []
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
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/communications/`,
      { headers }
    )
    return (await handleResponse<CommunicationLog[]>(response)) || []
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
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/preferences`,
      { headers }
    )
    return (
      (await handleResponse<Preferences>(response)) ||
      ({} as Preferences)
    )
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
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/active_consents`,
      { headers }
    )
    return (
      (await handleResponse<ActiveConsentRecord[]>(response)) || []
    )
  } catch (error) {
    console.error(`Error fetching consents for patient ${id}:`, error)
    return []
  }
}

export async function updatePatientConsents(
  patientId: string,
  newConsents: Partial<ActiveConsentRecord>[]
): Promise<ActiveConsentRecord[] | null> {
  console.log({ newConsents })
  try {
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${patientId}/active_consents/`,
      {
        method: 'PATCH',
        headers,
        body: JSON.stringify({ consents: newConsents }),
      }
    )
    const result = await handleResponse<ActiveConsentRecord[]>(
      response
    )
    if (result) {
      revalidatePath(`/patient`)
    }
    return result
  } catch (error) {
    console.error(
      `Error updating consent for patient ${patientId}:`,
      error
    )
    return null
  }
}

export async function updatePatientPreferences(
  patientId: string,
  prefs: Partial<Preferences>
): Promise<Preferences | null> {
  try {
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${patientId}/preferences/`,
      {
        method: 'PATCH',
        headers,
        body: JSON.stringify(prefs),
      }
    )
    const result = await handleResponse<Preferences>(response)
    if (result) {
      revalidatePath(`/patient`)
    }
    return result
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
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns${queryParam}`,
      { headers }
    )
    const data = await handleResponse<{ results: Campaign[] }>(
      response
    )
    return data?.results || []
  } catch (error) {
    console.error('Error fetching campaigns:', error)
    return []
  }
}

export async function getCampaign(
  id: number
): Promise<Campaign | null> {
  const accessToken = (await cookies()).get('accessToken')?.value
  if (!accessToken) return null

  try {
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/${id}/`,
      { headers }
    )
    return await handleResponse<Campaign>(response)
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
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/`,
      {
        method: 'POST',
        headers,
        body: JSON.stringify(data),
      }
    )
    const result = await handleResponse<Campaign>(response)
    if (result) {
      revalidatePath('/campaigns')
    }
    return result
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
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/${id}/`,
      {
        method: 'PATCH',
        headers,
        body: JSON.stringify(data),
      }
    )
    const result = await handleResponse<Campaign>(response)
    if (result) {
      revalidatePath(`/campaigns/${id}`)
      revalidatePath('/campaigns')
    }
    return result
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
    const headers = await getAuthHeaders()
    const data = segmentId ? { segment_id: segmentId } : {}
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/${id}/send/`,
      {
        method: 'POST',
        headers,
        body: JSON.stringify(data),
      }
    )
    if (response.ok) {
      revalidatePath(`/campaigns/${id}`)
      return true
    }
    return false
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
    const accessToken = (await cookies()).get('accessToken')?.value
    if (!accessToken) return null

    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/${id}/effectiveness`,
      { headers }
    )
    return await handleResponse<CampaignPerformance>(response)
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
    const accessToken = (await cookies()).get('accessToken')?.value
    if (!accessToken) return null

    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/analytics/channel-metrics?campaign_id=${id}`,
      { headers }
    )
    return await handleResponse<CampaignChannelMetrics>(response)
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
    const accessToken = (await cookies()).get('accessToken')?.value
    if (!accessToken) return null

    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/segments/`,
      { headers }
    )
    const data = await handleResponse<{ results: PatientSegment[] }>(
      response
    )
    return data?.results || []
  } catch (error) {
    console.error('Error fetching segments:', error)
    return []
  }
}

export async function getSegment(
  id: number
): Promise<PatientSegment | null> {
  const accessToken = (await cookies()).get('accessToken')?.value
  if (!accessToken) return null

  try {
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/segments/${id}/`,
      { headers }
    )
    return await handleResponse<PatientSegment>(response)
  } catch (error) {
    console.error(`Error fetching segment ${id}:`, error)
    return null
  }
}

export async function createSegment(
  data: Partial<PatientSegment>
): Promise<PatientSegment | null> {
  try {
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/segments/`,
      {
        method: 'POST',
        headers,
        body: JSON.stringify(data),
      }
    )
    const result = await handleResponse<PatientSegment>(response)
    if (result) {
      revalidatePath('/segments')
    }
    return result
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
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/segments/${id}/`,
      {
        method: 'PATCH',
        headers,
        body: JSON.stringify(data),
      }
    )
    const result = await handleResponse<PatientSegment>(response)
    if (result) {
      revalidatePath(`/segments/${id}`)
      revalidatePath('/segments')
    }
    return result
  } catch (error) {
    console.error(`Error updating segment ${id}:`, error)
    return null
  }
}

export async function getSegmentPatients(
  id: number
): Promise<Patient[] | null> {
  try {
    const accessToken = (await cookies()).get('accessToken')?.value
    if (!accessToken) return null

    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/segments/${id}/patients/`,
      { headers }
    )
    const data = await handleResponse<{ results: Patient[] }>(
      response
    )
    return data?.results || []
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
  campaign_history: Record<string, Campaign>
}

export async function analyzeSegment(
  id: number
): Promise<SegmentStats | null> {
  try {
    const accessToken = (await cookies()).get('accessToken')?.value
    if (!accessToken) return null

    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/segments/${id}/analyze/`,
      { headers }
    )
    return await handleResponse<SegmentStats>(response)
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
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/segments/create_ml_segments/`,
      {
        method: 'POST',
        headers,
        body: JSON.stringify(params),
      }
    )
    const result = await handleResponse<PatientSegment[]>(response)
    if (result) {
      revalidatePath('/segments')
    }
    return result || []
  } catch (error) {
    console.error('Error creating ML segments:', error)
    return []
  }
}

// ----- Dashboard & Analytics Actions -----

export async function getDashboardData(): Promise<DashboardData | null> {
  try {
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/analytics/dashboard/`,
      { headers }
    )
    return await handleResponse<DashboardData>(response)
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    return null
  }
}

export async function getInactivePatients(
  days: number = 90
): Promise<Patient[]> {
  try {
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/analytics/inactive_patients/?days=${days}`,
      { headers }
    )
    return (await handleResponse<Patient[]>(response)) || []
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
    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/analytics/engagement_trends/?days=${days}&interval=${interval}`,
      { headers }
    )
    return await handleResponse<unknown>(response)
  } catch (error) {
    console.error('Error fetching engagement trends:', error)
    return null
  }
}

// ----- Auth Actions -----

export async function register(
  username: string,
  email: string,
  password: string,
  passwordConfirm: string
) {
  try {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/accounts/register/`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          password,
          password_confirm: passwordConfirm,
        }),
      }
    )
    return response.ok
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
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/accounts/token/`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      }
    )

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      return {
        access: false,
        error:
          errorData.detail ||
          'Failed to login. Please check your credentials.',
      }
    }

    const data = await response.json()
    const cookies = await Cookies()
    cookies.set('accessToken', data.access)

    return {
      username: data.username,
      access: data.access,
      user_type: data.user_type,
    }
  } catch {
    return {
      access: false,
      error: 'Failed to login. Please check your credentials.',
    }
  }
}

export async function logout(): Promise<boolean> {
  ;(await cookies()).delete('accessToken')
  cache['user'] = undefined
  return redirect('/auth/login')
}

const cache: { user?: Patient } = {}

export async function getCurrentUser(): Promise<Patient | null> {
  try {
    if (cache['user']) return cache['user']
    const accessToken = (await Cookies()).get('accessToken')?.value
    if (!accessToken) return null

    const headers = await getAuthHeaders()
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/`,
      { headers }
    )
    const data = await handleResponse<{ results: Patient[] }>(
      response
    )
    const user = data?.results[0] || null
    if (user) {
      cache['user'] = user
    }
    return user
  } catch (error) {
    console.error('Error fetching current user:', error)
    return null
  }
}
