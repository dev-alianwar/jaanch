import React from 'react';
import Link from 'next/link';
import { getTranslations, createTranslator } from '@/lib/getTranslations';
import type { Locale } from '@/lib/locale';

interface FooterProps {
  locale: Locale;
}

export default async function Footer({ locale }: FooterProps) {
  const messages = await getTranslations(locale);
  const t = createTranslator(messages);
  
  const appName = process.env.NEXT_PUBLIC_APP_NAME || t('app.name');

  return (
    <footer className="bg-gray-50 border-t">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {appName}
            </h3>
            <p className="text-gray-600 mb-4">
              {t('footer.description')}
            </p>
          </div>
          
          <div>
            <h4 className="text-sm font-semibold text-gray-900 mb-4">{t('footer.product')}</h4>
            <ul className="space-y-2">
              <li>
                <Link href="/features" className="text-gray-600 hover:text-gray-900">
                  {t('navigation.features')}
                </Link>
              </li>
              <li>
                <Link href="/download" className="text-gray-600 hover:text-gray-900">
                  {t('navigation.download')}
                </Link>
              </li>
              <li>
                <Link href="/pricing" className="text-gray-600 hover:text-gray-900">
                  {t('footer.pricing')}
                </Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-sm font-semibold text-gray-900 mb-4">{t('footer.support')}</h4>
            <ul className="space-y-2">
              <li>
                <Link href="/contact" className="text-gray-600 hover:text-gray-900">
                  {t('footer.contactUs')}
                </Link>
              </li>
              <li>
                <Link href="/help" className="text-gray-600 hover:text-gray-900">
                  {t('footer.helpCenter')}
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-gray-600 hover:text-gray-900">
                  {t('footer.privacyPolicy')}
                </Link>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="mt-8 pt-8 border-t border-gray-200">
          <p className="text-center text-gray-500 text-sm">
            {t('footer.copyright')}
          </p>
        </div>
      </div>
    </footer>
  );
}