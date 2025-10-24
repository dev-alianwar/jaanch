import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import { TranslationProvider } from "@/components/TranslationProvider";
import { getLocale } from "@/lib/getLocale";

const inter = Inter({ subsets: ["latin"] });

const appName = process.env.NEXT_PUBLIC_APP_NAME || "InstallmentGuard";

export const metadata: Metadata = {
  title: `${appName} - Fraud Detection for Installment Purchases`,
  description: "Advanced fraud detection system for installment purchases across multiple businesses. Protect your business from fraudulent chains and make informed credit decisions.",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const locale = await getLocale();
  const direction = locale === 'ur' ? 'rtl' : 'ltr';

  const fallbackMessages = {
    navigation: {
      home: locale === 'ur' ? 'ہوم' : 'Home',
      features: locale === 'ur' ? 'خصوصیات' : 'Features',
      download: locale === 'ur' ? 'ڈاؤن لوڈ' : 'Download',
      dashboard: locale === 'ur' ? 'ڈیش بورڈ' : 'Dashboard',
      login: locale === 'ur' ? 'لاگ ان' : 'Login',
      register: locale === 'ur' ? 'رجسٹر' : 'Register',
      logout: locale === 'ur' ? 'لاگ آؤٹ' : 'Logout',
    },
    auth: {
      signIn: locale === 'ur' ? 'اپنے اکاؤنٹ میں سائن ان کریں' : 'Sign in to your account',
      email: locale === 'ur' ? 'ای میل ایڈریس' : 'Email address',
      password: locale === 'ur' ? 'پاس ورڈ' : 'Password',
      enterEmail: locale === 'ur' ? 'اپنا ای میل درج کریں' : 'Enter your email',
      enterPassword: locale === 'ur' ? 'اپنا پاس ورڈ درج کریں' : 'Enter your password',
      signInButton: locale === 'ur' ? 'سائن ان' : 'Sign in',
      createNew: locale === 'ur' ? 'نیا اکاؤنٹ بنائیں' : 'create a new account',
      forgotPassword: locale === 'ur' ? 'اپنا پاس ورڈ بھول گئے؟' : 'Forgot your password?',
    },
    home: {
      heroTitle: locale === 'ur' ? 'قسط کی دھوکہ دہی کو روکیں' : 'Stop Installment Fraud',
      heroSubtitle: locale === 'ur' ? 'اس سے پہلے کہ یہ شروع ہو' : 'Before It Starts',
      heroDescription: locale === 'ur' ? 'جدید فراڈ ڈیٹیکشن سسٹم جو متعدد کاروبار میں قسط کی خریداری کو ٹریک کرتا ہے' : 'Advanced fraud detection system that tracks installment purchases across multiple businesses',
      getStartedFree: locale === 'ur' ? 'مفت شروع کریں' : 'Get Started Free',
      downloadApps: locale === 'ur' ? 'ایپس ڈاؤن لوڈ کریں' : 'Download Apps',
    }
  };

  return (
    <html lang={locale} dir={direction} suppressHydrationWarning>
      <body className={inter.className}>
        <TranslationProvider locale={locale} initialMessages={fallbackMessages}>
          <AuthProvider>
            <div className="min-h-screen flex flex-col">
              <Header locale={locale} />
              <main className="flex-1">
                {children}
              </main>
              <Footer locale={locale} />
            </div>
          </AuthProvider>
        </TranslationProvider>
      </body>
    </html>
  );
}
