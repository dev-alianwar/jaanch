// Shared constants that can be imported by both client and server
export const LOCALE_COOKIE = 'NEXT_LOCALE';
export const defaultLocale = 'en';
export const locales = ['en', 'ur'] as const;

export type Locale = typeof locales[number];
