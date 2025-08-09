'use client';

import React, { Suspense } from 'react';
import { NextIntlClientProvider } from 'next-intl';

interface SafeTranslationWrapperProps {
  children: React.ReactNode;
  messages?: any;
  locale?: string;
}

const SafeTranslationWrapper: React.FC<SafeTranslationWrapperProps> = ({
  children,
  messages = {},
  locale = 'en'
}) => {
  return (
    <Suspense fallback={<div>Loading translations...</div>}>
      <NextIntlClientProvider messages={messages} locale={locale}>
        {children}
      </NextIntlClientProvider>
    </Suspense>
  );
};

export default SafeTranslationWrapper;