import React from 'react';
import Link from 'next/link';
import { getTranslations, createTranslator } from '@/lib/getTranslations';
import type { Locale } from '@/lib/locale';
import HeaderClient from './HeaderClient';

interface HeaderProps {
  locale: Locale;
}

export default async function Header({ locale }: HeaderProps) {
  const messages = await getTranslations(locale);
  const t = createTranslator(messages);
  
  const appName = process.env.NEXT_PUBLIC_APP_NAME || t('app.name');

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold text-gray-900">
              {appName}
            </Link>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            <Link href="/" className="text-gray-500 hover:text-gray-900">
              {t('navigation.home')}
            </Link>
            <Link href="/features" className="text-gray-500 hover:text-gray-900">
              {t('navigation.features')}
            </Link>
            <Link href="/download" className="text-gray-500 hover:text-gray-900">
              {t('navigation.download')}
            </Link>
          </nav>
          
          <HeaderClient
            translations={{
              login: t('navigation.login'),
              register: t('navigation.register'),
              logout: t('navigation.logout'),
            }}
          />
        </div>
      </div>
    </header>
  );
}