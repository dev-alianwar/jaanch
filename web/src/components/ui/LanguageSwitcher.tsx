'use client';

import React from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useTranslationFallback } from '@/components/TranslationProvider';

const LanguageSwitcher: React.FC = () => {
  const router = useRouter();
  const pathname = usePathname();
  const { locale } = useTranslationFallback();

  const switchLanguage = (newLocale: string) => {
    // Remove the current locale from the pathname
    const pathWithoutLocale = pathname.replace(`/${locale}`, '');
    // Navigate to the new locale
    router.push(`/${newLocale}${pathWithoutLocale}`);
  };

  return (
    <div className="flex items-center space-x-2">
      <button
        onClick={() => switchLanguage('en')}
        className={`px-2 py-1 text-sm rounded ${
          locale === 'en'
            ? 'bg-primary-500 text-white'
            : 'text-gray-600 hover:text-gray-900'
        }`}
      >
        EN
      </button>
      <button
        onClick={() => switchLanguage('ur')}
        className={`px-2 py-1 text-sm rounded ${
          locale === 'ur'
            ? 'bg-primary-500 text-white'
            : 'text-gray-600 hover:text-gray-900'
        }`}
      >
        اردو
      </button>
    </div>
  );
};

export default LanguageSwitcher;