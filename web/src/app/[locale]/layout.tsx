import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "../globals.css";
import { AuthProvider } from "@/contexts/AuthContext";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import { TranslationProvider } from "@/components/TranslationProvider";

const inter = Inter({ subsets: ["latin"] });

const appName = process.env.NEXT_PUBLIC_APP_NAME || "InstallmentGuard";

export const metadata: Metadata = {
  title: `${appName} - Fraud Detection for Installment Purchases`,
  description: "Advanced fraud detection system for installment purchases across multiple businesses. Protect your business from fraudulent chains and make informed credit decisions.",
};

export function generateStaticParams() {
  return [{ locale: 'en' }, { locale: 'ur' }];
}

export default async function RootLayout({
  children,
  params
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  // Ensure locale is valid to prevent hydration mismatches
  const validLocale = locale === 'ur' ? 'ur' : 'en';
  const direction = validLocale === 'ur' ? 'rtl' : 'ltr';

  const fallbackMessages = {
    navigation: {
      home: validLocale === 'ur' ? 'ہوم' : 'Home',
      features: validLocale === 'ur' ? 'خصوصیات' : 'Features',
      download: validLocale === 'ur' ? 'ڈاؤن لوڈ' : 'Download',
      dashboard: validLocale === 'ur' ? 'ڈیش بورڈ' : 'Dashboard',
      login: validLocale === 'ur' ? 'لاگ ان' : 'Login',
      register: validLocale === 'ur' ? 'رجسٹر' : 'Register',
      logout: validLocale === 'ur' ? 'لاگ آؤٹ' : 'Logout',
    },
    auth: {
      signIn: validLocale === 'ur' ? 'اپنے اکاؤنٹ میں سائن ان کریں' : 'Sign in to your account',
      email: validLocale === 'ur' ? 'ای میل ایڈریس' : 'Email address',
      password: validLocale === 'ur' ? 'پاس ورڈ' : 'Password',
      enterEmail: validLocale === 'ur' ? 'اپنا ای میل درج کریں' : 'Enter your email',
      enterPassword: validLocale === 'ur' ? 'اپنا پاس ورڈ درج کریں' : 'Enter your password',
      signInButton: validLocale === 'ur' ? 'سائن ان' : 'Sign in',
      createNew: validLocale === 'ur' ? 'نیا اکاؤنٹ بنائیں' : 'create a new account',
      forgotPassword: validLocale === 'ur' ? 'اپنا پاس ورڈ بھول گئے؟' : 'Forgot your password?',
    },
    home: {
      heroTitle: validLocale === 'ur' ? 'قسط کی دھوکہ دہی کو روکیں' : 'Stop Installment Fraud',
      heroSubtitle: validLocale === 'ur' ? 'اس سے پہلے کہ یہ شروع ہو' : 'Before It Starts',
      heroDescription: validLocale === 'ur' ? 'جدید فراڈ ڈیٹیکشن سسٹم جو متعدد کاروبار میں قسط کی خریداری کو ٹریک کرتا ہے' : 'Advanced fraud detection system that tracks installment purchases across multiple businesses',
      getStartedFree: validLocale === 'ur' ? 'مفت شروع کریں' : 'Get Started Free',
      downloadApps: validLocale === 'ur' ? 'ایپس ڈاؤن لوڈ کریں' : 'Download Apps',
    }
  };

  return (
    <html lang={validLocale} dir={direction} suppressHydrationWarning>
      <body className={inter.className}>
        <TranslationProvider locale={validLocale} initialMessages={fallbackMessages}>
          <AuthProvider>
            <div className="min-h-screen flex flex-col">
              <Header locale={validLocale} />
              <main className="flex-1">
                {children}
              </main>
              <Footer locale={validLocale} />
            </div>
          </AuthProvider>
        </TranslationProvider>
      </body>
    </html>
  );
}