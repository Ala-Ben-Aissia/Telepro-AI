'use client'

import { useEffect, useState } from 'react'
import { Button } from '@/components/button'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/card'
import { Checkbox } from '@/components/checkbox'
import {
  MessageSquare,
  Settings2,
  Check,
  Bell,
  Globe,
  Clock,
  Shield,
  Lock,
  Share2,
  Lightbulb,
  Bot,
  Mail,
  Clock as ClockIcon,
} from 'lucide-react'
import {
  ActiveConsentRecord,
  Channel,
  Preferences,
  updatePatientConsents,
  updatePatientPreferences,
} from '@/app/api/actions'

const channels: Channel[] = ['EMAIL', 'SMS', 'CALL', 'NONE']

export default function ConsentForm({
  consents: initialConsents,
  preferences,
  patient_id,
}: {
  consents: ActiveConsentRecord[]
  preferences: Preferences
  patient_id: string
}) {
  const [consents, setConsents] =
    useState<ActiveConsentRecord[]>(initialConsents)
  const [prefs, setPrefs] = useState<Preferences>(preferences)
  const handlePrefUpdate = (
    name: keyof Preferences,
    value: Preferences[keyof Preferences]
  ) => {
    setPrefs((prev) => ({
      ...prev,
      [name]: value,
    }))
  }
  const [isLoading, setIsLoading] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)
  // const handleCheckboxChange =
  //   (consentType: number) => (checked: boolean) => {
  //     setConsents((prevConsents) =>
  //       prevConsents.map((consent) => ({
  //         ...consent,
  //         granted:
  //           consent.consent_type === consentType
  //             ? checked
  //             : consent.granted,
  //         metadata: {
  //           ...consent.metadata,
  //           [consentType]: checked,
  //         },
  //       })),
  //     )
  //     setSaveSuccess(false)
  //   }

  const saveConsents = async () => {
    if (consents.length === 0) return
    setIsLoading(true)
    try {
      const updatedCts = await updatePatientConsents(
        patient_id,
        consents
      )
      setConsents(updatedCts || [])
      const updatedPrefs = await updatePatientPreferences(
        patient_id,
        prefs
      )
      setPrefs(updatedPrefs!)
      setSaveSuccess(true)
      // Reset success message after 3 seconds
      setTimeout(() => {
        setSaveSuccess(false)
      }, 3000)
    } catch (err) {
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }

  // Helper function to get appropriate icon for each consent type
  const getConsentIcon = (consentType: string) => {
    switch (consentType) {
      case 'GENERAL':
        return <Shield className="h-4 w-4 text-blue-600" />
      case 'MARKETING':
        return <Mail className="h-4 w-4 text-blue-600" />
      case 'RESEARCH':
        return <Lightbulb className="h-4 w-4 text-blue-600" />
      case 'THIRD_PARTY':
        return <Share2 className="h-4 w-4 text-blue-600" />
      case 'AUTOMATED_DECISION':
        return <Bot className="h-4 w-4 text-blue-600" />
      default:
        return <Lock className="h-4 w-4 text-blue-600" />
    }
  }

  // Helper function to format consent type for display
  // const formatConsentType = (consentType: string) => {
  //   return consentType
  //     .replace('_', ' ')
  //     .toLowerCase()
  //     .split(' ')
  //     .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
  //     .join(' ')
  // }

  // Helper function to get description for each consent type
  const getConsentDescription = (consentType: string) => {
    switch (consentType) {
      case 'GENERAL':
        return 'General consent for processing personal information'
      case 'MARKETING':
        return 'Allow us to send you marketing communications'
      case 'RESEARCH':
        return 'Allow use of your data for healthcare research'
      case 'THIRD_PARTY':
        return 'Allow sharing your information with trusted partners'
      case 'AUTOMATED_DECISION':
        return 'Allow automated processing for personalized care'
      default:
        return 'Consent for data processing'
    }
  }

  // Helper function to format consent method for display
  const formatConsentMethod = (method: string) => {
    switch (method) {
      case 'WEB_FORM':
        return 'Web Form'
      case 'IMPORT':
        return 'Imported'
      case 'API':
        return 'API'
      default:
        return method
    }
  }
  //
  // const handleUpdateConsent = async function(consent_pk: number, granted: boolean) {
  //   try {
  //     await updatePatientConsents(patient_id, consent_pk, granted)
  //   }
  // }

  // const handleChannelUpdate = async (
  //   name: string,
  //   value: string | boolean
  // ) => {
  //   console.log('handleChannelUpdate called with:', { name, value })
  //   setSaveSuccess(false)
  //   try {
  //     console.log('Attempting to update preference:', { name, value })
  //     // Simulate preference update logic here
  //     // For example: await updatePreference(name, value);
  //     console.log('Update successful')
  //     setSaveSuccess(true)
  //   } catch (error) {
  //     console.error('Error updating preference:', error)
  //     setSaveSuccess(false)
  //   }
  // }

  const handleConsentUpdate = function (
    granted: boolean,
    consentType: string
  ) {
    setConsents((prevConsents) => {
      const newConsents = prevConsents.map((consent) => {
        if (consent.consent_type !== consentType) return consent
        return {
          ...consent,
          granted,
          granted_at: new Date().toISOString(),
        }
      })
      return newConsents
    })
  }

  useEffect(() => {
    if (!Array.isArray(prefs.preferred_contact_methods)) {
      setPrefs((prev) => ({
        ...prev,
        preferred_contact_methods: [
          prefs.preferred_contact_methods as Channel,
        ],
      }))
    }
  }, [prefs.preferred_contact_methods])

  return (
    <div className="space-y-6">
      {/* Consent Settings Card */}
      <Card className="border border-blue-100 shadow-md overflow-hidden">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg text-blue-900 flex items-center gap-2">
            <Settings2 className="h-5 w-5 text-indigo-600" />
            Consent Settings
          </CardTitle>
        </CardHeader>

        {consents.length > 0 && (
          <CardContent>
            <div className="space-y-4">
              {consents.map((consent) => {
                const isChecked = consent.granted
                return (
                  <div
                    key={Math.random()}
                    className="flex items-start p-4 rounded-lg border border-blue-100 bg-blue-50 hover:bg-blue-100/30 transition-colors"
                  >
                    <div className="mt-0.5 mr-3">
                      <div className="p-1.5 bg-blue-100 rounded-md">
                        {getConsentIcon(consent.consent_type)}
                      </div>
                    </div>
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <Checkbox
                            id={consent.consent_type}
                            checked={isChecked}
                            onCheckedChange={(checked: boolean) => {
                              handleConsentUpdate(
                                checked,
                                consent.consent_type
                              )
                            }}
                            // onCheckedChange={handleCheckboxChange(
                            //   consent.consent_type,
                            // )}
                            className="border-blue-600 data-[state=checked]:bg-blue-600 data-[state=checked]:text-white"
                          />
                          <label
                            htmlFor={consent.consent_type}
                            className="text-sm font-medium text-blue-900 leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                          >
                            {consent.consent_type}
                          </label>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            {formatConsentMethod(
                              consent.consent_method
                            )}
                          </span>
                        </div>
                      </div>
                      <p className="text-sm text-gray-600 ml-6">
                        {getConsentDescription(consent.consent_type)}
                      </p>
                      <div className="flex items-center gap-2 ml-6 mt-1 text-xs text-gray-500">
                        <ClockIcon className="h-3 w-3" />
                        <span>
                          {new Date(
                            consent.granted_at
                          ).toLocaleDateString('en-US', {
                            day: 'numeric',
                            month: 'long',
                            year: 'numeric',
                          })}
                        </span>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        )}
      </Card>

      {/* Communication Preferences Card */}
      <Card className="border border-blue-100 shadow-md overflow-hidden">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg text-blue-900 flex items-center gap-2">
            <MessageSquare className="h-5 w-5 text-indigo-600" />
            Communication Preferences
          </CardTitle>
        </CardHeader>

        <CardContent>
          <div className="grid gap-4 sm:grid-cols-2">
            {/* Contact Method Column */}
            <div className="space-y-4">
              <h3 className="text-md font-semibold text-blue-900 flex items-center gap-2">
                <Globe className="h-4 w-4 text-indigo-500" />
                Contact Methods
              </h3>

              <div className="space-y-3">
                {channels.map((channel, index) => {
                  const currentMethods = Array.isArray(
                    prefs?.preferred_contact_methods
                  )
                    ? prefs.preferred_contact_methods
                    : prefs?.preferred_contact_methods
                    ? [prefs.preferred_contact_methods]
                    : []

                  // If array is empty, default to NONE being selected
                  const isChecked =
                    currentMethods.length === 0 && channel === 'NONE'
                      ? true
                      : currentMethods.includes(channel)

                  return (
                    <div
                      key={index}
                      className="flex items-start p-3 rounded-md border border-blue-100 bg-blue-50 hover:bg-blue-100/30 transition-colors"
                    >
                      <div className="flex-1 space-y-1">
                        <div className="flex items-center space-x-2">
                          <Checkbox
                            id={`channel-${index}`}
                            checked={isChecked}
                            onCheckedChange={(checked: boolean) => {
                              let updatedMethods

                              if (channel === 'NONE') {
                                // If NONE is selected, clear all other options
                                updatedMethods = checked
                                  ? ['NONE']
                                  : []
                              } else {
                                // For other channels
                                if (checked) {
                                  // Remove NONE if it exists, then add the new channel
                                  const methodsWithoutNone =
                                    currentMethods.filter(
                                      (method) => method !== 'NONE'
                                    )
                                  updatedMethods =
                                    methodsWithoutNone.includes(
                                      channel
                                    )
                                      ? methodsWithoutNone
                                      : [
                                          ...methodsWithoutNone,
                                          channel,
                                        ]
                                } else {
                                  // Remove the channel
                                  updatedMethods =
                                    currentMethods.filter(
                                      (method) => method !== channel
                                    )
                                  // If no methods left, default to NONE
                                  if (updatedMethods.length === 0) {
                                    updatedMethods = ['NONE']
                                  }
                                }
                              }

                              handlePrefUpdate(
                                'preferred_contact_methods',
                                updatedMethods
                              )
                            }}
                            className="border-blue-600 data-[state=checked]:bg-blue-600 data-[state=checked]:text-white"
                          />
                          <label
                            htmlFor={`channel-${index}`}
                            className="text-sm font-medium text-blue-900 leading-none"
                          >
                            {channel}
                          </label>
                        </div>
                        <p className="text-sm text-gray-600 ml-6">
                          {channel === 'CALL'
                            ? 'Receive phone calls for important updates'
                            : channel === 'SMS'
                            ? 'Get text message alerts and reminders'
                            : channel === 'EMAIL'
                            ? 'Receive detailed information via email'
                            : channel === 'NONE'
                            ? 'Opt out of all communications'
                            : ''}
                        </p>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Additional Preferences Column */}
            <div className="space-y-4">
              <h3 className="text-md font-semibold text-blue-900 flex items-center gap-2">
                <Bell className="h-4 w-4 text-indigo-500" />
                Notification Preferences
              </h3>

              <div className="space-y-3">
                <div className="flex items-start p-3 rounded-md border border-blue-100 bg-blue-50 hover:bg-blue-100/30 transition-colors">
                  <div className="flex-1 space-y-1">
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="appointment-reminders"
                        checked={true}
                        onCheckedChange={() => {}}
                        className="border-blue-600 data-[state=checked]:bg-blue-600 data-[state=checked]:text-white"
                      />
                      <label
                        htmlFor="appointment-reminders"
                        className="text-sm font-medium text-blue-900 leading-none"
                      >
                        Appointment Reminders
                      </label>
                    </div>
                    <p className="text-sm text-gray-600 ml-6">
                      Receive reminders about upcoming appointments
                    </p>
                  </div>
                </div>

                <div className="flex items-start p-3 rounded-md border border-blue-100 bg-blue-50 hover:bg-blue-100/30 transition-colors">
                  <div className="flex-1 space-y-1">
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="time-preference"
                        checked={true}
                        onCheckedChange={() => {}}
                        className="border-blue-600 data-[state=checked]:bg-blue-600 data-[state=checked]:text-white"
                      />
                      <label
                        htmlFor="time-preference"
                        className="text-sm font-medium text-blue-900 leading-none"
                      >
                        Communication Timing
                      </label>
                    </div>
                    <div className="flex items-center gap-2 ml-6 mt-2">
                      <Clock className="h-3 w-3 text-indigo-500" />
                      <span className="text-xs text-blue-700">
                        Morning (8AM - 12PM)
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Save Button and Success Message */}
      <div className="flex justify-between items-center">
        {saveSuccess && (
          <div className="flex items-center gap-2 text-green-700 bg-green-50 px-4 py-2 rounded-md border border-green-200 animate-coin-bounce">
            <Check className="h-4 w-4" />
            <span className="text-sm">
              Your preferences have been saved successfully
            </span>
          </div>
        )}
        <div className="ml-auto">
          <Button
            onClick={saveConsents}
            disabled={isLoading || consents.length === 0}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 shadow-sm transition-colors"
          >
            {isLoading ? (
              <div className="flex items-center gap-2">
                <div className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Saving...</span>
              </div>
            ) : (
              'Save Changes'
            )}
          </Button>
        </div>
      </div>
    </div>
  )
}
