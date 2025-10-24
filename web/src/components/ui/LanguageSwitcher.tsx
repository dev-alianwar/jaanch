'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { useTranslationFallback } from '@/components/TranslationProvider';
import { LOCALE_COOKIE } from '@/lib/locale';

const LanguageSwitcher: React.FC = () => {
  const router = useRouter();
  const { locale } = useTranslationFallback();

  const switchLanguage = (newLocale: string) => {
    // Set cookie
    document.cookie = `${LOCALE_COOKIE}=${newLocale}; path=/; max-age=31536000; SameSite=Lax`;
    
    // Refresh the page to apply new locale
    router.refresh();
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