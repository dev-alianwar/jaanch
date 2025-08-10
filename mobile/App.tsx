import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';

// Import screens
import LoginScreen from './src/screens/LoginScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import CustomerHomeScreen from './src/screens/CustomerHomeScreen';
import BusinessHomeScreen from './src/screens/BusinessHomeScreen';
import LoadingScreen from './src/screens/LoadingScreen';

// Import context
import { AuthProvider, useAuth } from './src/context/AuthContext';

// Import types
import { RootStackParamList } from './src/types/navigation';

// Import i18n
import { initializeTranslations } from './src/i18n';

const Stack = createStackNavigator<RootStackParamList>();

function AppNavigator() {
  const { user, loading } = useAuth();

  useEffect(() => {
    // Initialize translations on app start (non-blocking)
    initializeTranslations().catch(() => {
      // Silently handle translation loading errors
      console.warn('Translations could not be loaded from API, using static translations');
    });
  }, []);

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {user ? (
          // User is signed in
          <>
            {user.role === 'customer' && (
              <Stack.Screen name="CustomerHome" component={CustomerHomeScreen} />
            )}
            {user.role === 'business' && (
              <Stack.Screen name="BusinessHome" component={BusinessHomeScreen} />
            )}
          </>
        ) : (
          // User is not signed in
          <>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default function App() {
  return (
    <SafeAreaProvider>
      <AuthProvider>
        <StatusBar barStyle="dark-content" />
        <AppNavigator />
      </AuthProvider>
    </SafeAreaProvider>
  );
}