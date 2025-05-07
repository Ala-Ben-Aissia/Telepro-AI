'use server'

import { revalidatePath } from 'next/cache'
import apiClient from '@/lib/api-client'
import type {
  Patient,
  Campaign,
  PatientSegment,
  CommunicationLog,
  ConsentRecord,
  DashboardData,
} from '@/types/models'
import { cookies, cookies as Cookies } from 'next/headers'
import { redirect } from 'next/navigation'

// ----- Patient Actions -----

export async function getPatients(
  filter: 'all' | 'active' | 'inactive'
): Promise<Patient[]> {
  try {
    console.log({ filter })
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
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/`
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

export async function getPatientCommunications(
  id: string
): Promise<CommunicationLog[]> {
  try {
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/communications/`
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

export async function getPatientConsents(
  id: string
): Promise<ConsentRecord[]> {
  try {
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${id}/consents/`
    )
    return response.data
  } catch (error) {
    console.error(`Error fetching consents for patient ${id}:`, error)
    return []
  }
}

export async function updatePatientConsent(
  patientId: string,
  consentType: string,
  granted: boolean
): Promise<ConsentRecord | null> {
  try {
    const response = await apiClient.post(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/patients/${patientId}/update_consent/`,
      {
        consent_type: consentType,
        granted,
      }
    )
    revalidatePath(`/patients/${patientId}`)
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
  try {
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/${id}/`
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

export async function getCampaignPerformance(
  id: number
): Promise<unknown> {
  try {
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/${id}/performance/`
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

// ----- Segment Actions -----

export async function getSegments(): Promise<PatientSegment[]> {
  try {
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/campaigns/segments/`,
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
    console.error('Error fetching segments:', error)
    return []
  }
}

export async function getSegment(
  id: number
): Promise<PatientSegment | null> {
  try {
    const response = await apiClient.get(`/api/segments/${id}/`)
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
): Promise<Patient[]> {
  try {
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/segments/${id}/patients/`
    )
    return response.data
  } catch (error) {
    console.error(`Error fetching patients for segment ${id}:`, error)
    return []
  }
}

export async function analyzeSegment(id: number): Promise<unknown> {
  try {
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/segments/${id}/analyze/`
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

export async function getCurrentUser(): Promise<unknown> {
  try {
    const accessToken = (await Cookies()).get('accessToken')?.value
    const response = await apiClient.get(
      `${process.env.NEXT_PUBLIC_API_BASE_URL}/api/accounts/profile/`,
      { headers: { Authorization: `Bearer ${accessToken}` } }
    )
    return response.data
  } catch (error) {
    console.log('Error fetching current user:', error)
    return null
  }
}
