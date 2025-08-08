import React, { useState, useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Import screens
import LoginScreen from './src/screens/LoginScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import CustomerHomeScreen from './src/screens/CustomerHomeScreen';
import BusinessHomeScreen from './src/screens/BusinessHomeScreen';
import SuperAdminHomeScreen from './src/screens/SuperAdminHomeScreen';
import LoadingScreen from './src/screens/LoadingScreen';

// Import context
import { AuthProvider, useAuth } from './src/context/AuthContext';

// Import types
import { RootStackParamList } from './src/types/navigation';

const Stack = createStackNavigator<RootStackParamList>();

function AppNavigator() {
  const { user, loading } = useAuth();

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
            {user.role === 'superadmin' && (
              <Stack.Screen name="SuperAdminHome" component={SuperAdminHomeScreen} />
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
    <AuthProvider>
      <StatusBar style="auto" />
      <AppNavigator />
    </AuthProvider>
  );
}