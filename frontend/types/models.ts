// Core type definitions matching the backend models

// Patient model
export interface Patient {
  id: string
  email: string
  email_verified: boolean
  phone_number?: string
  phone_verified: boolean
  date_of_birth?: string
  gender?: 'M' | 'F' | 'O' | 'N'
  location?: string
  postal_code?: string
  age_group?: '0-18' | '19-35' | '36-50' | '51-65' | '65+'
  language_preference?: string
  preferred_contact_method?: 'EMAIL' | 'SMS' | 'CALL' | 'NONE'
  contact_time_preferences?: Record<string, unknown>
  campaign_preferences: Record<string, unknown>
  engagement_score: number
  last_campaign_response?: string // ISO date string
  is_active: boolean
  anonymized: boolean
  has_active_consent: boolean
  created_at: string // ISO date string
  updated_at: string // ISO date string
}

// Campaign model
export interface Campaign {
  id: number
  title: string
  category?: number // FK to CampaignCategory
  description: string
  start_date: string // ISO date string
  end_date: string // ISO date string
  is_active: boolean
  created_at: string // ISO date string
  updated_at: string // ISO date string
  target_age_groups: string[]
  target_locations: string[]
  target_languages: string[]
  email_template: string
  sms_template: string
  response_rate: number
}

// Campaign Category
export interface CampaignCategory {
  id: number
  name: string
  description: string
  is_active: boolean
}

// Patient Segment
export interface PatientSegment {
  id: number
  name: string
  description: string
  criteria: Record<string, unknown>
  is_active: boolean
  created_at: string // ISO date string
  updated_at: string // ISO date string
}

// Communication Log
export interface CommunicationLog {
  id: number
  campaign: number // Campaign ID
  patient: string // Patient ID
  communication_type: 'EMAIL' | 'SMS' | 'CALL' | 'NONE'
  status:
    | 'PENDING'
    | 'SENT'
    | 'FAILED'
    | 'DELIVERED'
    | 'READ'
    | 'RESPONDED'
  sent_at?: string // ISO date string
  delivered_at?: string // ISO date string
  read_at?: string // ISO date string
  response?: string
  responded_at?: string // ISO date string
  error_message?: string
  metadata: Record<string, unknown>
}

export type ConsentType =
  | 'GENERAL'
  | 'MARKETING'
  | 'RESEARCH'
  | 'THIRD_PARTY'
  | 'SENSITIVE_DATA'
  | 'AUTOMATED_DECISION'

// Consent Record
export interface ConsentRecord {
  pk: number
  patient: string // Patient ID
  consent_type: ConsentType
  granted: boolean
  timestamp: string // ISO date string
  metadata: Record<string, unknown>
  ip_address?: string
  document_version?: string
  user_agent?: string
  consent_method: ConsentMethod
}

export type ConsentMethod = 'WEB_FORM' | 'API' | 'STAFF' | 'IMPORT'

// Analytics response types
export interface PatientAnalytics {
  demographic_distribution: Record<string, number>
  engagement_metrics: {
    average_engagement: number
    response_rate: number
    preferred_channels: Record<string, number>
  }
  inactive_patients_count: number
  at_risk_patients_count: number
}

export interface CampaignAnalytics {
  total_sent: number
  delivery_rate: number
  response_rate: number
  engagement_by_channel: Record<string, number>
  performance_by_segment: Record<string, number>
  conversion_metrics: Record<string, number>
}

export interface DashboardData {
  recent_campaigns: Campaign[]
  patient_metrics: PatientAnalytics
  campaign_metrics: CampaignAnalytics
  engagement_trends: Record<string, number>[]
}
