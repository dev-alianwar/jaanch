import { Metadata } from 'next';
import Link from 'next/link';
import { Smartphone, Monitor, Download, CheckCircle, Shield, Users } from 'lucide-react';
import { Button } from '@/theme/components';
import { MobileAppScreenshot, DesktopAppScreenshot } from '@/components/AppScreenshots';
import TransparentHeader from '@/components/layout/TransparentHeader';
export const metadata: Metadata = {
    title: 'Download Apps - Fraud Detection System',
    description: 'Download our mobile and desktop applications for comprehensive fraud detection across all platforms.',
};

export default function DownloadPage() {

    return (
        <>
            {/* Transparent Header overlaying the hero section */}
            <TransparentHeader variant="light" />

            <div className="min-h-screen -mt-16">{/* Negative margin to account for default header */}

                {/* Hero Section */}
                <section className="relative bg-gradient-to-br from-primary-50 via-white to-primary-100 pt-32 pb-24 overflow-hidden">
                    {/* Background Pattern */}
                    <div className="absolute inset-0 opacity-30">
                        <div className="absolute inset-0" style={{
                            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23009933' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
                        }}></div>
                    </div>

                    {/* Floating Elements */}
                    <div className="absolute top-20 left-10 w-20 h-20 bg-primary-200 rounded-full opacity-20 animate-pulse"></div>
                    <div className="absolute top-40 right-20 w-16 h-16 bg-primary-300 rounded-full opacity-30 animate-pulse delay-1000"></div>
                    <div className="absolute bottom-20 left-1/4 w-12 h-12 bg-primary-400 rounded-full opacity-25 animate-pulse delay-2000"></div>

                    <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="text-center">
                            <div className="mb-6">
                                <span className="inline-flex items-center px-4 py-2 bg-primary-50 text-primary-700 rounded-full text-sm font-semibold border border-primary-200">
                                    📱 Mobile & Web Apps
                                </span>
                            </div>
                            <h1 className="text-5xl md:text-7xl font-bold mb-6 text-gray-900 leading-tight">
                                Fraud protection
                                <span className="block text-primary-600">in your pocket</span>
                            </h1>
                            <p className="text-xl md:text-2xl mb-12 max-w-4xl mx-auto text-gray-600 leading-relaxed">
                                Dedicated apps for customers and businesses. Access real-time fraud detection,
                                customer verification, and business analytics from anywhere.
                            </p>
                            <div className="flex flex-col sm:flex-row gap-6 justify-center max-w-md mx-auto">
                                <Button
                                    size="xl"
                                    variant="primary"
                                    icon={<Download className="h-5 w-5" />}
                                    className="shadow-lg hover:shadow-xl font-semibold"
                                    fullWidth
                                >
                                    Download Apps
                                </Button>
                                <Button
                                    size="xl"
                                    variant="outline"
                                    icon={<Monitor className="h-5 w-5" />}
                                    className="font-semibold"
                                    fullWidth
                                >
                                    Try Web App
                                </Button>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Mobile Apps Section */}
                <section className="py-24 bg-white">
                    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="text-center mb-20">
                            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6 leading-tight">
                                Native mobile apps for
                                <span className="block text-primary-600">every user type</span>
                            </h2>
                            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
                                Beautifully designed apps that put powerful fraud detection tools
                                right at your fingertips, wherever you are.
                            </p>
                        </div>

                        <div className="grid md:grid-cols-2 gap-16 items-center">
                            <div className="space-y-8">
                                <div className="space-y-6">
                                    <div className="flex items-start space-x-4">
                                        <div className="flex-shrink-0 w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                                            <Smartphone className="h-6 w-6 text-primary-600" />
                                        </div>
                                        <div>
                                            <h3 className="text-xl font-bold text-gray-900 mb-2">iOS & Android Native</h3>
                                            <p className="text-gray-600 leading-relaxed">
                                                Built specifically for each platform with native performance and design patterns.
                                            </p>
                                        </div>
                                    </div>

                                    <div className="flex items-start space-x-4">
                                        <div className="flex-shrink-0 w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                                            <CheckCircle className="h-6 w-6 text-primary-600" />
                                        </div>
                                        <div>
                                            <h3 className="text-xl font-bold text-gray-900 mb-2">Real-time Alerts</h3>
                                            <p className="text-gray-600 leading-relaxed">
                                                Instant push notifications for fraud detection and customer verification.
                                            </p>
                                        </div>
                                    </div>

                                    <div className="flex items-start space-x-4">
                                        <div className="flex-shrink-0 w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                                            <Shield className="h-6 w-6 text-primary-600" />
                                        </div>
                                        <div>
                                            <h3 className="text-xl font-bold text-gray-900 mb-2">Offline Support</h3>
                                            <p className="text-gray-600 leading-relaxed">
                                                Continue working even without internet connection with smart sync.
                                            </p>
                                        </div>
                                    </div>
                                </div>

                                <div className="flex flex-col sm:flex-row gap-4 pt-4">
                                    <Button
                                        variant="primary"
                                        icon={<Download className="h-4 w-4" />}
                                        className="flex-1 font-semibold"
                                    >
                                        Download for iOS
                                    </Button>
                                    <Button
                                        variant="outline"
                                        icon={<Download className="h-4 w-4" />}
                                        className="flex-1 font-semibold"
                                    >
                                        Download for Android
                                    </Button>
                                </div>
                            </div>

                            <div className="relative">
                                <div className="bg-gradient-to-br from-gray-50 to-white p-12 rounded-3xl border border-gray-200 shadow-sm">
                                    <div className="flex justify-center space-x-8">
                                        <div className="transform rotate-3 hover:rotate-0 transition-transform duration-300">
                                            <MobileAppScreenshot type="customer" />
                                        </div>
                                        <div className="transform -rotate-3 hover:rotate-0 transition-transform duration-300">
                                            <MobileAppScreenshot type="business" />
                                        </div>
                                    </div>
                                    <div className="text-center mt-8">
                                        <p className="text-gray-600 font-medium">
                                            Customer and Business interfaces
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Web Application Section */}
                <section className="py-20 bg-white">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="text-center mb-16">
                            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                                Web Application
                            </h2>
                            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                                Full-featured web application accessible from any browser
                            </p>
                        </div>

                        <div className="grid md:grid-cols-2 gap-12 items-center">
                            <div className="text-center">
                                <div className="bg-gradient-to-br from-gray-100 to-gray-200 p-8 rounded-2xl">
                                    <h4 className="text-xl font-semibold text-gray-900 mb-6">
                                        Desktop Dashboard
                                    </h4>
                                    <div className="flex justify-center">
                                        <DesktopAppScreenshot />
                                    </div>
                                    <p className="text-gray-600 mt-4">
                                        Full-featured web dashboard interface
                                    </p>
                                </div>
                            </div>

                            <div>
                                <div className="bg-gray-50 p-8 rounded-lg">
                                    <div className="flex items-center mb-6">
                                        <Monitor className="h-12 w-12 text-primary-600 mr-4" />
                                        <div>
                                            <h3 className="text-2xl font-bold text-gray-900">Web Portal</h3>
                                            <p className="text-gray-600">Access from any browser</p>
                                        </div>
                                    </div>

                                    <div className="space-y-4 mb-8">
                                        <div className="flex items-center">
                                            <CheckCircle className="h-5 w-5 text-primary-600 mr-3" />
                                            <span>Advanced analytics dashboard</span>
                                        </div>
                                        <div className="flex items-center">
                                            <CheckCircle className="h-5 w-5 text-primary-600 mr-3" />
                                            <span>Comprehensive reporting tools</span>
                                        </div>
                                        <div className="flex items-center">
                                            <CheckCircle className="h-5 w-5 text-primary-600 mr-3" />
                                            <span>Multi-user management</span>
                                        </div>
                                        <div className="flex items-center">
                                            <CheckCircle className="h-5 w-5 text-primary-600 mr-3" />
                                            <span>API integration tools</span>
                                        </div>
                                    </div>

                                    <Link href="/login">
                                        <Button
                                            size="lg"
                                            variant="primary"
                                            fullWidth
                                            className="shadow-lg"
                                        >
                                            Access Web Portal
                                        </Button>
                                    </Link>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* App Screenshots Gallery */}
                <section className="py-20 bg-white">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="text-center mb-16">
                            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                                See Our Apps in Action
                            </h2>
                            <p className="text-xl text-gray-700 max-w-3xl mx-auto font-medium">
                                Different interfaces for different user roles - all designed for maximum efficiency
                            </p>
                        </div>

                        <div className="grid md:grid-cols-2 gap-12 mb-12 max-w-4xl mx-auto">
                            <div className="text-center">
                                <MobileAppScreenshot type="customer" />
                                <h3 className="text-xl font-bold text-gray-900 mt-6 mb-3">Customer App</h3>
                                <p className="text-gray-700 font-medium">
                                    Track your purchases, view credit status, manage payments, and receive security notifications
                                </p>
                            </div>

                            <div className="text-center">
                                <MobileAppScreenshot type="business" />
                                <h3 className="text-xl font-bold text-gray-900 mt-6 mb-3">Business App</h3>
                                <p className="text-gray-700 font-medium">
                                    Real-time fraud alerts, customer verification tools, risk assessment, and business analytics
                                </p>
                            </div>
                        </div>

                        <div className="text-center">
                            <div className="bg-gradient-to-r from-primary-50 to-primary-100 p-8 rounded-2xl">
                                <h3 className="text-2xl font-bold text-gray-900 mb-4">Ready to Download?</h3>
                                <p className="text-gray-600 mb-6">
                                    Get started with our mobile apps and see the difference real-time fraud detection makes
                                </p>
                                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                                    <Button size="lg" className="bg-primary-600 text-white hover:bg-primary-700">
                                        <Download className="mr-2 h-5 w-5" />
                                        Download for iOS
                                    </Button>
                                    <Button
                                        size="lg"
                                        variant="primary"
                                        icon={<Download className="h-5 w-5" />}
                                    >
                                        Download for Android
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                {/* Features Section */}
                <section className="py-20">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="text-center mb-16">
                            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                                Why Choose Our Apps?
                            </h2>
                            <p className="text-xl text-gray-700 max-w-3xl mx-auto font-medium">
                                Built with security, performance, and user experience in mind
                            </p>
                        </div>

                        <div className="grid md:grid-cols-3 gap-8">
                            <div className="text-center">
                                <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                                    <Shield className="h-8 w-8 text-primary-600" />
                                </div>
                                <h3 className="text-xl font-bold text-gray-900 mb-2">
                                    Bank-Level Security
                                </h3>
                                <p className="text-gray-700 font-medium">
                                    End-to-end encryption and secure authentication protocols
                                </p>
                            </div>

                            <div className="text-center">
                                <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                                    <Users className="h-8 w-8 text-primary-600" />
                                </div>
                                <h3 className="text-xl font-bold text-gray-900 mb-2">
                                    Multi-User Support
                                </h3>
                                <p className="text-gray-700 font-medium">
                                    Role-based access control for teams and organizations
                                </p>
                            </div>

                            <div className="text-center">
                                <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                                    <Download className="h-8 w-8 text-primary-600" />
                                </div>
                                <h3 className="text-xl font-bold text-gray-900 mb-2">
                                    Always Updated
                                </h3>
                                <p className="text-gray-700 font-medium">
                                    Automatic updates ensure you always have the latest features
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
                                🚀 Get Started Today
                            </span>
                        </div>
                        <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white leading-tight">
                            Ready to protect your business?
                        </h2>
                        <p className="text-xl mb-12 max-w-2xl mx-auto text-primary-100 leading-relaxed">
                            Join thousands of businesses already using our fraud detection system
                            to prevent losses and make smarter decisions.
                        </p>
                        <div className="flex flex-col sm:flex-row gap-6 justify-center max-w-md mx-auto">
                            <Link href="/register" className="flex-1">
                                <Button
                                    size="xl"
                                    variant="secondary"
                                    className="shadow-xl font-semibold w-full"
                                >
                                    Start Free Trial
                                </Button>
                            </Link>
                            <Link href="/features" className="flex-1">
                                <Button
                                    size="xl"
                                    variant="outline"
                                    className="border-2 border-white text-white hover:bg-white hover:text-primary-700 font-semibold w-full"
                                >
                                    View Features
                                </Button>
                            </Link>
                        </div>
                    </div>
                </section>
            </div>
        </>
    );
}