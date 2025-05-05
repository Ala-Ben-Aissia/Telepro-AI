import Link from 'next/link'
import { AppLayout } from '@/components/layout/AppLayout'
import { Button } from '@/components/ui/Button'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Telepro-AI | Patient Teleprospection with AI',
  description:
    'A modern healthcare communication platform powered by AI',
  keywords: [
    'healthcare',
    'teleprospection',
    'patient communication',
    'AI',
  ],
  authors: [{ name: 'Telepro-AI Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function Home() {
  return (
    <AppLayout>
      <div className="flex flex-col items-center">
        {/* Hero Section */}
        <section className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-br from-primary-50 to-surface-100">
          <div className="container px-4 md:px-6 mx-auto flex flex-col md:flex-row items-center gap-8">
            <div className="flex-1 space-y-4">
              <h1 className="text-3xl md:text-5xl font-bold text-gray-900">
                Patient Teleprospection with{' '}
                <span className="text-primary-600">AI</span>
              </h1>
              <p className="text-lg text-gray-600 max-w-[600px]">
                Telepro-AI helps healthcare providers connect with
                patients through intelligent, personalized
                communication campaigns.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 pt-4">
                <Link href="/register">
                  <Button size="lg">Get Started</Button>
                </Link>
                <Link href="/login">
                  <Button variant="outline" size="lg">
                    Login
                  </Button>
                </Link>
              </div>
            </div>
            <div className="flex-1 flex justify-center">
              <div className="w-full max-w-md relative">
                <div className="absolute -top-6 -left-6 w-24 h-24 bg-secondary-200 rounded-full opacity-50" />
                <div className="absolute -bottom-6 -right-6 w-32 h-32 bg-primary-200 rounded-full opacity-50" />
                <div className="relative bg-white p-6 rounded-xl shadow-lg">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">
                    Intelligent Patient Communication
                  </h3>
                  <ul className="space-y-3">
                    <li className="flex items-start">
                      <svg
                        className="h-5 w-5 text-primary-500 mt-0.5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                      <span className="ml-2 text-gray-600">
                        AI-powered patient segmentation
                      </span>
                    </li>
                    <li className="flex items-start">
                      <svg
                        className="h-5 w-5 text-primary-500 mt-0.5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                      <span className="ml-2 text-gray-600">
                        Personalized communication campaigns
                      </span>
                    </li>
                    <li className="flex items-start">
                      <svg
                        className="h-5 w-5 text-primary-500 mt-0.5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                      <span className="ml-2 text-gray-600">
                        GDPR-compliant patient data management
                      </span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="w-full py-12 md:py-24 bg-white">
          <div className="container px-4 md:px-6 mx-auto">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900">
                Key Features
              </h2>
              <p className="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
                Our platform offers powerful tools to enhance patient
                communication and improve healthcare outcomes.
              </p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-surface-50 p-6 rounded-lg">
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                  <svg
                    className="h-6 w-6 text-primary-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                    />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Campaign Management
                </h3>
                <p className="text-gray-600">
                  Create, manage, and track targeted communication
                  campaigns for different patient segments.
                </p>
              </div>
              <div className="bg-surface-50 p-6 rounded-lg">
                <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center mb-4">
                  <svg
                    className="h-6 w-6 text-secondary-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z"
                    />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Multi-channel Communication
                </h3>
                <p className="text-gray-600">
                  Reach patients through their preferred channels
                  including email, SMS, and more.
                </p>
              </div>
              <div className="bg-surface-50 p-6 rounded-lg">
                <div className="w-12 h-12 bg-accent-100 rounded-lg flex items-center justify-center mb-4">
                  <svg
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
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Advanced Analytics
                </h3>
                <p className="text-gray-600">
                  Gain insights into campaign performance and patient
                  engagement with detailed analytics.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="w-full py-12 md:py-24 bg-primary-600 text-white">
          <div className="container px-4 md:px-6 mx-auto text-center">
            <h2 className="text-3xl font-bold mb-4">
              Ready to transform patient communication?
            </h2>
            <p className="text-lg text-primary-100 mb-8 max-w-2xl mx-auto">
              Join healthcare providers who are using Telepro-AI to
              improve patient engagement and outcomes.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/register">
                <Button variant="accent" size="lg">
                  Get Started
                </Button>
              </Link>
              <Link href="/login">
                <Button
                  variant="outline"
                  size="lg"
                  className="bg-transparent border-white text-white hover:bg-primary-700"
                >
                  Login
                </Button>
              </Link>
            </div>
          </div>
        </section>
      </div>
    </AppLayout>
  )
}
