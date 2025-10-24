'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import Button from '@/components/ui/Button';
import LanguageSwitcher from '@/components/ui/LanguageSwitcher';

interface HeaderClientProps {
  translations: {
    login: string;
    register: string;
    logout: string;
  };
}

export default function HeaderClient({ translations }: HeaderClientProps) {
  const { user, logout } = useAuth();

  return (
    <div className="flex items-center space-x-4">
      <LanguageSwitcher />
      {user ? (
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-700">
            Welcome, {user.firstName}
          </span>
          <Button variant="outline" size="sm" onClick={logout}>
            {translations.logout}
          </Button>
        </div>
      ) : (
        <div className="flex items-center space-x-2">
          <Link href="/login">
            <Button variant="outline" size="sm">
              {translations.login}
            </Button>
          </Link>
          <Link href="/register">
            <Button size="sm">
              {translations.register}
            </Button>
          </Link>
        </div>
      )}
    </div>
  );
}
