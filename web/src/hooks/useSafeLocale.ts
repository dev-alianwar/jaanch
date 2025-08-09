'use client';

import { useLocale } from 'next-intl';
import { usePathname } from 'next/navigation';

export function useSafeLocale(): string {
  try {
    return useLocale();
  } catch (error) {
    console.warn('Locale context not available, extracting from pathname');
    // Fallback: extract locale from pathname
    const pathname = usePathname();
    if (pathname.startsWith('/ur')) {
      return 'ur';
    }
    return 'en'; // default locale
  }
}