import { Metadata } from 'next';
import Link from 'next/link';
import { 
  Shield, 
  Users, 
  TrendingUp, 
  CheckCircle, 
  Smartphone, 
  AlertTriangle,
  BarChart3,
  Clock,
  Database,
  Globe,
  Lock,
  Zap
} from 'lucide-react';
import Button from '@/components/ui/Button';

export const metadata: Metadata = {
  title: 'Features - Fraud Detection System',
  description: 'Comprehensive fraud detection features including real-time monitoring, multi-business tracking, and advanced analytics.',
};

export default function FeaturesPage() {

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="relative text-white" style={{background: 'linear-gradient(to right, #008529, #005515)'}}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Powerful Features
            </h1>
            <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
              Advanced fraud detection capabilities designed to protect your business and customers
            </p>
            <Link href="/register">
              <Button size="lg" className="bg-white text-primary-600 hover:bg-gray-100">
                Start Free Trial
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Core Features Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Core Features
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Everything you need to detect and prevent installment fraud
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-lg shadow-sm border">
              <Shield className="h-12 w-12 text-primary-600 mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Real-Time Fraud Detection
              </h3>
              <p className="text-gray-600 mb-4">
                Instantly identify suspicious installment patterns across multiple businesses and prevent fraud before it happens.
              </p>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Instant alerts
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Pattern recognition
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Risk scoring
                </li>
              </ul>
            </div>

            <div className="bg-white p-8 rounded-lg shadow-sm border">
              <Users className="h-12 w-12 text-primary-500 mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Multi-Business Network
              </h3>
              <p className="text-gray-600 mb-4">
                Connect multiple businesses to share fraud intelligence and create a comprehensive protection network.
              </p>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Cross-business tracking
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Shared blacklists
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Network analytics
                </li>
              </ul>
            </div>

            <div className="bg-white p-8 rounded-lg shadow-sm border">
              <TrendingUp className="h-12 w-12 text-primary-700 mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Advanced Analytics
              </h3>
              <p className="text-gray-600 mb-4">
                Comprehensive reporting and analytics to understand fraud patterns and improve your detection strategies.
              </p>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Custom dashboards
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Trend analysis
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Export reports
                </li>
              </ul>
            </div>

            <div className="bg-white p-8 rounded-lg shadow-sm border">
              <Smartphone className="h-12 w-12 text-primary-500 mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Mobile Applications
              </h3>
              <p className="text-gray-600 mb-4">
                Native mobile apps for iOS and Android with full functionality for on-the-go fraud detection.
              </p>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Push notifications
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Offline mode
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Quick verification
                </li>
              </ul>
            </div>

            <div className="bg-white p-8 rounded-lg shadow-sm border">
              <AlertTriangle className="h-12 w-12 text-primary-600 mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Smart Alerts
              </h3>
              <p className="text-gray-600 mb-4">
                Intelligent notification system that learns from your preferences and reduces false positives.
              </p>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Priority levels
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Custom rules
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Multi-channel delivery
                </li>
              </ul>
            </div>

            <div className="bg-white p-8 rounded-lg shadow-sm border">
              <BarChart3 className="h-12 w-12 text-primary-700 mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Risk Assessment
              </h3>
              <p className="text-gray-600 mb-4">
                Automated risk scoring system that evaluates customers and transactions in real-time.
              </p>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  ML-powered scoring
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Historical analysis
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-2" />
                  Customizable thresholds
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Technical Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Technical Capabilities
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built on modern technology stack for reliability and performance
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Clock className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Real-Time Processing
              </h3>
              <p className="text-gray-600 text-sm">
                Sub-second response times for all fraud detection queries
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Database className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Scalable Database
              </h3>
              <p className="text-gray-600 text-sm">
                Handle millions of transactions with enterprise-grade database
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Globe className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                API Integration
              </h3>
              <p className="text-gray-600 text-sm">
                RESTful APIs for seamless integration with existing systems
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Lock className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Bank-Level Security
              </h3>
              <p className="text-gray-600 text-sm">
                End-to-end encryption and compliance with financial standards
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Highlight Section */}
      <section className="py-20 bg-primary-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Trusted by Businesses Worldwide
            </h2>
            <p className="text-xl text-primary-100 max-w-3xl mx-auto">
              Our fraud detection system is protecting businesses across multiple industries
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold mb-2">500+</div>
              <p className="text-primary-200">Active Businesses</p>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">$50M+</div>
              <p className="text-primary-200">Fraud Prevented</p>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">99.8%</div>
              <p className="text-primary-200">Customer Satisfaction</p>
            </div>
          </div>
        </div>
      </section>

      {/* User Roles Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Built for Every User
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Tailored experiences for different user roles and responsibilities
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-lg shadow-sm border">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Users className="h-8 w-8" style={{color: '#008529'}} />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4 text-center">
                Customer Portal
              </h3>
              <ul className="space-y-3 text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-3" />
                  View installment history
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-3" />
                  Update personal information
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-3" />
                  Dispute flagged transactions
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-3" />
                  Security notifications
                </li>
              </ul>
            </div>

            <div className="bg-white p-8 rounded-lg shadow-sm border">
              <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4 text-center">
                Business Dashboard
              </h3>
              <ul className="space-y-3 text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-3" />
                  Real-time fraud monitoring
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-3" />
                  Customer verification tools
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-3" />
                  Analytics and reporting
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-3" />
                  Risk management settings
                </li>
              </ul>
            </div>

            <div className="bg-white p-8 rounded-lg shadow-sm border">
              <div className="bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <Shield className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4 text-center">
                Super Admin Panel
              </h3>
              <ul className="space-y-3 text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-3" />
                  System-wide monitoring
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-3" />
                  Business management
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-3" />
                  Global fraud patterns
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-primary-600 mr-3" />
                  Platform configuration
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Performance Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Performance That Matters
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built for speed, reliability, and scale
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="bg-primary-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                <Zap className="h-10 w-10 text-primary-600" />
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-2">&lt;500ms</div>
              <p className="text-gray-600">Average response time</p>
            </div>

            <div>
              <div className="bg-primary-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="h-10 w-10 text-primary-600" />
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-2">99.9%</div>
              <p className="text-gray-600">Uptime guarantee</p>
            </div>

            <div>
              <div className="bg-primary-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                <Database className="h-10 w-10 text-primary-600" />
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-2">1M+</div>
              <p className="text-gray-600">Transactions per day</p>
            </div>

            <div>
              <div className="bg-primary-100 rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-4">
                <Shield className="h-10 w-10 text-primary-600" />
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-2">95%</div>
              <p className="text-gray-600">Fraud detection accuracy</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="text-white py-20" style={{backgroundColor: '#008529'}}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Experience These Features?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Start your free trial today and see how our fraud detection system can protect your business
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/register">
              <Button size="lg" className="bg-white text-primary-600 hover:bg-gray-100">
                Start Free Trial
              </Button>
            </Link>
            <Link href="/download">
              <Button size="lg" variant="outline" className="border-white text-white hover:bg-white hover:text-primary-600">
                Download Apps
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}