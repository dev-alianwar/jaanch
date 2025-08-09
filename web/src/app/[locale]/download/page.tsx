import { Metadata } from 'next';
import Link from 'next/link';
import { Smartphone, Monitor, Download, CheckCircle, Shield, Users } from 'lucide-react';
import Button from '@/components/ui/Button';
import { MobileAppScreenshot, DesktopAppScreenshot } from '@/components/AppScreenshots';
export const metadata: Metadata = {
    title: 'Download Apps - Fraud Detection System',
    description: 'Download our mobile and desktop applications for comprehensive fraud detection across all platforms.',
};

export default function DownloadPage() {

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Hero Section */}
            <section className="relative text-white" style={{ background: 'linear-gradient(to right, #008529, #005515)' }}>
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
                    <div className="text-center">
                        <h1 className="text-4xl md:text-6xl font-bold mb-6">
                            Download Our Apps
                        </h1>
                        <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
                            Dedicated apps for customers and businesses - access fraud protection tools from anywhere
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <Button size="lg" className="bg-white text-primary-600 hover:bg-gray-100">
                                <Download className="mr-2 h-5 w-5" />
                                Download Mobile App
                            </Button>
                            <Button
                                size="lg"
                                variant="outline"
                                className="border-white text-white hover:bg-white hover:text-primary-600"
                            >
                                <Monitor className="mr-2 h-5 w-5" />
                                Web Application
                            </Button>
                        </div>
                    </div>
                </div>
            </section>

            {/* Mobile Apps Section */}
            <section className="py-20">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                            Mobile Applications
                        </h2>
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Stay connected and monitor fraud detection on the go with our native mobile apps
                        </p>
                    </div>

                    <div className="grid md:grid-cols-2 gap-12 items-center">
                        <div>
                            <div className="bg-white p-8 rounded-lg shadow-lg border">
                                <div className="flex items-center mb-6">
                                    <Smartphone className="h-12 w-12 text-primary-600 mr-4" />
                                    <div>
                                        <h3 className="text-2xl font-bold text-gray-900">iOS & Android</h3>
                                        <p className="text-gray-600">Native apps for all devices</p>
                                    </div>
                                </div>

                                <div className="space-y-4 mb-8">
                                    <div className="flex items-center">
                                        <CheckCircle className="h-5 w-5 text-primary-600 mr-3" />
                                        <span>Real-time fraud alerts</span>
                                    </div>
                                    <div className="flex items-center">
                                        <CheckCircle className="h-5 w-5 text-primary-600 mr-3" />
                                        <span>Customer verification tools</span>
                                    </div>
                                    <div className="flex items-center">
                                        <CheckCircle className="h-5 w-5 text-primary-600 mr-3" />
                                        <span>Business dashboard access</span>
                                    </div>
                                    <div className="flex items-center">
                                        <CheckCircle className="h-5 w-5 text-primary-600 mr-3" />
                                        <span>Offline mode support</span>
                                    </div>
                                </div>

                                <div className="flex flex-col sm:flex-row gap-4">
                                    <Button className="flex-1">
                                        <Download className="mr-2 h-4 w-4" />
                                        Download for iOS
                                    </Button>
                                    <Button className="flex-1">
                                        <Download className="mr-2 h-4 w-4" />
                                        Download for Android
                                    </Button>
                                </div>
                            </div>
                        </div>

                        <div className="text-center">
                            <div className="bg-gradient-to-br from-gray-100 to-gray-200 p-8 rounded-2xl">
                                <h4 className="text-xl font-semibold text-gray-900 mb-6">
                                    App Screenshots
                                </h4>
                                <div className="flex justify-center space-x-4">
                                    <MobileAppScreenshot type="customer" />
                                    <MobileAppScreenshot type="business" />
                                </div>
                                <p className="text-gray-600 mt-4">
                                    Customer and Business mobile interfaces
                                </p>
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
                                    <Button size="lg" className="w-full">
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
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Different interfaces for different user roles - all designed for maximum efficiency
                        </p>
                    </div>

                    <div className="grid md:grid-cols-2 gap-12 mb-12 max-w-4xl mx-auto">
                        <div className="text-center">
                            <MobileAppScreenshot type="customer" />
                            <h3 className="text-xl font-semibold text-gray-900 mt-6 mb-3">Customer App</h3>
                            <p className="text-gray-600">
                                Track your purchases, view credit status, manage payments, and receive security notifications
                            </p>
                        </div>

                        <div className="text-center">
                            <MobileAppScreenshot type="business" />
                            <h3 className="text-xl font-semibold text-gray-900 mt-6 mb-3">Business App</h3>
                            <p className="text-gray-600">
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
                                <Button size="lg" className="bg-primary-600 text-white hover:bg-primary-700">
                                    <Download className="mr-2 h-5 w-5" />
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
                        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                            Built with security, performance, and user experience in mind
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-8">
                        <div className="text-center">
                            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                                <Shield className="h-8 w-8 text-primary-600" />
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                Bank-Level Security
                            </h3>
                            <p className="text-gray-600">
                                End-to-end encryption and secure authentication protocols
                            </p>
                        </div>

                        <div className="text-center">
                            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                                <Users className="h-8 w-8 text-primary-600" />
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                Multi-User Support
                            </h3>
                            <p className="text-gray-600">
                                Role-based access control for teams and organizations
                            </p>
                        </div>

                        <div className="text-center">
                            <div className="bg-primary-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                                <Download className="h-8 w-8 text-primary-600" />
                            </div>
                            <h3 className="text-xl font-semibold text-gray-900 mb-2">
                                Always Updated
                            </h3>
                            <p className="text-gray-600">
                                Automatic updates ensure you always have the latest features
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="text-white py-20" style={{ backgroundColor: '#008529' }}>
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
                    <h2 className="text-3xl md:text-4xl font-bold mb-4">
                        Ready to Get Started?
                    </h2>
                    <p className="text-xl mb-8 max-w-2xl mx-auto">
                        Download our apps today and start protecting your business from fraud
                    </p>
                    <div className="flex flex-col sm:flex-row gap-4 justify-center">
                        <Link href="/register">
                            <Button size="lg" className="bg-white text-primary-600 hover:bg-gray-100">
                                Start Free Trial
                            </Button>
                        </Link>
                        <Link href="/features">
                            <Button
                                size="lg"
                                variant="outline"
                                className="border-white text-white hover:bg-white hover:text-primary-600"
                            >
                                View All Features
                            </Button>
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    );
}