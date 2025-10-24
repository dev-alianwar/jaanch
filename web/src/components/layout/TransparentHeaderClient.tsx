'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import LanguageSwitcher from '@/components/ui/LanguageSwitcher';

interface TransparentHeaderClientProps {
  variant: 'light' | 'dark';
  locale: string;
  translations: {
    login: string;
    register: string;
    logout: string;
  };
}

export default function TransparentHeaderClient({ variant, locale, translations }: TransparentHeaderClientProps) {
  const { user, logout } = useAuth();

  const textColor = variant === 'dark' ? 'text-white' : 'text-gray-900';

  return (
    <div className="flex items-center space-x-4">
      <LanguageSwitcher />
      {user ? (
        <div className="flex items-center space-x-4">
          <span className={`text-sm font-medium ${textColor}`}>
            Welcome, {user.firstName}
          </span>
          <button 
            onClick={logout}
            className={`px-4 py-2 text-sm font-semibold rounded-lg transition-all duration-200 ${
              variant === 'dark' 
                ? 'border-2 border-white text-white hover:bg-white hover:text-primary-700' 
                : 'border-2 border-primary-700 text-primary-700 hover:bg-primary-700 hover:text-white'
            }`}
          >
            {translations.logout}
          </button>
        </div>
      ) : (
        <div className="flex items-center space-x-3">
          <Link href="/login">
            <button 
              className="px-4 py-2 text-sm font-semibold rounded-lg transition-all duration-200 hover:bg-white hover:bg-opacity-20"
              style={{ color: variant === 'dark' ? '#ffffff' : '#374151' }}
            >
              {translations.login}
            </button>
          </Link>
          <Link href="/register">
            <button 
              className="px-4 py-2 text-sm font-bold rounded-lg shadow-lg transition-all duration-200"
              style={{
                backgroundColor: variant === 'dark' ? '#ffffff' : '#008529',
                color: variant === 'dark' ? '#006b1f' : '#ffffff'
              }}
            >
              {translations.register}
            </button>
          </Link>
        </div>
      )}
    </div>
  );
}
