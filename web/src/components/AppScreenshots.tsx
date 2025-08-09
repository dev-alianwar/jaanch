import React from 'react';
import { Shield, Users, TrendingUp, Bell, Search, Settings } from 'lucide-react';

export const MobileAppScreenshot: React.FC<{ type: 'customer' | 'business' }> = ({ type }) => {
  const getScreenContent = () => {
    switch (type) {
      case 'customer':
        return (
          <div className="bg-white h-full flex flex-col">
            {/* Header */}
            <div className="bg-primary-600 text-white p-4 rounded-t-2xl">
              <div className="flex items-center justify-between">
                <h1 className="text-lg font-bold">InstallmentGuard</h1>
                <Bell className="h-5 w-5" />
              </div>
              <p className="text-primary-100 text-sm mt-1">Customer Portal</p>
            </div>
            
            {/* Content */}
            <div className="flex-1 p-4 space-y-4">
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2">Credit Status</h3>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                  <span className="text-sm text-gray-600">Good Standing</span>
                </div>
              </div>
              
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2">Recent Purchases</h3>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Electronics Store</span>
                    <span className="text-green-600">$299</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Furniture Shop</span>
                    <span className="text-green-600">$599</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2">Payment Schedule</h3>
                <div className="text-sm text-gray-600">
                  Next payment: $150 due in 5 days
                </div>
              </div>
            </div>
          </div>
        );
      
      case 'business':
        return (
          <div className="bg-white h-full flex flex-col">
            {/* Header */}
            <div className="bg-primary-600 text-white p-4 rounded-t-2xl">
              <div className="flex items-center justify-between">
                <h1 className="text-lg font-bold">InstallmentGuard</h1>
                <Search className="h-5 w-5" />
              </div>
              <p className="text-primary-100 text-sm mt-1">Business Dashboard</p>
            </div>
            
            {/* Content */}
            <div className="flex-1 p-4 space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-red-50 p-3 rounded-lg text-center">
                  <div className="text-2xl font-bold text-red-600">3</div>
                  <div className="text-xs text-red-600">High Risk</div>
                </div>
                <div className="bg-yellow-50 p-3 rounded-lg text-center">
                  <div className="text-2xl font-bold text-yellow-600">12</div>
                  <div className="text-xs text-yellow-600">Medium Risk</div>
                </div>
              </div>
              
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2">Recent Alerts</h3>
                <div className="space-y-2">
                  <div className="flex items-center text-sm">
                    <div className="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                    <span>Suspicious pattern detected</span>
                  </div>
                  <div className="flex items-center text-sm">
                    <div className="w-2 h-2 bg-yellow-500 rounded-full mr-2"></div>
                    <span>Multiple applications</span>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-50 p-4 rounded-lg">
                <h3 className="font-semibold text-gray-900 mb-2">Customer Verification</h3>
                <div className="flex space-x-2">
                  <button className="flex-1 bg-primary-600 text-white py-2 px-3 rounded text-sm">
                    Verify
                  </button>
                  <button className="flex-1 bg-gray-200 text-gray-700 py-2 px-3 rounded text-sm">
                    Flag
                  </button>
                </div>
              </div>
            </div>
          </div>
        );
      

    }
  };

  return (
    <div className="relative">
      {/* Phone Frame */}
      <div className="w-64 h-96 bg-gray-900 rounded-3xl p-2 shadow-2xl">
        <div className="w-full h-full bg-gray-100 rounded-2xl overflow-hidden relative">
          {/* Notch */}
          <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-20 h-6 bg-gray-900 rounded-b-xl z-10"></div>
          
          {/* Screen Content */}
          <div className="w-full h-full pt-6">
            {getScreenContent()}
          </div>
        </div>
      </div>
    </div>
  );
};

export const DesktopAppScreenshot: React.FC = () => {
  return (
    <div className="relative">
      {/* Desktop Frame */}
      <div className="w-96 h-64 bg-gray-900 rounded-lg p-1 shadow-2xl">
        <div className="w-full h-full bg-white rounded-md overflow-hidden">
          {/* Title Bar */}
          <div className="bg-gray-100 px-4 py-2 flex items-center justify-between border-b">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            </div>
            <div className="text-sm text-gray-600">InstallmentGuard Dashboard</div>
            <div></div>
          </div>
          
          {/* Content */}
          <div className="p-4 h-full">
            <div className="grid grid-cols-4 gap-3 mb-4">
              <div className="bg-primary-50 p-2 rounded text-center">
                <Shield className="h-6 w-6 text-primary-600 mx-auto mb-1" />
                <div className="text-xs text-primary-600">Security</div>
              </div>
              <div className="bg-blue-50 p-2 rounded text-center">
                <Users className="h-6 w-6 text-blue-600 mx-auto mb-1" />
                <div className="text-xs text-blue-600">Users</div>
              </div>
              <div className="bg-green-50 p-2 rounded text-center">
                <TrendingUp className="h-6 w-6 text-green-600 mx-auto mb-1" />
                <div className="text-xs text-green-600">Analytics</div>
              </div>
              <div className="bg-purple-50 p-2 rounded text-center">
                <Settings className="h-6 w-6 text-purple-600 mx-auto mb-1" />
                <div className="text-xs text-purple-600">Settings</div>
              </div>
            </div>
            
            <div className="bg-gray-50 p-3 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-2 text-sm">Fraud Detection Overview</h3>
              <div className="space-y-1">
                <div className="flex justify-between text-xs">
                  <span>Total Scans Today</span>
                  <span className="font-semibold">1,247</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Fraud Detected</span>
                  <span className="font-semibold text-red-600">23</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span>Success Rate</span>
                  <span className="font-semibold text-green-600">98.2%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};