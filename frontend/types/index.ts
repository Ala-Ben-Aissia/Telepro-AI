// User and Authentication Types
export interface User {
  user_id: string
  username: string
  email: string
  user_type: 'STAFF' | 'PATIENT'
  patient_uuid?: string | null
}

export interface TokenResponse {
  access: string
  refresh: string
  user_id: string
  username: string
  email: string
  user_type: 'STAFF' | 'PATIENT'
  patient_uuid?: string | null
}

export interface DecodedToken {
  exp: number
  iat: number
  jti: string
  token_type: string
  user_id: string
  pwd_changed: number
}

// Patient Types
export interface PatientProfile {
  id: string
  medical_record_number: string | null
  date_of_birth: string | null
  gender: string | null
  location: string | null
  postal_code: string | null
  age_group: string | null
  language_preference: string | null
  email_verified: boolean
  phone_verified: boolean
  preferred_contact_method: 'EMAIL' | 'SMS' | 'CALL' | 'NONE'
  has_active_consent: boolean
  engagement_score: number
}

export interface PatientPreferences {
  preferred_contact_method: 'EMAIL' | 'SMS' | 'CALL' | 'NONE'
  contact_time_preferences: Record<string, unknown>
  campaign_preferences: Record<string, unknown>
  language_preference: string
}

export interface PatientConsent {
  has_active_consent: boolean
}

export interface ConsentRecord {
  consent_type:
    | 'GENERAL'
    | 'MARKETING'
    | 'RESEARCH'
    | 'THIRD_PARTY'
    | 'SENSITIVE_DATA'
    | 'AUTOMATED_DECISION'
  granted: boolean
  metadata: Record<string, unknown>
}

// Campaign Types
export interface Campaign {
  id: string
  title: string
  category: CampaignCategory | null
  description: string
  start_date: string
  end_date: string
  is_active: boolean
  target_age_groups: string[]
  target_locations: string[]
  target_languages: string[]
  email_template: string
  sms_template: string
}

export interface CampaignCategory {
  id: string
  name: string
  description: string
  is_active: boolean
}

export interface PatientSegment {
  id: string
  name: string
  description: string
  criteria: Record<string, unknown>
  is_active: boolean
}

export interface CommunicationLog {
  id: string
  campaign: string | Campaign
  communication_type: 'EMAIL' | 'SMS' | 'CALL' | 'NONE'
  status:
    | 'PENDING'
    | 'SENT'
    | 'FAILED'
    | 'DELIVERED'
    | 'READ'
    | 'RESPONDED'
  sent_at: string | null
  delivered_at: string | null
  read_at: string | null
  response?: string
  error_message?: string
  metadata?: Record<string, unknown>
  message?: string // For frontend display
}

// Analytics Types
export interface DashboardStats {
  totalPatients: number
  activeCampaigns: number
  communicationsSent: number
  responseRate: number
  readRate?: number
  avgResponseTimeHours?: number
}

export interface RecentCampaign {
  id: string
  title: string
  start_date: string
  end_date: string
  is_active: boolean
  target_count: number
  sent_count: number
  response_count: number
}

export interface AnalyticsResponse {
  engagement_overview: EngagementOverview
  campaign_performance: CampaignPerformance
  communication_channels: CommunicationChannels
  time_of_day: TimeOfDay
  period_days: number
}

export interface CampaignEffectiveness {
  campaign_id: string
  sent_count: number
  delivered_count: number
  read_count: number
  response_count: number
  delivery_rate: number
  read_rate: number
  response_rate: number
}

export interface CampaignPerformanceItem {
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
  segments: Array<{
    id: number
    name: string
    patient_count: number
  }>
}

export interface CampaignPerformance {
  campaigns: CampaignPerformanceItem[]
  overall_metrics: {
    total_campaigns: number
    total_communications: number
    overall_response_rate: number
    overall_read_rate: number
  }
  period_days: number
}

export interface EngagementOverview {
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

export interface EngagementTrends {
  dates: string[]
  metrics: {
    sent: number[]
    delivered: number[]
    read: number[]
    responded: number[]
    response_rate: number[]
  }
}

export interface ChannelMetricsItem {
  total: number
  responded: number
  read: number
  response_rate: number
  read_rate: number
  avg_response_time_hours: number
}

export interface CommunicationChannels {
  channel_metrics: {
    EMAIL: ChannelMetricsItem
    SMS: ChannelMetricsItem
    CALL: ChannelMetricsItem
  }
  best_response_channel: string | null
  fastest_response_channel: string | null
  period_days: number
}

export interface TimeMetricsItem {
  total: number
  responded: number
  read: number
  response_rate: number
  read_rate: number
  avg_response_time_hours: number
}

export interface TimeOfDay {
  time_metrics: {
    morning: TimeMetricsItem
    afternoon: TimeMetricsItem
    evening: TimeMetricsItem
    night: TimeMetricsItem
  }
  best_time_period: string | null
  period_days: number
}

// API Response Types
export interface ApiResponse<T> {
  data: T
  status: number
  message?: string
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface ErrorResponse {
  detail: string
  code?: string
  errors?: Record<string, string[]>
}
