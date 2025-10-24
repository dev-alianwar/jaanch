'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/theme/components';
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
          <span className={`text-sm ${textColor}`}>
            Welcome, {user.firstName}
          </span>
          <Button 
            variant="outline" 
            size="sm" 
            onClick={logout}
            className={variant === 'dark' ? 'border-white text-white hover:bg-white hover:text-gray-900' : ''}
          >
            {translations.logout}
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
              {translations.login}
            </Button>
          </Link>
          <Link href="/register">
            <Button 
              size="sm"
              variant={variant === 'dark' ? 'secondary' : 'primary'}
              className="font-semibold"
            >
              {translations.register}
            </Button>
          </Link>
        </div>
      )}
    </div>
  );
}
