'use client'
import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import { ConsentRecord } from '@/types/models'

export default function PatientPortalPage() {
  const { id } = useParams<{ id: string }>()
  const [consents, setConsents] = useState<ConsentRecord[]>([])
  const [preferences, setPreferences] = useState({
    language: 'English',
    notifications: true,
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [success, setSuccess] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    // Fetch consents and preferences for this patient
    async function fetchData() {
      setLoading(true)
      try {
        // TODO: Replace with your API endpoints
        const consentRes = await fetch(`/api/patients/${id}/consents`)
        const prefsRes = await fetch(
          `/api/patients/${id}/preferences`
        )
        if (consentRes.ok) {
          setConsents(await consentRes.json())
        }
        if (prefsRes.ok) {
          setPreferences(await prefsRes.json())
        }
      } catch (e) {
        console.log(e)
        setError('Failed to load data')
      }
      setLoading(false)
    }
    fetchData()
  }, [id])

  const handleConsentChange = (pk: number) => {
    setConsents((prev) =>
      prev.map((c) =>
        c.pk === pk ? { ...c, granted: !c.granted } : c
      )
    )
  }

  const handlePreferenceChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target
    const checked = (e.target as HTMLInputElement).checked
    setPreferences((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }))
  }

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setSuccess('')
    setError('')
    try {
      // TODO: Replace with your API endpoints
      const consentRes = await fetch(`/api/patients/${id}/consents`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(consents),
      })
      const prefsRes = await fetch(
        `/api/patients/${id}/preferences`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(preferences),
        }
      )
      if (consentRes.ok && prefsRes.ok) {
        setSuccess('Preferences saved!')
      } else {
        setError('Failed to save preferences')
      }
    } catch (e) {
      console.log(e)
      setError('Failed to save preferences')
    }
    setSaving(false)
  }

  return (
    <div className="max-w-3xl mx-auto bg-white p-10 rounded-xl shadow-lg space-y-10 mt-10">
      <h1 className="text-3xl font-bold mb-2 text-blue-900">
        Patient Portal
      </h1>
      <p className="text-gray-600 mb-6">
        Manage your data sharing consents and personal preferences
        below.
      </p>
      {loading ? (
        <div className="text-center text-gray-500">Loading...</div>
      ) : (
        <form onSubmit={handleSave} className="space-y-8">
          <section>
            <h2 className="text-xl font-semibold mb-4 text-blue-800 flex items-center gap-2">
              <svg
                className="w-5 h-5 text-blue-500"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M9 12l2 2l4-4"
                />
              </svg>
              Consents
            </h2>
            <ul className="space-y-3">
              {consents.length === 0 && (
                <li className="text-gray-400">No consents found.</li>
              )}
              {consents.map((consent) => (
                <li
                  key={consent.pk}
                  className="flex items-center gap-4 bg-gray-50 rounded p-3"
                >
                  <input
                    type="checkbox"
                    checked={consent.granted}
                    onChange={() => handleConsentChange(consent.pk)}
                    className="h-5 w-5 accent-blue-600"
                    id={`consent-${consent.pk}`}
                  />
                  <label
                    htmlFor={`consent-${consent.pk}`}
                    className="text-gray-800 text-base"
                  >
                    {consent.consent_type.replace(/_/g, ' ')}
                  </label>
                  <span
                    className={`ml-auto text-xs px-2 py-1 rounded ${
                      consent.granted
                        ? 'bg-green-100 text-green-700'
                        : 'bg-red-100 text-red-700'
                    }`}
                  >
                    {consent.granted ? 'Granted' : 'Revoked'}
                  </span>
                </li>
              ))}
            </ul>
          </section>
          <section>
            <h2 className="text-xl font-semibold mb-4 text-blue-800 flex items-center gap-2">
              <svg
                className="w-5 h-5 text-blue-500"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 4v16m8-8H4"
                />
              </svg>
              Preferences
            </h2>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-1">
                Language
              </label>
              <select
                name="language"
                value={preferences.language}
                onChange={handlePreferenceChange}
                className="w-full border rounded p-2"
              >
                <option value="English">English</option>
                <option value="French">French</option>
                <option value="Spanish">Spanish</option>
              </select>
            </div>
            <div>
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  name="notifications"
                  checked={preferences.notifications}
                  onChange={handlePreferenceChange}
                  className="h-5 w-5 accent-blue-600"
                />
                Receive notifications
              </label>
            </div>
          </section>
          {success && (
            <div className="text-green-600 font-medium">
              {success}
            </div>
          )}
          {error && (
            <div className="text-red-600 font-medium">{error}</div>
          )}
          <button
            type="submit"
            className="w-full bg-blue-700 text-white py-3 rounded-lg hover:bg-blue-800 font-semibold text-lg disabled:opacity-60"
            disabled={saving}
          >
            {saving ? 'Saving...' : 'Save Preferences'}
          </button>
        </form>
      )}
    </div>
  )
}
