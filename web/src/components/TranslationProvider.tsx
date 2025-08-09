'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { getTranslations } from '@/lib/translations';

interface TranslationContextType {
  translations: any;
  loading: boolean;
  locale: string;
  t: (key: string, params?: any) => string;
}

const TranslationContext = createContext<TranslationContextType | undefined>(undefined);

export const useTranslationFallback = () => {
  const context = useContext(TranslationContext);
  if (context === undefined) {
    throw new Error('useTranslationFallback must be used within a TranslationProvider');
  }
  return context;
};

interface TranslationProviderProps {
  children: React.ReactNode;
  locale: string;
  initialMessages?: any;
}

export const TranslationProvider: React.FC<TranslationProviderProps> = ({
  children,
  locale,
  initialMessages
}) => {
  const [translations, setTranslations] = useState(initialMessages || {});
  const [loading, setLoading] = useState(!initialMessages);

  useEffect(() => {
    if (!initialMessages) {
      loadTranslations();
    }
  }, [locale, initialMessages]);

  const loadTranslations = async () => {
    try {
      setLoading(true);
      const messages = await getTranslations(locale);
      setTranslations(messages);
    } catch (error) {
      console.error('Failed to load translations:', error);
    } finally {
      setLoading(false);
    }
  };

  const t = (key: string, params?: any) => {
    const keys = key.split('.');
    let value = translations;
    
    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        return key; // Return key if translation not found
      }
    }
    
    if (typeof value === 'string') {
      // Simple parameter replacement
      if (params) {
        return value.replace(/\{(\w+)\}/g, (match, paramKey) => {
          return params[paramKey] || match;
        });
      }
      return value;
    }
    
    return key;
  };

  const value = {
    translations,
    loading,
    locale,
    t
  };

  return (
    <TranslationContext.Provider value={value}>
      {children}
    </TranslationContext.Provider>
  );
};