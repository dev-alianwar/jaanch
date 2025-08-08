import { notFound } from 'next/navigation';
import { getRequestConfig } from 'next-intl/server';
import { getTranslations } from './lib/translations';

// Can be imported from a shared config
const locales = ['en', 'ur'];

export default getRequestConfig(async ({ locale }) => {
  // Validate that the incoming `locale` parameter is valid
  if (!locales.includes(locale as any)) notFound();

  try {
    const messages = await getTranslations(locale);
    return { messages };
  } catch (error) {
    // Fallback to static files if API fails
    return {
      messages: (await import(`../locales/${locale}.json`)).default
    };
  }
});