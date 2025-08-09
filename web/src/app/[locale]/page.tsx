import Link from 'next/link';
import { getTranslations } from 'next-intl/server';
import Button from '@/components/ui/Button';
import { Shield, Users, TrendingUp, AlertTriangle, CheckCircle, Smartphone } from 'lucide-react';

export default async function Home({
  params
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="relative text-white" style={{background: 'linear-gradient(to right, #008529, #006b1f)'}}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Stop Installment Fraud
              <span className="block text-primary-200">Before It Starts</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
              Advanced fraud detection system that tracks installment purchases across multiple businesses 
              to prevent fraudulent chains and protect your revenue.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/register">
                <Button size="lg" className="bg-white text-primary-600 hover:bg-gray-100">
                  Get Started Free
                </Button>
              </Link>
              <Link href="/download">
                <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-primary-600">
                  Download Apps
                </Button>
              </Link>
            </div>
          </div>
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
      <section className="text-white py-20" style={{backgroundColor: '#008529'}}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Protect Your Business?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Join hundreds of businesses already using InstallmentGuard to prevent fraud 
            and make smarter credit decisions.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/register">
              <Button size="lg" className="bg-white hover:bg-gray-100" style={{color: '#008529'}}>
                Start Free Trial
              </Button>
            </Link>
            <Link href="/contact">
              <Button size="lg" variant="outline" className="border-white text-white hover:bg-white" style={{'--hover-color': '#008529'} as any}>
                Contact Sales
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}