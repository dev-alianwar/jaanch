from sqlalchemy.orm import Session
from translation_models import Translation, TranslationSet
from typing import Dict, List, Optional
import json

class TranslationService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_translations_by_locale(self, locale: str) -> Dict:
        """Get all translations for a specific locale as nested JSON"""
        translation_set = self.db.query(TranslationSet).filter(
            TranslationSet.locale == locale,
            TranslationSet.is_active == True
        ).first()
        
        if translation_set:
            return translation_set.translations
        
        # Fallback to individual translations if no set exists
        translations = self.db.query(Translation).filter(
            Translation.locale == locale,
            Translation.is_active == True
        ).all()
        
        result = {}
        for trans in translations:
            keys = trans.key.split('.')
            current = result
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = trans.value
        
        return result
    
    def get_all_translations(self) -> List[Dict]:
        """Get all individual translations for admin management"""
        translations = self.db.query(Translation).filter(
            Translation.is_active == True
        ).all()
        return [trans.to_dict() for trans in translations]
    
    def get_translations_by_category(self, category: str, locale: Optional[str] = None) -> List[Dict]:
        """Get translations by category"""
        query = self.db.query(Translation).filter(
            Translation.category == category,
            Translation.is_active == True
        )
        
        if locale:
            query = query.filter(Translation.locale == locale)
        
        translations = query.all()
        return [trans.to_dict() for trans in translations]
    
    def create_translation(self, key: str, locale: str, value: str, 
                          category: Optional[str] = None, description: Optional[str] = None) -> Translation:
        """Create a new translation"""
        translation = Translation(
            key=key,
            locale=locale,
            value=value,
            category=category,
            description=description
        )
        self.db.add(translation)
        self.db.commit()
        self.db.refresh(translation)
        
        # Update translation set
        self._update_translation_set(locale)
        
        return translation
    
    def update_translation(self, translation_id: str, value: str, 
                          description: Optional[str] = None) -> Optional[Translation]:
        """Update an existing translation"""
        translation = self.db.query(Translation).filter(
            Translation.id == translation_id
        ).first()
        
        if translation:
            translation.value = value
            if description is not None:
                translation.description = description
            self.db.commit()
            self.db.refresh(translation)
            
            # Update translation set
            self._update_translation_set(translation.locale)
            
            return translation
        
        return None
    
    def delete_translation(self, translation_id: str) -> bool:
        """Soft delete a translation"""
        translation = self.db.query(Translation).filter(
            Translation.id == translation_id
        ).first()
        
        if translation:
            translation.is_active = False
            self.db.commit()
            
            # Update translation set
            self._update_translation_set(translation.locale)
            
            return True
        
        return False
    
    def _update_translation_set(self, locale: str):
        """Update the translation set for a locale"""
        translations = self.get_translations_by_locale(locale)
        
        translation_set = self.db.query(TranslationSet).filter(
            TranslationSet.locale == locale,
            TranslationSet.is_active == True
        ).first()
        
        if translation_set:
            translation_set.translations = translations
            self.db.commit()
        else:
            new_set = TranslationSet(
                locale=locale,
                translations=translations
            )
            self.db.add(new_set)
            self.db.commit()
    
    def seed_default_translations(self):
        """Seed default translations"""
        default_translations = {
            'en': {
                'common.loading': 'Loading...',
                'common.submit': 'Submit',
                'common.cancel': 'Cancel',
                'common.save': 'Save',
                'common.delete': 'Delete',
                'common.edit': 'Edit',
                'common.close': 'Close',
                'common.back': 'Back',
                'common.next': 'Next',
                'common.previous': 'Previous',
                'common.search': 'Search',
                'common.filter': 'Filter',
                'common.clear': 'Clear',
                'common.yes': 'Yes',
                'common.no': 'No',
                
                'navigation.home': 'Home',
                'navigation.features': 'Features',
                'navigation.download': 'Download',
                'navigation.dashboard': 'Dashboard',
                'navigation.login': 'Login',
                'navigation.register': 'Register',
                'navigation.logout': 'Logout',
                
                'auth.signIn': 'Sign in to your account',
                'auth.createAccount': 'Create your account',
                'auth.signInToExisting': 'sign in to your existing account',
                'auth.createNew': 'create a new account',
                'auth.email': 'Email address',
                'auth.password': 'Password',
                'auth.confirmPassword': 'Confirm Password',
                'auth.firstName': 'First Name',
                'auth.lastName': 'Last Name',
                'auth.phone': 'Phone',
                'auth.accountType': 'Account Type',
                'auth.customer': 'Customer',
                'auth.business': 'Business',
                'auth.businessName': 'Business Name',
                'auth.businessType': 'Business Type',
                'auth.address': 'Address',
                'auth.registrationNumber': 'Registration Number',
                'auth.forgotPassword': 'Forgot your password?',
                'auth.signInButton': 'Sign in',
                'auth.createAccountButton': 'Create Account',
                'auth.loginFailed': 'Login failed. Please try again.',
                'auth.registrationFailed': 'Registration failed. Please try again.',
                'auth.passwordsDoNotMatch': 'Passwords do not match',
                'auth.enterEmail': 'Enter your email',
                'auth.enterPassword': 'Enter your password',
                
                'dashboard.welcome': 'Welcome, {name}!',
                'dashboard.customerDashboard': 'Customer Dashboard',
                'dashboard.businessDashboard': 'Business Dashboard',
                'dashboard.superAdminDashboard': 'Super Admin Dashboard',
                'dashboard.browseBusiness': 'Browse Businesses',
                'dashboard.myInstallmentRequests': 'My Installment Requests',
                'dashboard.paymentHistory': 'Payment History',
                'dashboard.pendingRequests': 'Pending Requests',
                'dashboard.activeInstallments': 'Active Installments',
                'dashboard.customerHistory': 'Customer History',
                'dashboard.businessAnalytics': 'Business Analytics',
                'dashboard.systemOverview': 'System Overview',
                'dashboard.fraudDetection': 'Fraud Detection',
                'dashboard.businessManagement': 'Business Management',
                'dashboard.userManagement': 'User Management',
                'dashboard.analyticsReports': 'Analytics & Reports',
                'dashboard.systemConfiguration': 'System Configuration',
            },
            'ur': {
                'common.loading': 'لوڈ ہو رہا ہے...',
                'common.submit': 'جمع کریں',
                'common.cancel': 'منسوخ',
                'common.save': 'محفوظ کریں',
                'common.delete': 'حذف کریں',
                'common.edit': 'ترمیم',
                'common.close': 'بند کریں',
                'common.back': 'واپس',
                'common.next': 'اگلا',
                'common.previous': 'پچھلا',
                'common.search': 'تلاش',
                'common.filter': 'فلٹر',
                'common.clear': 'صاف کریں',
                'common.yes': 'ہاں',
                'common.no': 'نہیں',
                
                'navigation.home': 'ہوم',
                'navigation.features': 'خصوصیات',
                'navigation.download': 'ڈاؤن لوڈ',
                'navigation.dashboard': 'ڈیش بورڈ',
                'navigation.login': 'لاگ ان',
                'navigation.register': 'رجسٹر',
                'navigation.logout': 'لاگ آؤٹ',
                
                'auth.signIn': 'اپنے اکاؤنٹ میں سائن ان کریں',
                'auth.createAccount': 'اپنا اکاؤنٹ بنائیں',
                'auth.signInToExisting': 'اپنے موجودہ اکاؤنٹ میں سائن ان کریں',
                'auth.createNew': 'نیا اکاؤنٹ بنائیں',
                'auth.email': 'ای میل ایڈریس',
                'auth.password': 'پاس ورڈ',
                'auth.confirmPassword': 'پاس ورڈ کی تصدیق',
                'auth.firstName': 'پہلا نام',
                'auth.lastName': 'آخری نام',
                'auth.phone': 'فون',
                'auth.accountType': 'اکاؤنٹ کی قسم',
                'auth.customer': 'کسٹمر',
                'auth.business': 'کاروبار',
                'auth.businessName': 'کاروبار کا نام',
                'auth.businessType': 'کاروبار کی قسم',
                'auth.address': 'پتہ',
                'auth.registrationNumber': 'رجسٹریشن نمبر',
                'auth.forgotPassword': 'اپنا پاس ورڈ بھول گئے؟',
                'auth.signInButton': 'سائن ان',
                'auth.createAccountButton': 'اکاؤنٹ بنائیں',
                'auth.loginFailed': 'لاگ ان ناکام۔ براہ کرم دوبارہ کوشش کریں۔',
                'auth.registrationFailed': 'رجسٹریشن ناکام۔ براہ کرم دوبارہ کوشش کریں۔',
                'auth.passwordsDoNotMatch': 'پاس ورڈ میل نہیں کھاتے',
                'auth.enterEmail': 'اپنا ای میل درج کریں',
                'auth.enterPassword': 'اپنا پاس ورڈ درج کریں',
                
                'dashboard.welcome': 'خوش آمدید، {name}!',
                'dashboard.customerDashboard': 'کسٹمر ڈیش بورڈ',
                'dashboard.businessDashboard': 'بزنس ڈیش بورڈ',
                'dashboard.superAdminDashboard': 'سپر ایڈمن ڈیش بورڈ',
                'dashboard.browseBusiness': 'کاروبار دیکھیں',
                'dashboard.myInstallmentRequests': 'میری قسط کی درخواستیں',
                'dashboard.paymentHistory': 'ادائیگی کی تاریخ',
                'dashboard.pendingRequests': 'زیر التواء درخواستیں',
                'dashboard.activeInstallments': 'فعال اقساط',
                'dashboard.customerHistory': 'کسٹمر کی تاریخ',
                'dashboard.businessAnalytics': 'بزنس تجزیات',
                'dashboard.systemOverview': 'سسٹم کا جائزہ',
                'dashboard.fraudDetection': 'فراڈ ڈیٹیکشن',
                'dashboard.businessManagement': 'بزنس مینجمنٹ',
                'dashboard.userManagement': 'یوزر مینجمنٹ',
                'dashboard.analyticsReports': 'تجزیات اور رپورٹس',
                'dashboard.systemConfiguration': 'سسٹم کنفیگریشن',
            }
        }
        
        for locale, translations in default_translations.items():
            for key, value in translations.items():
                category = key.split('.')[0]
                
                # Check if translation already exists
                existing = self.db.query(Translation).filter(
                    Translation.key == key,
                    Translation.locale == locale
                ).first()
                
                if not existing:
                    translation = Translation(
                        key=key,
                        locale=locale,
                        value=value,
                        category=category
                    )
                    self.db.add(translation)
            
            self.db.commit()
            self._update_translation_set(locale)