import { notFound } from 'next/navigation';
import { getRequestConfig } from 'next-intl/server';
import { getTranslations } from './lib/translations';

// Can be imported from a shared config
const locales = ['en', 'ur'];

function getFallbackMessages(locale: string) {
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
      logout: locale === 'ur' ? 'لاگ آؤٹ' : 'Logout',
    },
    auth: {
      signIn: locale === 'ur' ? 'اپنے اکاؤنٹ میں سائن ان کریں' : 'Sign in to your account',
      email: locale === 'ur' ? 'ای میل ایڈریس' : 'Email address',
      password: locale === 'ur' ? 'پاس ورڈ' : 'Password',
      enterEmail: locale === 'ur' ? 'اپنا ای میل درج کریں' : 'Enter your email',
      enterPassword: locale === 'ur' ? 'اپنا پاس ورڈ درج کریں' : 'Enter your password',
      signInButton: locale === 'ur' ? 'سائن ان' : 'Sign in',
      createNew: locale === 'ur' ? 'نیا اکاؤنٹ بنائیں' : 'create a new account',
      forgotPassword: locale === 'ur' ? 'اپنا پاس ورڈ بھول گئے؟' : 'Forgot your password?',
    }
  };
  
  return fallback;
}

export default getRequestConfig(async ({ locale }) => {
  // Validate that the incoming `locale` parameter is valid
  if (!locale || !locales.includes(locale)) notFound();

  // At this point, locale is guaranteed to be a valid string
  const validLocale = locale as string;

  // Always try static files first for reliability
  try {
    const messages = (await import(`./locales/${validLocale}.json`)).default;
    return { 
      messages,
      locale: validLocale
    };
  } catch {
    console.warn(`Failed to load static translations for ${validLocale}, trying API`);
    
    // Fallback to API
    try {
      const messages = await getTranslations(validLocale);
      return { 
        messages,
        locale: validLocale
      };
    } catch {
      console.warn(`Failed to load translations from API for ${validLocale}, using minimal fallback`);
      // Return minimal fallback
      return {
        messages: getFallbackMessages(validLocale),
        locale: validLocale
      };
    }
  }
});