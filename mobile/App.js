/**
 * PowerSave Mobile App
 *
 * Main Application Entry Point
 */
import React from 'react';
import { StatusBar } from 'react-native';
import { AppProvider } from './src/context/AppContext';
import AppNavigator from './src/navigation/AppNavigator';

const App = () => {
  return (
    <AppProvider>
      <StatusBar barStyle="dark-content" backgroundColor="#FFFFFF" />
      <AppNavigator />
    </AppProvider>
  );
};

export default App;
