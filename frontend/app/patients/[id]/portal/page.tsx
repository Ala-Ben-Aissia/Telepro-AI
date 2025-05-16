"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import {
  Check,
  AlertTriangle,
  ShieldCheck,
  Lock,
  MessageSquare,
  Bell,
  Globe,
  Calendar,
  Clock,
  Mail,
  Phone,
} from "lucide-react";

// Patient interface matching the API response from api/patients/${id}
interface Patient {
  id: string;
  medical_record_number: string | null;
  date_of_birth: string;
  gender: string;
  location: string;
  postal_code: string;
  age_group: string;
  language_preference: string;
  email_verified: boolean;
  phone_verified: boolean;
  phone_number: string | null;
  preferred_contact_method: string;
  has_active_consent: boolean;
  engagement_score: number;
}

// Index signature for preferences
interface PreferencesDictionary {
  [key: string]: string | boolean;
}

// Communication interface matching the API response from api/patients/communications
interface Communication {
  id: number;
  campaign: string;
  communication_type: string;
  status: string;
  sent_at: string;
  delivered_at: string | null;
  read_at: string | null;
}

// Define types for our preferences to help with type safety
interface PreferencesType extends PreferencesDictionary {
  language: string;
  preferred_contact_method: string;
  time_of_day_preference: string;
  receive_appointment_reminders: boolean;
  receive_test_results: boolean;
  receive_newsletters: boolean;
  language_preference: string;
}

export default function PatientPortalPage() {
  const { id } = useParams<{ id: string }>();
  // Patient data from api/patients/${id}
  const [patientData, setPatientData] = useState<Patient | null>(
    null
  );
  // Communications data from api/patients/communications
  const [communications, setCommunications] = useState<
    Communication[]
  >([]);
  // UI preferences derived from patient data
  const [preferences, setPreferences] = useState<PreferencesType>({
    language: "English",
    preferred_contact_method: "SMS",
    time_of_day_preference: "morning",
    receive_appointment_reminders: true,
    receive_test_results: true,
    receive_newsletters: false,
    language_preference: "en",
  });

  // UI state
  const [loading, setLoading] = useState(true);
  const [communicationsLoading, setCommunicationsLoading] =
    useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const [showSecurityVerification, setShowSecurityVerification] =
    useState(false);
  const [securityCode, setSecurityCode] = useState("");

  useEffect(() => {
    // Fetch patient data and communications
    async function fetchData() {
      setLoading(true);
      setCommunicationsLoading(true);
      // const access = (await cookies()).get("accessToken");
      try {
        // Fetch patient data from the specified API
        const patientRes = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/patients/${id}`,
          {
            headers: {
              Authorization: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3NDE0ODA5LCJpYXQiOjE3NDczMjg0MDksImp0aSI6ImI3NWQ2MWVhNTQ1YTQ3OGZiZjQyYzYzMzIzNzBlYzgwIiwidXNlcl9pZCI6MSwicHdkX2NoYW5nZWQiOjE3NDU2NzYyMjEuOTE2MTk2fQ.5Tlowoq87HuAwraKk6_zlgZDOZm1V_S_zt1IWuqlo-k`,
            },
          }
        );

        if (patientRes.ok) {
          const data = await patientRes.json();
          setPatientData(data);

          // Create language mapping
          const languageMap: Record<string, string> = {
            en: "English",
            fr: "French",
            es: "Spanish",
            ar: "Arabic",
            zh: "Chinese",
          };

          // Set derived preferences from patient data
          setPreferences({
            // Map language code to full language name
            language:
              languageMap[data.language_preference] || "English",
            // Take contact method directly from API
            preferred_contact_method: data.preferred_contact_method,
            // Default time preference (can be customized by user)
            time_of_day_preference: "morning",
            // Default notification preferences
            receive_appointment_reminders: true,
            receive_test_results: true,
            receive_newsletters: false,
            // Keep language code for reference
            language_preference: data.language_preference,
          });
        } else {
          throw new Error("Failed to load patient data");
        }

        // Fetch communications data
        const communicationsRes = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/patients/communications`
        );
        if (communicationsRes.ok) {
          const commsData = await communicationsRes.json();
          setCommunications(commsData);
        }
      } catch (e) {
        console.error(e);
        setError("Failed to load data");
      } finally {
        setLoading(false);
        setCommunicationsLoading(false);
      }
    }
    fetchData();
  }, [id]);

  const handlePreferenceChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;

    setPreferences(prev => {
      const newPrefs = { ...prev };

      // Handle different input types appropriately
      if (type === "checkbox") {
        // For checkbox inputs, use the checked boolean value
        if (
          name === "receive_appointment_reminders" ||
          name === "receive_test_results" ||
          name === "receive_newsletters"
        ) {
          newPrefs[name] = checked;
        }
      } else {
        // For non-checkbox inputs, use the string value
        if (
          name === "language" ||
          name === "preferred_contact_method" ||
          name === "time_of_day_preference"
        ) {
          newPrefs[name] = value;
        }
      }

      // Map language name to language code when language preference changes
      if (name === "language") {
        const langCodeMap: Record<string, string> = {
          English: "en",
          French: "fr",
          Spanish: "es",
          Arabic: "ar",
          Chinese: "zh",
        };
        newPrefs.language_preference = langCodeMap[value] || "en";
      }

      return newPrefs;
    });
  };

  const handleMainConsentToggle = () => {
    setShowSecurityVerification(true);
  };

  const verifyAndUpdateConsent = async () => {
    // Validate security code
    if (securityCode.length < 4) {
      setError("Please enter a valid security code");
      return;
    }

    if (!patientData) {
      setError("Patient data not loaded");
      return;
    }

    try {
      // For demo purposes, we'll pretend the verification was successful
      // In a real app, this would verify the code with the backend

      // Update the consent status
      const response = await fetch(`/api/patients/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          has_active_consent: !patientData.has_active_consent,
        }),
      });

      if (response.ok) {
        // Update local patient data
        setPatientData(prevData => {
          if (!prevData) return null;
          return {
            ...prevData,
            has_active_consent: !prevData.has_active_consent,
          };
        });

        setSuccess(
          `Successfully ${
            patientData.has_active_consent ? "withdrawn" : "granted"
          } consent`
        );
        setShowSecurityVerification(false);
        setSecurityCode("");
      } else {
        const errorData = await response.json();
        setError(errorData.message || "Consent update failed");
      }
    } catch (e) {
      console.error(e);
      setError("Failed to update consent status");
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSuccess("");
    setError("");

    if (!patientData) {
      setError("Patient data not loaded");
      setSaving(false);
      return;
    }

    try {
      // Update patient preferences
      const updateData = {
        language_preference: preferences.language_preference,
        preferred_contact_method:
          preferences.preferred_contact_method,
      };

      const response = await fetch(`/api/patients/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updateData),
      });

      if (response.ok) {
        // Update local patient data with new preferences
        setPatientData(prevData => {
          if (!prevData) return null;
          return {
            ...prevData,
            language_preference: preferences.language_preference,
            preferred_contact_method:
              preferences.preferred_contact_method,
          };
        });

        setSuccess("Preferences saved successfully!");
      } else {
        setError("Failed to save preferences");
      }
    } catch (e) {
      console.error(e);
      setError("Failed to save preferences");
    }
    setSaving(false);
  };

  return (
    <div className="max-w-4xl mx-auto bg-white p-6 md:p-10 rounded-xl shadow-lg space-y-8 mt-6 md:mt-10">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl md:text-3xl font-bold text-blue-900">
            Patient Portal
          </h1>
          <p className="text-gray-600 mt-1">
            Manage your communication preferences and consent settings
          </p>
        </div>
        {patientData && (
          <div
            className={`px-4 py-2 rounded-full flex items-center gap-2 ${
              patientData.has_active_consent
                ? "bg-green-100 text-green-800"
                : "bg-amber-100 text-amber-800"
            }`}
          >
            {patientData.has_active_consent ? (
              <Check size={16} className="text-green-600" />
            ) : (
              <AlertTriangle size={16} className="text-amber-600" />
            )}
            <span className="font-medium">
              {patientData.has_active_consent
                ? "Active Consent"
                : "Consent Required"}
            </span>
          </div>
        )}
      </div>

      {loading ? (
        <div className="text-center p-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700 mx-auto"></div>
          <p className="mt-4 text-gray-600">
            Loading your preferences...
          </p>
        </div>
      ) : (
        <form onSubmit={handleSave} className="space-y-8">
          {/* Main Consent Toggle Section */}
          <section className="border border-blue-100 rounded-xl p-5 bg-blue-50/50">
            {patientData && (
              <div className="flex items-center justify-between flex-wrap gap-4">
                <div className="flex items-center gap-3">
                  <div className="bg-blue-100 p-3 rounded-full">
                    <ShieldCheck className="h-6 w-6 text-blue-700" />
                  </div>
                  <div>
                    <h2 className="text-xl font-semibold text-blue-900">
                      General Consent
                    </h2>
                    <p className="text-sm text-gray-600">
                      Control your overall consent status for TelepAI
                      services
                    </p>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={handleMainConsentToggle}
                  className={`px-5 py-2 rounded-lg font-medium transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                    patientData.has_active_consent
                      ? "bg-red-100 text-red-700 hover:bg-red-200 focus:ring-red-500"
                      : "bg-green-100 text-green-700 hover:bg-green-200 focus:ring-green-500"
                  }`}
                >
                  {patientData.has_active_consent
                    ? "Withdraw Consent"
                    : "Give Consent"}
                </button>
              </div>
            )}

            {/* Security Verification Modal */}
            {showSecurityVerification && patientData && (
              <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50">
                <div className="bg-white rounded-xl p-6 max-w-md w-full mx-4 shadow-xl">
                  <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                    <Lock size={18} />
                    Verify Your Identity
                  </h3>
                  <p className="text-gray-600 mb-4">
                    To{" "}
                    {patientData.has_active_consent
                      ? "withdraw"
                      : "give"}{" "}
                    consent, please enter the security code sent to
                    your registered contact method.
                  </p>
                  <div className="mb-5">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Security Code
                    </label>
                    <input
                      type="text"
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Enter code"
                      value={securityCode}
                      onChange={e => setSecurityCode(e.target.value)}
                    />
                  </div>
                  <div className="flex gap-3 justify-end">
                    <button
                      type="button"
                      className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
                      onClick={() => {
                        setShowSecurityVerification(false);
                        setSecurityCode("");
                      }}
                    >
                      Cancel
                    </button>
                    <button
                      type="button"
                      className="px-4 py-2 bg-blue-700 text-white rounded-lg hover:bg-blue-800"
                      onClick={verifyAndUpdateConsent}
                    >
                      Verify & Continue
                    </button>
                  </div>
                </div>
              </div>
            )}
          </section>

          {/* Recent Communications Section */}
          <section className="rounded-xl border border-gray-200 p-5">
            <h2 className="text-xl font-semibold mb-4 text-blue-800 flex items-center gap-2">
              <MessageSquare className="h-5 w-5 text-blue-600" />
              Recent Communications
            </h2>
            <div className="space-y-3">
              {communicationsLoading ? (
                <div className="flex justify-center py-6">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-700"></div>
                </div>
              ) : communications.length === 0 ? (
                <p className="text-gray-400 py-4">
                  No recent communications found.
                </p>
              ) : (
                <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 rounded-lg">
                  <table className="min-w-full divide-y divide-gray-300">
                    <thead className="bg-gray-50">
                      <tr>
                        <th
                          scope="col"
                          className="py-3.5 px-3 text-left text-sm font-semibold text-gray-900"
                        >
                          Campaign
                        </th>
                        <th
                          scope="col"
                          className="py-3.5 px-3 text-left text-sm font-semibold text-gray-900"
                        >
                          Type
                        </th>
                        <th
                          scope="col"
                          className="py-3.5 px-3 text-left text-sm font-semibold text-gray-900"
                        >
                          Status
                        </th>
                        <th
                          scope="col"
                          className="py-3.5 px-3 text-left text-sm font-semibold text-gray-900"
                        >
                          Sent
                        </th>
                        <th
                          scope="col"
                          className="py-3.5 px-3 text-left text-sm font-semibold text-gray-900"
                        >
                          Read
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200 bg-white">
                      {communications.slice(0, 5).map(comm => (
                        <tr key={comm.id}>
                          <td className="py-4 px-3 text-sm">
                            {comm.campaign}
                          </td>
                          <td className="py-4 px-3 text-sm">
                            <span className="inline-flex items-center gap-1">
                              {comm.communication_type === "EMAIL" ? (
                                <Mail className="h-4 w-4 text-blue-600" />
                              ) : comm.communication_type ===
                                "SMS" ? (
                                <Phone className="h-4 w-4 text-green-600" />
                              ) : (
                                <Bell className="h-4 w-4 text-orange-600" />
                              )}
                              {comm.communication_type}
                            </span>
                          </td>
                          <td className="py-4 px-3 text-sm">
                            <span
                              className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                comm.status === "DELIVERED"
                                  ? "bg-green-100 text-green-800"
                                  : comm.status === "SENT"
                                  ? "bg-blue-100 text-blue-800"
                                  : comm.status === "RESPONDED"
                                  ? "bg-purple-100 text-purple-800"
                                  : comm.status === "READ"
                                  ? "bg-indigo-100 text-indigo-800"
                                  : comm.status === "FAILED"
                                  ? "bg-red-100 text-red-800"
                                  : "bg-gray-100 text-gray-800"
                              }`}
                            >
                              {comm.status}
                            </span>
                          </td>
                          <td className="py-4 px-3 text-sm text-gray-500">
                            <div className="flex items-center gap-1">
                              <Calendar className="h-4 w-4 text-gray-400" />
                              {new Date(
                                comm.sent_at
                              ).toLocaleDateString()}
                            </div>
                          </td>
                          <td className="py-4 px-3 text-sm text-gray-500">
                            {comm.read_at ? (
                              <div className="flex items-center gap-1">
                                <Clock className="h-4 w-4 text-gray-400" />
                                {new Date(
                                  comm.read_at
                                ).toLocaleDateString()}
                              </div>
                            ) : (
                              <span className="text-gray-400">
                                Not read
                              </span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
              {!patientData?.has_active_consent && (
                <div className="mt-3 py-2 px-3 bg-amber-50 border border-amber-100 rounded-lg text-amber-800 text-sm">
                  <div className="flex items-center gap-2">
                    <AlertTriangle size={16} />
                    <span>
                      For full access to your communications history,
                      please provide your consent.
                    </span>
                  </div>
                </div>
              )}
            </div>
          </section>

          {/* Communication Preferences Section */}
          <section className="rounded-xl border border-gray-200 p-5">
            <h2 className="text-xl font-semibold mb-4 text-blue-800 flex items-center gap-2">
              <MessageSquare className="h-5 w-5 text-blue-600" />
              Communication Preferences
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Preferred Language
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <Globe className="h-5 w-5 text-gray-400" />
                  </div>
                  <select
                    name="language"
                    value={preferences.language}
                    onChange={handlePreferenceChange}
                    className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="English">English</option>
                    <option value="French">French</option>
                    <option value="Spanish">Spanish</option>
                    <option value="Arabic">Arabic</option>
                    <option value="Chinese">Chinese</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Preferred Contact Method
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                    <Bell className="h-5 w-5 text-gray-400" />
                  </div>
                  <select
                    name="preferred_contact_method"
                    value={preferences.preferred_contact_method}
                    onChange={handlePreferenceChange}
                    className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="EMAIL">Email</option>
                    <option value="SMS">SMS</option>
                    <option value="CALL">Phone Call</option>
                    <option value="NONE">No Communication</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Preferred Time for Communications
                </label>
                <div className="relative">
                  <select
                    name="time_of_day_preference"
                    value={preferences.time_of_day_preference}
                    onChange={handlePreferenceChange}
                    className="block w-full pl-3 pr-3 py-2 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="morning">
                      Morning (8am-12pm)
                    </option>
                    <option value="afternoon">
                      Afternoon (12pm-5pm)
                    </option>
                    <option value="evening">Evening (5pm-9pm)</option>
                  </select>
                </div>
              </div>
            </div>

            {patientData && (
              <div className="flex flex-col gap-2">
                <h3 className="text-sm font-medium text-gray-700">
                  Verification Status
                </h3>
                <div className="border border-gray-200 rounded-lg p-3 space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Mail className="h-5 w-5 text-gray-500" />
                      <span className="text-sm text-gray-700">
                        Email
                      </span>
                    </div>
                    <span
                      className={`text-xs px-2 py-1 rounded-full ${
                        patientData.email_verified
                          ? "bg-green-100 text-green-800"
                          : "bg-amber-100 text-amber-800"
                      }`}
                    >
                      {patientData.email_verified
                        ? "Verified"
                        : "Not Verified"}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Phone className="h-5 w-5 text-gray-500" />
                      <span className="text-sm text-gray-700">
                        Phone
                      </span>
                    </div>
                    <span
                      className={`text-xs px-2 py-1 rounded-full ${
                        patientData.phone_verified
                          ? "bg-green-100 text-green-800"
                          : "bg-amber-100 text-amber-800"
                      }`}
                    >
                      {patientData.phone_verified
                        ? "Verified"
                        : "Not Verified"}
                    </span>
                  </div>
                </div>
              </div>
            )}

            <div className="mt-6 space-y-3">
              <h3 className="font-medium text-gray-900">
                Notification Settings
              </h3>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <label className="flex items-center gap-2 p-3 border border-gray-200 rounded-lg hover:bg-gray-50">
                  <input
                    type="checkbox"
                    name="receive_appointment_reminders"
                    checked={
                      preferences.receive_appointment_reminders
                    }
                    onChange={handlePreferenceChange}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500"
                  />
                  <div>
                    <span className="font-medium block">
                      Appointment Reminders
                    </span>
                    <span className="text-xs text-gray-500">
                      Get notified about upcoming appointments
                    </span>
                  </div>
                </label>

                <label className="flex items-center gap-2 p-3 border border-gray-200 rounded-lg hover:bg-gray-50">
                  <input
                    type="checkbox"
                    name="receive_test_results"
                    checked={preferences.receive_test_results}
                    onChange={handlePreferenceChange}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500"
                  />
                  <div>
                    <span className="font-medium block">
                      Test Results
                    </span>
                    <span className="text-xs text-gray-500">
                      Get notified when test results are ready
                    </span>
                  </div>
                </label>

                <label className="flex items-center gap-2 p-3 border border-gray-200 rounded-lg hover:bg-gray-50">
                  <input
                    type="checkbox"
                    name="receive_newsletters"
                    checked={preferences.receive_newsletters}
                    onChange={handlePreferenceChange}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500"
                  />
                  <div>
                    <span className="font-medium block">
                      Newsletters
                    </span>
                    <span className="text-xs text-gray-500">
                      Receive health newsletters and updates
                    </span>
                  </div>
                </label>
              </div>
            </div>
          </section>

          {/* Feedback Messages */}
          {success && (
            <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg flex items-center gap-2">
              <Check className="h-5 w-5" />
              <span>{success}</span>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg flex items-center gap-2">
              <AlertTriangle className="h-5 w-5" />
              <span>{error}</span>
            </div>
          )}

          {/* Submit Button */}
          <div className="pt-3">
            <button
              type="submit"
              className="w-full bg-blue-700 text-white py-3 rounded-lg hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-semibold text-lg disabled:opacity-60 transition-all"
              disabled={saving}
            >
              {saving ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="h-5 w-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                  Saving...
                </span>
              ) : (
                "Save Preferences"
              )}
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
