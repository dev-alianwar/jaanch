import api from '@/services/api';

let translationCache: { [locale: string]: any } = {};

export async function getTranslations(locale: string) {
  // Check cache first
  if (translationCache[locale]) {
    return translationCache[locale];
  }

  try {
    const response = await api.get(`/translations/locale/${locale}`);
    const translations = response.data.translations;
    
    // Cache the translations
    translationCache[locale] = translations;
    
    return translations;
  } catch (error) {
    console.error(`Failed to fetch translations for locale ${locale}:`, error);
    
    // Return fallback translations
    return getFallbackTranslations(locale);
  }
}

function getFallbackTranslations(locale: string) {
  const fallback = {
    common: {
      loading: locale === 'ur' ? 'لوڈ ہو رہا ہے...' : 'Loading...',
      submit: locale === 'ur' ? 'جمع کریں' : 'Submit',
      cancel: locale === 'ur' ? 'منسوخ' : 'Cancel',
    },
    navigation: {
      home: locale === 'ur' ? 'ہوم' : 'Home',
      login: locale === 'ur' ? 'لاگ ان' : 'Login',
      register: locale === 'ur' ? 'رجسٹر' : 'Register',
    },
    auth: {
      signIn: locale === 'ur' ? 'اپنے اکاؤنٹ میں سائن ان کریں' : 'Sign in to your account',
      email: locale === 'ur' ? 'ای میل ایڈریس' : 'Email address',
      password: locale === 'ur' ? 'پاس ورڈ' : 'Password',
    }
  };
  
  return fallback;
}

// Clear cache when translations are updated
export function clearTranslationCache() {
  translationCache = {};
}