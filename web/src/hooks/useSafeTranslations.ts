'use client';

import { useTranslations } from 'next-intl';
import { useCallback } from 'react';

export function useSafeTranslations(namespace: string) {
  const createFallbackTranslator = useCallback((ns: string) => {
    const fallbacks: Record<string, Record<string, string>> = {
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
        createAccount: 'Create your account',
        signInToExisting: 'sign in to your existing account',
        createNew: 'create a new account',
        email: 'Email address',
        password: 'Password',
        confirmPassword: 'Confirm Password',
        firstName: 'First Name',
        lastName: 'Last Name',
        phone: 'Phone',
        forgotPassword: 'Forgot your password?',
        signInButton: 'Sign in',
        createAccountButton: 'Create Account',
        enterEmail: 'Enter your email',
        enterPassword: 'Enter your password',
      },
      common: {
        loading: 'Loading...',
        submit: 'Submit',
        cancel: 'Cancel',
        save: 'Save',
        delete: 'Delete',
        edit: 'Edit',
      }
    };

    return (key: string) => {
      const namespaceTranslations = fallbacks[ns] || {};
      return namespaceTranslations[key] || key;
    };
  }, []);

  try {
    const t = useTranslations(namespace);
    return t;
  } catch (error) {
    console.warn(`Translation context not available for namespace ${namespace}, using fallback`);
    return createFallbackTranslator(namespace);
  }
}