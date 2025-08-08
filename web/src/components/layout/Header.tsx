'use client';

import React from 'react';
import Link from 'next/link';
import { useTranslations } from 'next-intl';
import { useAuth } from '@/contexts/AuthContext';
import Button from '@/components/ui/Button';
import LanguageSwitcher from '@/components/ui/LanguageSwitcher';

const Header: React.FC = () => {
  const { user, logout } = useAuth();
  const t = useTranslations('navigation');

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-gray-900">
              InstallmentGuard
            </Link>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            <Link href="/" className="text-gray-500 hover:text-gray-900">
              {t('home')}
            </Link>
            <Link href="/features" className="text-gray-500 hover:text-gray-900">
              {t('features')}
            </Link>
            <Link href="/download" className="text-gray-500 hover:text-gray-900">
              {t('download')}
            </Link>
            {user && (
              <Link href="/app" className="text-gray-500 hover:text-gray-900">
                {t('dashboard')}
              </Link>
            )}
          </nav>
          
          <div className="flex items-center space-x-4">
            <LanguageSwitcher />
            {user ? (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-700">
                  Welcome, {user.firstName}
                </span>
                <Button variant="outline" size="sm" onClick={logout}>
                  {t('logout')}
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link href="/login">
                  <Button variant="outline" size="sm">
                    {t('login')}
                  </Button>
                </Link>
                <Link href="/register">
                  <Button size="sm">
                    {t('register')}
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

export default Header;