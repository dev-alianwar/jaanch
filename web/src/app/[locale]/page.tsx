import Link from 'next/link';
import { getTranslations } from 'next-intl/server';
import { Button } from '@/theme/components';
import { Shield, Users, TrendingUp, AlertTriangle, CheckCircle, Smartphone } from 'lucide-react';
import TransparentHeader from '@/components/layout/TransparentHeader';
export default async function Home({
  params
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  return (
    <>
      {/* Transparent Header overlaying the hero section */}
      <TransparentHeader variant="dark" />

      <div className="bg-white -mt-16">
        {/* Hero Section */}
        <section className="relative text-white overflow-hidden pt-32 pb-24" style={{ background: 'linear-gradient(135deg, #008529 0%, #006b1f 50%, #005515 100%)' }}>
          {/* Background Pattern */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute inset-0" style={{
              backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
            }}></div>
          </div>

          {/* Floating Elements */}
          <div className="absolute top-20 left-10 w-20 h-20 bg-white bg-opacity-10 rounded-full animate-pulse"></div>
          <div className="absolute top-40 right-20 w-16 h-16 bg-white bg-opacity-15 rounded-full animate-pulse delay-1000"></div>
          <div className="absolute bottom-20 left-1/4 w-12 h-12 bg-white bg-opacity-20 rounded-full animate-pulse delay-2000"></div>

          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-10 flex flex-wrap">
            <div className="w-full md:w-1/2">
              {/* Please add a mobile app screen shot here*/}
            </div>
            <div className="w-full md:w-1/2">
              <div className="text-center">
                <div className="mb-6">
                  <span className="inline-block px-4 py-2 bg-white text-gray-900 dark:text-white bg-opacity-20 rounded-full font-medium mb-4 backdrop-blur-sm">
                    🛡️ Advanced Fraud Protection
                  </span>
                </div>
                <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
                  Stop Installment Fraud
                  <span className="block text-green-200 mt-2">Before It Starts</span>
                </h1>
                <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto text-green-100 leading-relaxed">
                  Advanced fraud detection system that tracks installment purchases across multiple businesses
                  to prevent fraudulent chains and protect your revenue.
                </p>
                <div className="flex flex-col sm:flex-row gap-6 justify-center max-w-md mx-auto">
                  <Link href="/register" className="flex-1">
                    <Button
                      size="xl"
                      variant="secondary"
                      icon={<span>🚀</span>}
                      className="shadow-lg hover:shadow-xl font-semibold w-full"
                      fullWidth
                    >
                      Get Started Free
                    </Button>
                  </Link>
                </div>
              </div>  </div>

          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Comprehensive Fraud Protection
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Our advanced system detects fraudulent patterns where customers obtain products on installment,
                sell for cash, and repeat the cycle across multiple businesses.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <div className="bg-white p-8 rounded-lg shadow-sm border">
                <Shield className="h-12 w-12 text-primary-500 mb-4" />
                <h3 className="text-xl font-semibold mb-3">Real-time Fraud Detection</h3>
                <p className="text-gray-600">
                  Advanced algorithms analyze customer behavior patterns and detect suspicious activities
                  across multiple businesses in real-time.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-sm border">
                <Users className="h-12 w-12 text-primary-600 mb-4" />
                <h3 className="text-xl font-semibold mb-3">Cross-Business Intelligence</h3>
                <p className="text-gray-600">
                  Share customer installment history across participating businesses to make
                  informed credit decisions and prevent fraud chains.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-sm border">
                <TrendingUp className="h-12 w-12 text-primary-700 mb-4" />
                <h3 className="text-xl font-semibold mb-3">Risk Assessment</h3>
                <p className="text-gray-600">
                  Comprehensive risk scoring system that evaluates customer creditworthiness
                  and fraud probability based on historical data.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-sm border">
                <AlertTriangle className="h-12 w-12 text-red-600 mb-4" />
                <h3 className="text-xl font-semibold mb-3">Automated Alerts</h3>
                <p className="text-gray-600">
                  Instant notifications when suspicious patterns are detected, allowing
                  businesses to take immediate action to prevent losses.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-sm border">
                <CheckCircle className="h-12 w-12 text-primary-500 mb-4" />
                <h3 className="text-xl font-semibold mb-3">Easy Integration</h3>
                <p className="text-gray-600">
                  Simple API integration and user-friendly interfaces for businesses
                  of all sizes to start protecting against fraud immediately.
                </p>
              </div>

              <div className="bg-white p-8 rounded-lg shadow-sm border">
                <Smartphone className="h-12 w-12 text-primary-600 mb-4" />
                <h3 className="text-xl font-semibold mb-3">Mobile & Web Access</h3>
                <p className="text-gray-600">
                  Access the system from anywhere with native mobile apps and
                  comprehensive web platform for maximum flexibility.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                How InstallmentGuard Works
              </h2>
              <p className="text-xl text-gray-600">
                Simple, effective fraud prevention in three steps
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary-600">1</span>
                </div>
                <h3 className="text-xl font-semibold mb-3">Customer Applies</h3>
                <p className="text-gray-600">
                  Customer submits installment request through your business or our platform
                </p>
              </div>

              <div className="text-center">
                <div className="bg-primary-200 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary-700">2</span>
                </div>
                <h3 className="text-xl font-semibold mb-3">Fraud Analysis</h3>
                <p className="text-gray-600">
                  Our system analyzes customer history across all participating businesses
                </p>
              </div>

              <div className="text-center">
                <div className="bg-primary-300 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-primary-800">3</span>
                </div>
                <h3 className="text-xl font-semibold mb-3">Informed Decision</h3>
                <p className="text-gray-600">
                  Make confident approval decisions with comprehensive risk assessment
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-24 bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 relative overflow-hidden">
          <div className="absolute inset-0 bg-black opacity-10"></div>
          <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div className="mb-8">
              <span className="inline-flex items-center px-4 py-2 bg-white bg-opacity-20 text-white rounded-full text-sm font-semibold backdrop-blur-sm">
                🛡️ Trusted by Businesses
              </span>
            </div>
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white leading-tight">
              Ready to protect your business?
            </h2>
            <p className="text-xl mb-12 max-w-2xl mx-auto text-primary-100 leading-relaxed">
              Join hundreds of businesses already using InstallmentGuard to prevent fraud
              and make smarter credit decisions.
            </p>
            <div className="flex flex-col sm:flex-row gap-6 justify-center max-w-md mx-auto">
              <Link href="/register" className="flex-1">
                <Button
                  size="xl"
                  variant="secondary"
                  className="font-semibold shadow-xl w-full"
                >
                  Start Free Trial
                </Button>
              </Link>
              <Link href="/contact" className="flex-1">
                <Button
                  size="xl"
                  variant="outline"
                  className="border-2 border-white text-white hover:bg-white hover:text-primary-700 font-semibold w-full"
                >
                  Contact Sales
                </Button>
              </Link>
            </div>
          </div>
        </section>
      </div>
    </>
  );
}