import { NextRequest, NextResponse } from 'next/server';

const locales = ['en', 'ur'];
const defaultLocale = 'en';
const LOCALE_COOKIE = 'NEXT_LOCALE';

function getLocale(request: NextRequest): string {
  // 1. Check cookie
  const cookieLocale = request.cookies.get(LOCALE_COOKIE)?.value;
  if (cookieLocale && locales.includes(cookieLocale)) {
    return cookieLocale;
  }

  // 2. Check Accept-Language header
  const acceptLanguage = request.headers.get('accept-language');
  if (acceptLanguage) {
    const preferredLocale = acceptLanguage
      .split(',')[0]
      .split('-')[0]
      .toLowerCase();
    if (locales.includes(preferredLocale)) {
      return preferredLocale;
    }
  }

  // 3. Default locale
  return defaultLocale;
}

export function middleware(request: NextRequest) {
  const locale = getLocale(request);
  const response = NextResponse.next();

  // Set locale cookie if not present or different
  const currentCookie = request.cookies.get(LOCALE_COOKIE)?.value;
  if (currentCookie !== locale) {
    response.cookies.set(LOCALE_COOKIE, locale, {
      path: '/',
      maxAge: 31536000, // 1 year
      sameSite: 'lax',
    });
  }

  // Add locale to headers for server components to access
  response.headers.set('x-locale', locale);

  return response;
}

export const config = {
  matcher: [
    // Skip all internal paths (_next, api, static files)
    '/((?!_next|api|favicon.ico|.*\\.).*)',
  ],
};