import { cookies, headers } from 'next/headers';
import { LOCALE_COOKIE, defaultLocale, locales, type Locale } from './locale';

export async function getLocale(): Promise<Locale> {
  // Try to get from headers first (set by middleware)
  const headersList = await headers();
  const localeFromHeader = headersList.get('x-locale');
  
  if (localeFromHeader && locales.includes(localeFromHeader as Locale)) {
    return localeFromHeader as Locale;
  }

  // Fallback to cookie
  const cookieStore = await cookies();
  const localeCookie = cookieStore.get(LOCALE_COOKIE);
  
  if (localeCookie && locales.includes(localeCookie.value as Locale)) {
    return localeCookie.value as Locale;
  }

  return defaultLocale;
}
