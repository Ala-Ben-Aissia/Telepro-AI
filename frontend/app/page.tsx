import { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'Telepro-AI | AI-Powered Patient Teleprospection System',
  description:
    'An intelligent system for patient segmentation, proactive identification and optimized healthcare campaigns',
}

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      {/* Hero Section */}
      <div className="relative isolate overflow-hidden">
        <div className="absolute inset-0 -z-10 opacity-30">
          <div className="absolute inset-y-0 right-1/2 -z-10 mr-16 w-[200%] origin-bottom-left skew-x-[-30deg] bg-gradient-to-tl from-blue-100 to-indigo-50 opacity-30 sm:mr-28 lg:mr-0 xl:mr-16 xl:origin-center"></div>
          <svg
            className="absolute left-[max(50%,25rem)] top-0 h-[64rem] w-[128rem] -translate-x-1/2"
            viewBox="0 0 1155 678"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fill="url(#ecb5b0c9-546c-4772-8c71-4d3f06d544bc)"
              fillOpacity=".3"
              d="M317.219 518.975L203.852 678 0 438.341l317.219 80.634 204.172-286.402c1.307 132.337 45.083 346.658 209.733 145.248C936.936 126.058 882.053-94.234 1031.02 41.331c119.18 108.451 130.68 295.337 121.53 375.223L855 299l21.173 362.054-558.954-142.079z"
            />
            <defs>
              <linearGradient
                id="ecb5b0c9-546c-4772-8c71-4d3f06d544bc"
                x1="1155.49"
                x2="-78.208"
                y1=".177"
                y2="474.645"
                gradientUnits="userSpaceOnUse"
              >
                <stop stopColor="#4F46E5" />
                <stop offset={1} stopColor="#80CAFF" />
              </linearGradient>
            </defs>
          </svg>
        </div>

        <div className="mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:flex lg:items-center lg:gap-x-10 lg:px-8 lg:py-40">
          <div className="mx-auto max-w-2xl lg:mx-0 lg:flex-auto">
            <h1 className="mt-10 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              <span className="block text-indigo-600">
                Telepro-AI
              </span>
              <span className="block mt-2">
                Intelligent Healthcare Prospecting
              </span>
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              Transform patient outreach with AI-powered segmentation,
              proactive identification, and optimized healthcare
              campaigns to deliver personalized care when it matters
              most.
            </p>
            <div className="mt-10 flex items-center gap-x-6">
              <Link
                href="/auth/login"
                className="rounded-md bg-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 transition-all duration-200"
              >
                Log in to dashboard
              </Link>
              <Link
                href="/auth/register"
                className="rounded-md border border-indigo-600 bg-white px-6 py-3 text-sm font-semibold text-indigo-600 shadow-sm hover:bg-indigo-50 transition-all duration-200"
              >
                Register for free trial
              </Link>
            </div>
          </div>
          <div className="mt-16 sm:mt-24 lg:mt-0 lg:flex-shrink-0 lg:flex-grow">
            <div className="relative mx-auto w-[22rem] max-w-full">
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="h-full w-full rounded-3xl bg-gradient-to-tr from-indigo-500 to-blue-500 opacity-20 blur-3xl"></div>
              </div>
              <div className="relative rounded-3xl border border-gray-200 bg-white/80 p-8 shadow-xl backdrop-blur-sm">
                <div className="absolute -bottom-px left-1/2 h-px w-3/4 bg-gradient-to-r from-transparent via-blue-500 to-transparent -translate-x-1/2"></div>
                <Image
                  src="/globe.svg"
                  alt="Telepro AI Dashboard Visualization"
                  width={150}
                  height={150}
                  className="mx-auto mb-6"
                />
                <div className="space-y-4">
                  <div className="h-2 w-3/4 rounded bg-gray-200"></div>
                  <div className="h-2 w-11/12 rounded bg-gray-200"></div>
                  <div className="h-2 w-5/6 rounded bg-gray-200"></div>
                  <div className="h-8 w-full rounded-md bg-indigo-100"></div>
                  <div className="grid grid-cols-3 gap-2">
                    <div className="h-16 rounded-md bg-blue-50"></div>
                    <div className="h-16 rounded-md bg-indigo-50"></div>
                    <div className="h-16 rounded-md bg-purple-50"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-white py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:text-center">
            <h2 className="text-base font-semibold leading-7 text-indigo-600">
              AI-Powered Insights
            </h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Everything you need to optimize patient outreach
            </p>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              Our platform uses advanced machine learning algorithms
              to analyze patient data, identify trends, and generate
              actionable insights for healthcare providers.
            </p>
          </div>
          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
            <div className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-2 lg:gap-y-16">
              {[
                {
                  title: 'Patient Segmentation',
                  description:
                    'Automatically categorize patients based on demographics, medical history, and care needs.',
                  icon: '/window.svg',
                },
                {
                  title: 'Predictive Analytics',
                  description:
                    'Identify patients who may benefit from early intervention using predictive models.',
                  icon: '/file.svg',
                },
                {
                  title: 'Campaign Optimization',
                  description:
                    'Design and implement data-driven outreach campaigns with measurable outcomes.',
                  icon: '/next.svg',
                },
                {
                  title: 'Secure & Compliant',
                  description:
                    'HIPAA-compliant platform with enterprise-grade security for patient data protection.',
                  icon: '/globe.svg',
                },
              ].map((feature, idx) => (
                <div
                  key={idx}
                  className="relative flex flex-col gap-6 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-300 hover:shadow-md"
                >
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-indigo-50">
                    <Image
                      src={feature.icon}
                      alt={feature.title}
                      width={24}
                      height={24}
                      className="text-indigo-600"
                    />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold leading-8 tracking-tight text-gray-900">
                      {feature.title}
                    </h3>
                    <p className="mt-2 text-base leading-7 text-gray-600">
                      {feature.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Testimonial Section */}
      <div className="relative isolate overflow-hidden bg-white py-24 sm:py-32">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(45rem_50rem_at_top,theme(colors.gray.100),theme(colors.white))] opacity-30"></div>
        <div className="mx-auto max-w-2xl lg:max-w-4xl">
          <div className="text-center">
            <h2 className="text-lg font-semibold leading-8 text-indigo-600">
              Trusted by healthcare leaders
            </h2>
            <figure className="mt-10">
              <blockquote className="text-center text-xl font-semibold leading-8 text-gray-900 sm:text-2xl sm:leading-9">
                <p>
                  "Telepro-AI has revolutionized how we approach
                  patient outreach. We've seen a 40% increase in
                  preventive care appointments and significantly
                  improved patient satisfaction scores."
                </p>
              </blockquote>
              <figcaption className="mt-10">
                <div className="mx-auto h-12 w-12 overflow-hidden rounded-full">
                  <div className="h-full w-full bg-indigo-600 flex items-center justify-center">
                    <span className="text-white font-bold text-lg">
                      DR
                    </span>
                  </div>
                </div>
                <div className="mt-4 flex items-center justify-center space-x-3 text-base">
                  <div className="font-semibold text-gray-900">
                    Dr. Rebecca Chen
                  </div>
                  <svg
                    viewBox="0 0 2 2"
                    width={3}
                    height={3}
                    className="fill-gray-400"
                  >
                    <circle cx={1} cy={1} r={1} />
                  </svg>
                  <div className="text-gray-600">
                    Chief Medical Officer, Healthcare Partners
                  </div>
                </div>
              </figcaption>
            </figure>
          </div>
        </div>
      </div>

      {/* Final CTA Section */}
      <div className="bg-white py-20">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl rounded-3xl bg-indigo-600 p-8 text-center ring-1 ring-inset ring-gray-900/10 lg:flex lg:items-center lg:justify-between lg:max-w-5xl lg:p-12">
            <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl lg:text-left">
              Ready to transform patient outreach?
              <br />
              <span className="text-indigo-200">
                Start your free trial today.
              </span>
            </h2>
            <div className="mt-6 lg:mt-0 lg:ml-8 lg:flex-shrink-0">
              <Link
                href="/auth/register"
                className="inline-flex items-center justify-center rounded-md bg-white px-8 py-3 text-base font-medium text-indigo-600 shadow-sm hover:bg-indigo-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white transition-all duration-200"
              >
                Get started
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-50 py-12">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="border-t border-gray-200 pt-8 md:flex md:items-center md:justify-between text-center md:text-left">
            <p className="text-sm text-gray-500">
              &copy; {new Date().getFullYear()} Telepro-AI. All rights reserved.
            </p>
            <div className="mt-4 md:mt-0 flex justify-center md:justify-end space-x-6">
              <a href="#" className="text-gray-400 hover:text-indigo-600 transition-colors">
                Terms of Service
              </a>
              <a href="#" className="text-gray-400 hover:text-indigo-600 transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="text-gray-400 hover:text-indigo-600 transition-colors">
                Contact
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
