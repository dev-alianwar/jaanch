import React from 'react';
import { View, TouchableOpacity, Text, StyleSheet } from 'react-native';
import i18n from '../i18n';

const LanguageSwitcher: React.FC = () => {
  const switchLanguage = (locale: string) => {
    i18n.locale = locale;
    // Force re-render by updating a state or using a context
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity
        style={[styles.button, i18n.locale === 'en' && styles.activeButton]}
        onPress={() => switchLanguage('en')}
      >
        <Text style={[styles.buttonText, i18n.locale === 'en' && styles.activeText]}>
          EN
        </Text>
      </TouchableOpacity>
      
      <TouchableOpacity
        style={[styles.button, i18n.locale === 'ur' && styles.activeButton]}
        onPress={() => switchLanguage('ur')}
      >
        <Text style={[styles.buttonText, i18n.locale === 'ur' && styles.activeText]}>
          اردو
        </Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: '#f0f0f0',
    borderRadius: 20,
    padding: 2,
  },
  button: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 18,
    minWidth: 40,
    alignItems: 'center',
  },
  activeButton: {
    backgroundColor: '#007AFF',
  },
  buttonText: {
    fontSize: 12,
    color: '#666',
    fontWeight: '500',
  },
  activeText: {
    color: '#fff',
  },
});

export default LanguageSwitcher;