'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/theme/components';
import LanguageSwitcher from '@/components/ui/LanguageSwitcher';
import { useTranslationFallback } from '@/components/TranslationProvider';

interface TransparentHeaderProps {
  variant?: 'light' | 'dark';
}

const TransparentHeader: React.FC<TransparentHeaderProps> = ({ variant = 'light' }) => {
  const { user, logout } = useAuth();
  const { t } = useTranslationFallback();

  const textColor = variant === 'dark' ? 'text-white' : 'text-gray-900';
  const hoverColor = variant === 'dark' ? 'hover:text-gray-200' : 'hover:text-gray-600';
  const logoColor = variant === 'dark' ? 'text-white' : 'text-gray-900';

  return (
    <header className="absolute top-0 left-0 right-0 z-50 bg-transparent">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          <div className="flex items-center">
            <Link href="/" className={`text-xl font-bold ${logoColor}`}>
              InstallmentGuard
            </Link>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            <Link href="/" className={`${textColor} ${hoverColor} font-medium transition-colors`}>
              {t('navigation.home')}
            </Link>
            <Link href="/features" className={`${textColor} ${hoverColor} font-medium transition-colors`}>
              {t('navigation.features')}
            </Link>
            <Link href="/download" className={`${textColor} ${hoverColor} font-medium transition-colors`}>
              {t('navigation.download')}
            </Link>
            {user && (
              <Link href="/app" className={`${textColor} ${hoverColor} font-medium transition-colors`}>
                {t('navigation.dashboard')}
              </Link>
            )}
          </nav>
          
          <div className="flex items-center space-x-4">
            <LanguageSwitcher />
            {user ? (
              <div className="flex items-center space-x-4">
                <span className={`text-sm ${textColor}`}>
                  Welcome, {user.firstName}
                </span>
                <Button 
                  variant={variant === 'dark' ? 'outline' : 'outline'} 
                  size="sm" 
                  onClick={logout}
                  className={variant === 'dark' ? 'border-white text-white hover:bg-white hover:text-gray-900' : ''}
                >
                  {t('navigation.logout')}
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <Link href="/login">
                  <Button 
                    variant="ghost" 
                    size="sm"
                    className={variant === 'dark' ? 'text-white hover:bg-white hover:bg-opacity-20' : ''}
                  >
                    {t('navigation.login')}
                  </Button>
                </Link>
                <Link href="/register">
                  <Button 
                    size="sm"
                    variant={variant === 'dark' ? 'secondary' : 'primary'}
                    className="font-semibold"
                  >
                    {t('navigation.register')}
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default TransparentHeader;