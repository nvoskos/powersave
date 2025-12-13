/**
 * App Navigator
 *
 * Main navigation structure using React Navigation
 */
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';

// Screens
import WasteWalletScreen from '../screens/WasteWalletScreen';
import SessionsScreen from '../screens/SessionsScreen';
import GreenGardenScreen from '../screens/GreenGardenScreen';
import HomeScreen from '../screens/HomeScreen';
import ProfileScreen from '../screens/ProfileScreen';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

// Tab Navigator
const TabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#4CAF50',
        tabBarInactiveTintColor: '#999',
        tabBarStyle: {
          paddingBottom: 8,
          paddingTop: 8,
          height: 60,
        },
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          title: 'Home',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>🏠</Text>,
        }}
      />
      <Tab.Screen
        name="Wallet"
        component={WasteWalletScreen}
        options={{
          title: 'Waste Wallet',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>💰</Text>,
        }}
      />
      <Tab.Screen
        name="Sessions"
        component={SessionsScreen}
        options={{
          title: 'Sessions',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>⚡</Text>,
        }}
      />
      <Tab.Screen
        name="Garden"
        component={GreenGardenScreen}
        options={{
          title: 'Green Garden',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>🌱</Text>,
        }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          title: 'Profile',
          tabBarIcon: ({ color }) => <Text style={{ fontSize: 24 }}>👤</Text>,
        }}
      />
    </Tab.Navigator>
  );
};

// Main App Navigator
const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Main"
          component={TabNavigator}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;
