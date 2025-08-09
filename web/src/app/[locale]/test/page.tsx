import { getTranslations } from 'next-intl/server';

export default async function TestPage({
  params
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: 'auth' });

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Translation Test</h1>
      <p><strong>Locale:</strong> {locale}</p>
      <p><strong>Sign In:</strong> {t('signIn')}</p>
      <p><strong>Email:</strong> {t('email')}</p>
      <p><strong>Password:</strong> {t('password')}</p>
    </div>
  );
}