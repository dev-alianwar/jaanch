'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useTranslationFallback } from '@/components/TranslationProvider';
import { LOCALE_COOKIE } from '@/lib/locale';
import { Globe } from 'lucide-react';

const LanguageSwitcher: React.FC = () => {
  const router = useRouter();
  const { locale } = useTranslationFallback();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'ur', name: 'اردو', flag: '🇵🇰' },
  ];

  const currentLanguage = languages.find(lang => lang.code === locale) || languages[0];

  const switchLanguage = (newLocale: string) => {
    // Set cookie
    document.cookie = `${LOCALE_COOKIE}=${newLocale}; path=/; max-age=31536000; SameSite=Lax`;
    
    // Close dropdown
    setIsOpen(false);
    
    // Refresh the page to apply new locale
    router.refresh();
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors"
        style={{ backgroundColor: '#ffffff', color: '#374151' }}
      >
        <Globe className="w-4 h-4" />
        <span>{currentLanguage.flag}</span>
        <span>{currentLanguage.name}</span>
        <svg
          className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 rounded-lg shadow-lg border border-gray-200 overflow-hidden z-50" style={{ backgroundColor: '#ffffff' }}>
          {languages.map((lang) => (
            <button
              key={lang.code}
              onClick={() => switchLanguage(lang.code)}
              className={`w-full flex items-center gap-3 px-4 py-3 text-sm font-medium transition-colors ${
                locale === lang.code
                  ? 'bg-primary-50'
                  : 'hover:bg-gray-50'
              }`}
              style={{ 
                color: locale === lang.code ? '#008529' : '#374151',
                backgroundColor: locale === lang.code ? '#f0fdf4' : 'transparent'
              }}
            >
              <span className="text-xl">{lang.flag}</span>
              <span>{lang.name}</span>
              {locale === lang.code && (
                <svg className="w-4 h-4 ml-auto" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default LanguageSwitcher;