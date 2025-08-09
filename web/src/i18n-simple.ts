import { notFound } from 'next/navigation';
import { getRequestConfig } from 'next-intl/server';

const locales = ['en', 'ur'];

export default getRequestConfig(async ({ locale }) => {
  if (!locale || !locales.includes(locale)) notFound();

  return {
    messages: {
      auth: {
        signIn: locale === 'ur' ? 'اپنے اکاؤنٹ میں سائن ان کریں' : 'Sign in to your account',
        email: locale === 'ur' ? 'ای میل ایڈریس' : 'Email address',
        password: locale === 'ur' ? 'پاس ورڈ' : 'Password',
      },
      navigation: {
        home: locale === 'ur' ? 'ہوم' : 'Home',
        login: locale === 'ur' ? 'لاگ ان' : 'Login',
        register: locale === 'ur' ? 'رجسٹر' : 'Register',
      }
    }
  };
});