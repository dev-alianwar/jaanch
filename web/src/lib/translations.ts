import api from '@/services/api';

let translationCache: { [locale: string]: Record<string, unknown> } = {};

export async function getTranslations(locale: string) {
  // Check cache first
  if (translationCache[locale]) {
    return translationCache[locale];
  }

  try {
    // Add timeout for API call
    const response = await api.get(`/translations/locale/${locale}`, {
      timeout: 5000 // 5 second timeout
    });
    const translations = response.data.translations;
    
    // Cache the translations
    translationCache[locale] = translations;
    
    return translations;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    console.warn(`Failed to fetch translations for locale ${locale}, using fallback:`, errorMessage);
    
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
      save: locale === 'ur' ? 'محفوظ کریں' : 'Save',
      delete: locale === 'ur' ? 'حذف کریں' : 'Delete',
      edit: locale === 'ur' ? 'ترمیم' : 'Edit',
    },
    navigation: {
      home: locale === 'ur' ? 'ہوم' : 'Home',
      features: locale === 'ur' ? 'خصوصیات' : 'Features',
      download: locale === 'ur' ? 'ڈاؤن لوڈ' : 'Download',
      dashboard: locale === 'ur' ? 'ڈیش بورڈ' : 'Dashboard',
      login: locale === 'ur' ? 'لاگ ان' : 'Login',
      register: locale === 'ur' ? 'رجسٹر' : 'Register',
      logout: locale === 'ur' ? 'لاگ آؤٹ' : 'Logout',
    },
    auth: {
      signIn: locale === 'ur' ? 'اپنے اکاؤنٹ میں سائن ان کریں' : 'Sign in to your account',
      createAccount: locale === 'ur' ? 'اپنا اکاؤنٹ بنائیں' : 'Create your account',
      signInToExisting: locale === 'ur' ? 'اپنے موجودہ اکاؤنٹ میں سائن ان کریں' : 'sign in to your existing account',
      createNew: locale === 'ur' ? 'نیا اکاؤنٹ بنائیں' : 'create a new account',
      email: locale === 'ur' ? 'ای میل ایڈریس' : 'Email address',
      password: locale === 'ur' ? 'پاس ورڈ' : 'Password',
      confirmPassword: locale === 'ur' ? 'پاس ورڈ کی تصدیق' : 'Confirm Password',
      firstName: locale === 'ur' ? 'پہلا نام' : 'First Name',
      lastName: locale === 'ur' ? 'آخری نام' : 'Last Name',
      phone: locale === 'ur' ? 'فون' : 'Phone',
      forgotPassword: locale === 'ur' ? 'اپنا پاس ورڈ بھول گئے؟' : 'Forgot your password?',
      signInButton: locale === 'ur' ? 'سائن ان' : 'Sign in',
      createAccountButton: locale === 'ur' ? 'اکاؤنٹ بنائیں' : 'Create Account',
      enterEmail: locale === 'ur' ? 'اپنا ای میل درج کریں' : 'Enter your email',
      enterPassword: locale === 'ur' ? 'اپنا پاس ورڈ درج کریں' : 'Enter your password',
    },
    home: {
      heroTitle: locale === 'ur' ? 'قسط کی دھوکہ دہی کو روکیں' : 'Stop Installment Fraud',
      heroSubtitle: locale === 'ur' ? 'اس سے پہلے کہ یہ شروع ہو' : 'Before It Starts',
      heroDescription: locale === 'ur' ? 'جدید فراڈ ڈیٹیکشن سسٹم جو متعدد کاروبار میں قسط کی خریداری کو ٹریک کرتا ہے' : 'Advanced fraud detection system that tracks installment purchases across multiple businesses',
      getStartedFree: locale === 'ur' ? 'مفت شروع کریں' : 'Get Started Free',
      downloadApps: locale === 'ur' ? 'ایپس ڈاؤن لوڈ کریں' : 'Download Apps',
    }
  };
  
  return fallback;
}

// Clear cache when translations are updated
export function clearTranslationCache() {
  translationCache = {};
}