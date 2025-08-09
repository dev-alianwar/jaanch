import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import "../globals.css";
import { AuthProvider } from "@/contexts/AuthContext";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "InstallmentGuard - Fraud Detection for Installment Purchases",
  description: "Advanced fraud detection system for installment purchases across multiple businesses. Protect your business from fraudulent chains and make informed credit decisions.",
};

export default async function RootLayout({
  children,
  params
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  
  // Providing all messages to the client side
  let messages;
  try {
    messages = await getMessages();
  } catch (error) {
    console.warn('Failed to load messages, using fallback');
    messages = {
      navigation: {
        home: 'Home',
        features: 'Features',
        download: 'Download',
        dashboard: 'Dashboard',
        login: 'Login',
        register: 'Register',
        logout: 'Logout',
      },
      auth: {
        signIn: 'Sign in to your account',
        email: 'Email address',
        password: 'Password',
        enterEmail: 'Enter your email',
        enterPassword: 'Enter your password',
        signInButton: 'Sign in',
        createNew: 'create a new account',
        forgotPassword: 'Forgot your password?',
      }
    };
  }

  return (
    <html lang={locale} dir={locale === 'ur' ? 'rtl' : 'ltr'}>
      <body className={inter.className}>
        <NextIntlClientProvider messages={messages} locale={locale}>
          <AuthProvider>
            <div className="min-h-screen flex flex-col">
              <Header />
              <main className="flex-1">
                {children}
              </main>
              <Footer />
            </div>
          </AuthProvider>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}