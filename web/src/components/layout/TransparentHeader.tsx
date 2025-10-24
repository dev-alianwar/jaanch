import React from 'react';
import Link from 'next/link';
import { getTranslations, createTranslator } from '@/lib/getTranslations';
import type { Locale } from '@/lib/locale';
import TransparentHeaderClient from './TransparentHeaderClient';

interface TransparentHeaderProps {
  variant?: 'light' | 'dark';
  locale: Locale;
}

export default async function TransparentHeader({ variant = 'light', locale }: TransparentHeaderProps) {
  const messages = await getTranslations(locale);
  const t = createTranslator(messages);
  
  const appName = process.env.NEXT_PUBLIC_APP_NAME || t('app.name');
  const textColor = variant === 'dark' ? 'text-white' : 'text-gray-900';
  const hoverColor = variant === 'dark' ? 'hover:text-gray-200' : 'hover:text-gray-600';
  const logoColor = variant === 'dark' ? 'text-white' : 'text-gray-900';

  return (
    <header className="absolute top-0 left-0 right-0 z-50 bg-transparent">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          <div className="flex items-center">
            <Link href="/" className={`text-xl font-bold ${logoColor}`}>
              {appName}
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
          </nav>
          
          <TransparentHeaderClient
            variant={variant}
            locale={locale}
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