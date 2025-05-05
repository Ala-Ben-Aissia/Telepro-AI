import Link from 'next/link'
import { AppLayout } from '@/components/layout/AppLayout'
import { Button } from '@/components/ui/Button'
import { Metadata } from 'next'
import {
  CheckCircle2,
  BarChart3,
  Users,
  MessageCircle,
  ArrowRight,
  Shield,
  Award,
  TrendingUp,
  Zap,
  Star,
  Play,
  MousePointer,
  Lock,
  ArrowUpRight,
  ChevronDown,
} from 'lucide-react'
import Image from 'next/image'
import {
  FadeIn,
  AnimatedGradientText,
  StaggerContainer,
  StaggerItem,
} from '@/components/ui/Motion'
import { StatCard } from '@/components/ui/StatCard'
import { FeatureCard } from '@/components/ui/FeatureCard'
import { SmallFeatureCard } from '@/components/ui/SmallFeatureCard'

export const metadata: Metadata = {
  title: 'Telepro-AI | Premier Patient Teleprospection Platform',
  description:
    'An advanced healthcare communication platform powered by AI for exceptional patient engagement',
  keywords: [
    'healthcare',
    'teleprospection',
    'patient communication',
    'AI',
    'medical technology',
    'healthcare innovation',
  ],
  authors: [{ name: 'Telepro-AI Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

// Fancy blob background animation component
const AnimatedBackground = () => (
  <div className="absolute inset-0 overflow-hidden pointer-events-none">
    <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-primary-100/40 rounded-full blur-3xl -translate-y-1/2 translate-x-1/3 animate-blob"></div>
    <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-secondary-100/30 rounded-full blur-3xl translate-y-1/3 -translate-x-1/4 animate-blob animation-delay-2000"></div>
    <div className="absolute top-1/2 left-1/3 w-[700px] h-[700px] bg-accent-300/20 rounded-full blur-3xl -translate-y-1/2 animate-blob animation-delay-4000"></div>
  </div>
)

// Subtle grid background with dots
const GridBackground = () => (
  <div className="absolute inset-0 bg-[linear-gradient(to_right,#f0f0f0_1px,transparent_1px),linear-gradient(to_bottom,#f0f0f0_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] pointer-events-none opacity-30"></div>
)

export default function Home() {
  return (
    <AppLayout>
      <div className="flex flex-col items-center">
        {/* Hero Section */}
        <section className="w-full py-24 md:py-40 relative overflow-hidden">
          {/* Enhanced background elements */}
          <div className="absolute inset-0 bg-gradient-to-br from-primary-50 via-surface-50 to-white z-0"></div>
          <AnimatedBackground />
          <GridBackground />

          <div className="container px-6 md:px-12 mx-auto flex flex-col md:flex-row items-center gap-16 relative z-10">
            <div className="flex-1 space-y-8">
              <FadeIn delay={0.1}>
                <div className="inline-flex items-center px-4 py-2 bg-primary-50 border border-primary-100 rounded-full text-primary-700 font-medium text-sm mb-2 shadow-sm backdrop-blur-sm">
                  <span className="flex items-center">
                    <Zap className="h-4 w-4 mr-2" />
                    <span className="relative after:content-[''] after:absolute after:bottom-0 after:left-0 after:h-[4px] after:w-full after:bg-primary-200/60 after:-z-10">
                      Leading Healthcare AI Technology
                    </span>
                  </span>
                </div>
              </FadeIn>

              <div>
                <FadeIn delay={0.2}>
                  <h1 className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-gray-900 tracking-tight leading-tight">
                    Patient Teleprospection
                  </h1>
                </FadeIn>
                <AnimatedGradientText>
                  <span className="block mt-2 bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent text-5xl md:text-6xl lg:text-7xl font-extrabold">
                    Redefined by AI
                  </span>
                </AnimatedGradientText>
              </div>

              <FadeIn delay={0.4}>
                <p className="text-xl md:text-2xl text-gray-700 max-w-[600px] leading-relaxed">
                  Telepro-AI helps healthcare providers build deeper
                  patient relationships through intelligent,
                  personalized communication campaigns.
                </p>
              </FadeIn>

              <FadeIn delay={0.5}>
                <div className="flex flex-col sm:flex-row gap-4 pt-6">
                  <Link href="/register">
                    <Button
                      size="lg"
                      className="px-8 py-6 text-lg font-semibold shadow-xl bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 transition-all duration-300 group border border-primary-500/20 hover:border-primary-600/30 relative overflow-hidden"
                    >
                      <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-white/10 to-transparent opacity-0 group-hover:opacity-100 duration-300 transform -skew-x-12 group-hover:translate-x-full transition-all"></span>
                      <span className="relative flex items-center">
                        Get Started
                        <ArrowRight className="ml-2 h-5 w-5 transition-transform duration-300 group-hover:translate-x-1" />
                      </span>
                    </Button>
                  </Link>
                  <Link href="/login">
                    <Button
                      variant="outline"
                      size="lg"
                      className="px-8 py-6 text-lg font-semibold border-2 hover:bg-gray-50 transition-all duration-300 relative overflow-hidden group"
                    >
                      <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-gray-100 to-transparent opacity-0 group-hover:opacity-100 duration-300 transform -skew-x-12 group-hover:translate-x-full transition-all"></span>
                      <span className="relative">Sign In</span>
                    </Button>
                  </Link>
                </div>
              </FadeIn>

              <FadeIn delay={0.6}>
                <div className="flex flex-wrap gap-8 pt-8">
                  <div className="flex items-center gap-2 group">
                    <div className="bg-primary-100 rounded-full p-1 transition-all duration-300 group-hover:scale-110 group-hover:bg-primary-200">
                      <Shield className="h-5 w-5 text-primary-700" />
                    </div>
                    <span className="text-gray-700 font-medium">
                      HIPAA Compliant
                    </span>
                  </div>
                  <div className="flex items-center gap-2 group">
                    <div className="bg-primary-100 rounded-full p-1 transition-all duration-300 group-hover:scale-110 group-hover:bg-primary-200">
                      <Award className="h-5 w-5 text-primary-700" />
                    </div>
                    <span className="text-gray-700 font-medium">
                      Industry Leading
                    </span>
                  </div>
                  <div className="flex items-center gap-2 group">
                    <div className="bg-primary-100 rounded-full p-1 transition-all duration-300 group-hover:scale-110 group-hover:bg-primary-200">
                      <TrendingUp className="h-5 w-5 text-primary-700" />
                    </div>
                    <span className="text-gray-700 font-medium">
                      96% Satisfaction
                    </span>
                  </div>
                </div>
              </FadeIn>
            </div>

            <div className="flex-1 flex justify-center">
              <FadeIn
                delay={0.6}
                className="w-full max-w-md relative"
              >
                <div
                  className="absolute -top-12 -left-12 w-32 h-32 bg-secondary-200 rounded-full opacity-50 blur-xl animate-pulse"
                  style={{ animationDuration: '8s' }}
                />
                <div
                  className="absolute -bottom-12 -right-12 w-40 h-40 bg-primary-200 rounded-full opacity-50 blur-xl animate-pulse"
                  style={{ animationDuration: '12s' }}
                />

                <div className="relative backdrop-blur-sm bg-white/95 p-8 rounded-3xl shadow-2xl border border-gray-100 hover:shadow-[0_30px_60px_rgba(0,0,0,0.1)] transition-shadow duration-500">
                  <div className="absolute -top-3 -right-3 bg-gradient-to-br from-secondary-500 to-secondary-600 text-white text-xs font-bold px-3 py-1 rounded-full flex items-center gap-1">
                    <Star className="h-3 w-3 fill-white" /> PREMIUM
                  </div>

                  <div className="absolute -bottom-2 -right-2 w-40 h-40 bg-gradient-to-br from-primary-100 to-secondary-100 rounded-full opacity-30 blur-2xl -z-10"></div>

                  <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                    <MessageCircle className="h-6 w-6 text-primary-500" />{' '}
                    Intelligent Patient Communication
                  </h3>

                  <ul className="space-y-5">
                    <li className="flex items-start gap-3 group">
                      <div className="mt-1 bg-primary-100 rounded-full p-1 flex-shrink-0 transition-all duration-300 group-hover:scale-110 group-hover:bg-primary-200 group-hover:shadow-md">
                        <CheckCircle2 className="h-5 w-5 text-primary-600" />
                      </div>
                      <div>
                        <span className="text-gray-900 font-semibold block group-hover:text-primary-700 transition-colors">
                          AI-powered patient segmentation
                        </span>
                        <span className="text-gray-600 text-sm">
                          Target the right patients with precision
                        </span>
                      </div>
                    </li>
                    <li className="flex items-start gap-3 group">
                      <div className="mt-1 bg-primary-100 rounded-full p-1 flex-shrink-0 transition-all duration-300 group-hover:scale-110 group-hover:bg-primary-200 group-hover:shadow-md">
                        <CheckCircle2 className="h-5 w-5 text-primary-600" />
                      </div>
                      <div>
                        <span className="text-gray-900 font-semibold block group-hover:text-primary-700 transition-colors">
                          Personalized communication
                        </span>
                        <span className="text-gray-600 text-sm">
                          Tailor messaging to individual patient needs
                        </span>
                      </div>
                    </li>
                    <li className="flex items-start gap-3 group">
                      <div className="mt-1 bg-primary-100 rounded-full p-1 flex-shrink-0 transition-all duration-300 group-hover:scale-110 group-hover:bg-primary-200 group-hover:shadow-md">
                        <CheckCircle2 className="h-5 w-5 text-primary-600" />
                      </div>
                      <div>
                        <span className="text-gray-900 font-semibold block group-hover:text-primary-700 transition-colors">
                          GDPR-compliant data management
                        </span>
                        <span className="text-gray-600 text-sm">
                          Secure, ethical handling of patient
                          information
                        </span>
                      </div>
                    </li>
                  </ul>

                  <div className="mt-8 pt-6 border-t border-gray-100">
                    <div className="flex justify-between items-center">
                      <div className="flex gap-2">
                        <div className="h-8 w-8 rounded-full bg-gray-200 overflow-hidden shadow-md border border-white">
                          <Image
                            src="/api/placeholder/32/32"
                            width="24"
                            height="24"
                            alt="User"
                            className="h-full w-full object-cover"
                          />
                        </div>
                        <div className="h-8 w-8 rounded-full bg-gray-200 overflow-hidden -ml-4 shadow-md border border-white">
                          <Image
                            src="/api/placeholder/32/32"
                            width="24"
                            height="24"
                            alt="User"
                            className="h-full w-full object-cover"
                          />
                        </div>
                        <div className="h-8 w-8 rounded-full bg-gray-200 overflow-hidden -ml-4 shadow-md border border-white">
                          <Image
                            src="/api/placeholder/32/32"
                            width="24"
                            height="24"
                            alt="User"
                            className="h-full w-full object-cover"
                          />
                        </div>
                      </div>
                      <span className="text-sm text-gray-500 font-medium">
                        Trusted by 2,000+ providers
                      </span>
                    </div>
                  </div>
                </div>
              </FadeIn>
            </div>
          </div>

          {/* Scroll indicator */}
          <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex flex-col items-center text-gray-400 animate-bounce">
            <MousePointer className="h-4 w-4 mb-2" />
            <ChevronDown className="h-4 w-4" />
          </div>
        </section>

        {/* Brands Section */}
        <section className="w-full py-16 bg-white border-y border-gray-100">
          <div className="container px-6 md:px-12 mx-auto">
            <FadeIn>
              <p className="text-center text-gray-500 font-medium mb-10 flex items-center justify-center gap-2 before:content-[''] before:h-[1px] before:w-16 before:bg-gray-300 after:content-[''] after:h-[1px] after:w-16 after:bg-gray-300">
                Trusted by leading healthcare organizations
              </p>
            </FadeIn>

            <StaggerContainer
              className="flex flex-wrap justify-center items-center gap-x-16 gap-y-8"
              delayChildren={0.1}
              staggerChildren={0.1}
            >
              {/* These would typically be actual client logos */}
              <StaggerItem>
                <div className="h-12 w-32 bg-gray-100 rounded opacity-70 hover:opacity-100 transition-opacity hover:shadow-sm"></div>
              </StaggerItem>
              <StaggerItem>
                <div className="h-12 w-32 bg-gray-100 rounded opacity-70 hover:opacity-100 transition-opacity hover:shadow-sm"></div>
              </StaggerItem>
              <StaggerItem>
                <div className="h-12 w-32 bg-gray-100 rounded opacity-70 hover:opacity-100 transition-opacity hover:shadow-sm"></div>
              </StaggerItem>
              <StaggerItem>
                <div className="h-12 w-32 bg-gray-100 rounded opacity-70 hover:opacity-100 transition-opacity hover:shadow-sm"></div>
              </StaggerItem>
              <StaggerItem>
                <div className="h-12 w-32 bg-gray-100 rounded opacity-70 hover:opacity-100 transition-opacity hover:shadow-sm"></div>
              </StaggerItem>
            </StaggerContainer>
          </div>
        </section>

        {/* Stats Section - NEW */}
        <section className="w-full py-16 bg-surface-50">
          <div className="container px-6 md:px-12 mx-auto">
            <StaggerContainer
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
              delayChildren={0.1}
              staggerChildren={0.1}
            >
              <StaggerItem>
                <StatCard
                  number="2,000+"
                  label="Healthcare Providers"
                  icon={<Users className="h-6 w-6" />}
                  color="primary"
                />
              </StaggerItem>
              <StaggerItem>
                <StatCard
                  number="96%"
                  label="Satisfaction Rate"
                  icon={<Award className="h-6 w-6" />}
                  color="secondary"
                />
              </StaggerItem>
              <StaggerItem>
                <StatCard
                  number="65%"
                  label="Engagement Increase"
                  icon={<TrendingUp className="h-6 w-6" />}
                  color="accent"
                />
              </StaggerItem>
              <StaggerItem>
                <StatCard
                  number="100%"
                  label="HIPAA Compliant"
                  icon={<Shield className="h-6 w-6" />}
                  color="primary"
                />
              </StaggerItem>
            </StaggerContainer>
          </div>
        </section>

        {/* Features Section */}
        <section className="w-full py-24 md:py-32 bg-gradient-to-b from-white to-surface-50 relative">
          <div className="absolute left-0 right-0 top-0 h-32 bg-gradient-to-b from-white to-transparent z-10"></div>

          <div className="container px-6 md:px-12 mx-auto relative z-20">
            <FadeIn className="text-center mb-20">
              <div className="inline-flex items-center px-4 py-2 bg-secondary-50 rounded-full border border-secondary-100 text-secondary-700 font-medium text-sm mb-4 shadow-sm backdrop-blur-sm">
                <span>Premium Features</span>
              </div>
              <h2 className="text-4xl md:text-5xl font-extrabold text-gray-900 tracking-tight max-w-3xl mx-auto">
                Advanced tools for exceptional patient engagement
              </h2>
              <p className="mt-6 text-xl text-gray-700 max-w-2xl mx-auto">
                Our platform delivers powerful capabilities to enhance
                patient communication and drive improved healthcare
                outcomes.
              </p>
            </FadeIn>

            <StaggerContainer
              className="grid grid-cols-1 md:grid-cols-3 gap-8"
              delayChildren={0.1}
              staggerChildren={0.2}
            >
              <StaggerItem>
                <FeatureCard
                  icon={<BarChart3 className="h-8 w-8" />}
                  title="Campaign Management"
                  description="Create, manage, and track targeted communication campaigns for different patient segments with precision and ease."
                  color="primary"
                />
              </StaggerItem>
              <StaggerItem>
                <FeatureCard
                  icon={<Users className="h-8 w-8" />}
                  title="Multi-channel Communication"
                  description="Engage patients through their preferred channels including email, SMS, voice, and more for optimal response rates."
                  color="secondary"
                />
              </StaggerItem>
              <StaggerItem>
                <FeatureCard
                  icon={<TrendingUp className="h-8 w-8" />}
                  title="Advanced Analytics"
                  description="Gain actionable insights into campaign performance and patient engagement with comprehensive, real-time analytics."
                  color="accent"
                />
              </StaggerItem>
            </StaggerContainer>

            {/* Additional Features - Expanded Grid - NEW */}
            <StaggerContainer
              className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-8"
              delayChildren={0.3}
              staggerChildren={0.1}
            >
              <StaggerItem className="md:col-span-1">
                <SmallFeatureCard
                  icon={<Shield className="h-6 w-6" />}
                  title="Maximum Security"
                  description="End-to-end encryption and robust security protocols keep all patient data safe and protected."
                  color="primary"
                />
              </StaggerItem>
              <StaggerItem className="md:col-span-1">
                <SmallFeatureCard
                  icon={<Lock className="h-6 w-6" />}
                  title="Regulatory Compliance"
                  description="Built for HIPAA, GDPR, and other healthcare regulations to ensure complete data protection."
                  color="secondary"
                />
              </StaggerItem>
              <StaggerItem className="md:col-span-1">
                <SmallFeatureCard
                  icon={<Zap className="h-6 w-6" />}
                  title="Fast Implementation"
                  description="Seamless integration with your existing healthcare systems, with setup in days not months."
                  color="accent"
                />
              </StaggerItem>
            </StaggerContainer>
          </div>
        </section>

        {/* Video Showcase Section - NEW */}
        <section className="w-full py-24 bg-white relative overflow-hidden">
          <GridBackground />
          <div className="container px-6 md:px-12 mx-auto">
            <FadeIn className="text-center mb-12">
              <div className="inline-flex items-center px-4 py-2 bg-accent-300/10 rounded-full border border-accent-400/20 text-accent-600 font-medium text-sm mb-4 shadow-sm backdrop-blur-sm">
                <span>See it in action</span>
              </div>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Watch how Telepro-AI transforms patient communication
              </h2>
              <p className="text-xl text-gray-700 max-w-2xl mx-auto">
                Our platform makes it easy to create personalized,
                engaging communication that resonates with patients.
              </p>
            </FadeIn>

            <FadeIn delay={0.2}>
              <div className="relative w-full max-w-4xl mx-auto rounded-2xl overflow-hidden shadow-2xl group">
                {/* Video thumbnail with play overlay */}
                <div className="aspect-video bg-gray-100 relative">
                  <Image
                    src="/api/placeholder/1024/576"
                    width={1024}
                    height={576}
                    alt="Video thumbnail"
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center group-hover:bg-opacity-40 transition-all duration-300">
                    <div className="w-20 h-20 rounded-full bg-white flex items-center justify-center shadow-xl group-hover:scale-110 transition-transform duration-300">
                      <Play className="h-8 w-8 text-primary-600 ml-1" />
                    </div>
                  </div>
                </div>
              </div>
            </FadeIn>
          </div>
        </section>

        {/* Testimonial Section */}
        <section className="w-full py-24 bg-surface-50">
          <div className="container px-6 md:px-12 mx-auto">
            <FadeIn className="max-w-3xl mx-auto bg-gradient-to-br from-primary-50 to-surface-50 p-12 rounded-3xl shadow-xl relative border border-primary-100/40">
              <div className="absolute -top-6 -left-6">
                <svg
                  width="48"
                  height="48"
                  viewBox="0 0 48 48"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M14.0156 24.0078C14.0156 20.6797 12.5078 19.9766 10 19.9766V14.0156C17.3906 14.0156 20.0156 17.9688 20.0156 24.9609V33.9844H10.9688V24.0078H14.0156ZM33.9844 24.0078C33.9844 20.6797 32.4766 19.9766 29.9688 19.9766V14.0156C37.3594 14.0156 39.9844 17.9688 39.9844 24.9609V33.9844H30.9375V24.0078H33.9844Z"
                    fill="currentColor"
                    className="text-primary-300"
                  />
                </svg>
              </div>

              <div className="absolute -bottom-6 -right-6">
                <div className="h-12 w-12 bg-secondary-100 rounded-full opacity-70 blur-xl"></div>
              </div>

              <div className="flex flex-col md:flex-row items-center gap-8">
                <div className="w-full md:w-1/3">
                  <div className="relative">
                    <div className="absolute inset-0 bg-gradient-to-br from-primary-100 to-secondary-100 rounded-xl -rotate-6 scale-95 opacity-70"></div>
                    <div className="h-48 w-48 rounded-xl bg-gray-200 overflow-hidden relative shadow-lg border-4 border-white">
                      <Image
                        src="/api/placeholder/192/192"
                        width={200}
                        height={200}
                        alt="Dr. Sarah Johnson"
                        className="h-full w-full object-cover"
                      />
                    </div>
                  </div>
                </div>

                <div className="w-full md:w-2/3">
                  <p className="text-xl md:text-2xl text-gray-800 font-medium leading-relaxed mb-8 relative">
                    <span className="absolute -left-4 -top-1 text-5xl text-primary-200 ">
                      &ldquo;
                    </span>
                    &nbsp;&nbsp;Telepro-AI has transformed how we
                    engage with our patients. The platform&apos;s
                    AI-driven approach has increased our response
                    rates by 65% and significantly improved patient
                    satisfaction scores.&nbsp;
                    <span className="absolute bottom-0 text-5xl text-primary-200">
                      &rdquo;
                    </span>
                  </p>

                  <div>
                    <h4 className="text-lg font-semibold text-gray-900">
                      Dr. Sarah Johnson
                    </h4>
                    <p className="text-gray-600">
                      Chief Medical Officer, Northwest Medical Group
                    </p>
                    <div className="flex items-center mt-2">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <Star
                          key={star}
                          className="h-4 w-4 text-yellow-400 fill-yellow-400"
                        />
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </FadeIn>
          </div>
        </section>

        {/* CTA Section */}
        <section className="w-full py-16 bg-white border-t border-gray-100">
          <div className="container px-6 md:px-12 mx-auto text-center">
            <FadeIn>
              <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-6">
                Ready to transform your patient communication?
              </h2>
              <Link href="/register">
                <Button
                  size="lg"
                  className="px-8 py-6 text-lg font-semibold shadow-xl bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 transition-all duration-300 group"
                >
                  <span className="flex items-center">
                    Get Started Today
                    <ArrowUpRight className="ml-2 h-5 w-5 transition-transform duration-300 group-hover:translate-x-1 group-hover:-translate-y-1" />
                  </span>
                </Button>
              </Link>
            </FadeIn>
          </div>
        </section>
      </div>
    </AppLayout>
  )
}
