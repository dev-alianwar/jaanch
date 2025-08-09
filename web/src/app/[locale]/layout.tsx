import type { Metadata } from "next";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "InstallmentGuard - Fraud Detection for Installment Purchases",
  description: "Advanced fraud detection system for installment purchases across multiple businesses.",
};

export default async function LocaleLayout({
  children,
  params
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  return (
    <div className="min-h-screen bg-white">
      <main>
        {children}
      </main>
    </div>
  );
}