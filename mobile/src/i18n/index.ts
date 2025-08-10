import { I18n } from 'i18n-js';
import * as RNLocalize from 'react-native-localize';
import { apiService } from '../services/apiService';
import en from './locales/en.json';
import ur from './locales/ur.json';

const i18n = new I18n({
  en,
  ur,
});

// Set the locale once at the beginning of your app.
i18n.locale = RNLocalize.getLocales()[0].languageCode;

// When a value is missing from a language it'll fallback to another language with the key present.
i18n.enableFallback = true;
i18n.defaultLocale = 'en';

// Function to load translations from API
export const loadTranslationsFromAPI = async (locale: string) => {
  try {
    const response = await apiService.get(`/translations/locale/${locale}`);
    const translations = response.data.translations;
    
    // Update i18n with API translations
    i18n.store(locale, translations);
    
    return translations;
  } catch (error) {
    // Silently fail and use static translations
    console.warn(`API translations not available for ${locale}, using static translations`);
    return null;
  }
};

// Initialize translations from API (optional)
export const initializeTranslations = async () => {
  try {
    const currentLocale = i18n.locale;
    await loadTranslationsFromAPI(currentLocale);
    
    // Also load the other locale for quick switching
    const otherLocale = currentLocale === 'en' ? 'ur' : 'en';
    await loadTranslationsFromAPI(otherLocale);
  } catch (error) {
    // Silently fail and continue with static translations
    console.warn('API translations not available, using static translations');
  }
};

export default i18n;