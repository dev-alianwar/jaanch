import type { Locale } from './locale';

type Messages = Record<string, any>;

export async function getTranslations(locale: Locale): Promise<Messages> {
  try {
    const messages = await import(`@/locales/${locale}.json`);
    return messages.default;
  } catch (error) {
    console.error(`Failed to load translations for locale: ${locale}`, error);
    // Fallback to English
    const fallback = await import('@/locales/en.json');
    return fallback.default;
  }
}

export function createTranslator(messages: Messages) {
  return (key: string, params?: Record<string, string>): string => {
    const keys = key.split('.');
    let value: any = messages;
    
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
}
