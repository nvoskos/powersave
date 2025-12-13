/**
 * Home Screen
 *
 * Dashboard with overview of all metrics
 */
import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import { useApp } from '../context/AppContext';

const HomeScreen = ({ navigation }) => {
  const { walletBalance, totalKwhSaved, greenPoints } = useApp();

  const quickActions = [
    {
      title: 'Schedule Session',
      icon: '📅',
      color: '#4CAF50',
      onPress: () => navigation.navigate('Sessions'),
    },
    {
      title: 'View Wallet',
      icon: '💰',
      color: '#2196F3',
      onPress: () => navigation.navigate('Wallet'),
    },
    {
      title: 'Plant Garden',
      icon: '🌱',
      color: '#8BC34A',
      onPress: () => navigation.navigate('Garden'),
    },
    {
      title: 'Donate',
      icon: '❤️',
      color: '#FF5722',
      onPress: () => navigation.navigate('Wallet'),
    },
  ];

  return (
    <ScrollView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.greeting}>Welcome to PowerSave</Text>
        <Text style={styles.tagline}>
          Save Energy • Earn Rewards • Help Others
        </Text>
      </View>

      {/* Stats Overview */}
      <View style={styles.statsContainer}>
        <View style={styles.statCard}>
          <Text style={styles.statIcon}>💰</Text>
          <Text style={styles.statValue}>€{walletBalance || 0}</Text>
          <Text style={styles.statLabel}>Wallet Balance</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statIcon}>⚡</Text>
          <Text style={styles.statValue}>{totalKwhSaved || 0}</Text>
          <Text style={styles.statLabel}>kWh Saved</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statIcon}>🌟</Text>
          <Text style={styles.statValue}>{greenPoints || 0}</Text>
          <Text style={styles.statLabel}>Green Points</Text>
        </View>
      </View>

      {/* Quick Actions */}
      <View style={styles.quickActionsCard}>
        <Text style={styles.cardTitle}>Quick Actions</Text>
        <View style={styles.actionsGrid}>
          {quickActions.map((action, index) => (
            <TouchableOpacity
              key={index}
              style={[styles.actionButton, { backgroundColor: action.color }]}
              onPress={action.onPress}
            >
              <Text style={styles.actionIcon}>{action.icon}</Text>
              <Text style={styles.actionTitle}>{action.title}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* How It Works */}
      <View style={styles.howItWorksCard}>
        <Text style={styles.cardTitle}>How PowerSave Works</Text>
        <StepItem
          number="1"
          title="Schedule a Saving Session"
          description="Choose a time (typically 17:00-20:00) to reduce energy"
        />
        <StepItem
          number="2"
          title="Reduce Your Consumption"
          description="Turn off unnecessary devices during the session"
        />
        <StepItem
          number="3"
          title="Earn Rewards"
          description="Get € credits for waste fees + Green Points"
        />
        <StepItem
          number="4"
          title="Make an Impact"
          description="Help the environment and support others"
        />
      </View>

      {/* Impact Banner */}
      <View style={styles.impactBanner}>
        <Text style={styles.impactTitle}>🌍 Together We've Saved</Text>
        <Text style={styles.impactValue}>50,000+ kWh</Text>
        <Text style={styles.impactSubtext}>
          Equivalent to 35 tons of CO₂
        </Text>
      </View>
    </ScrollView>
  );
};

const StepItem = ({ number, title, description }) => (
  <View style={styles.stepItem}>
    <View style={styles.stepNumber}>
      <Text style={styles.stepNumberText}>{number}</Text>
    </View>
    <View style={styles.stepContent}>
      <Text style={styles.stepTitle}>{title}</Text>
      <Text style={styles.stepDescription}>{description}</Text>
    </View>
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  header: {
    backgroundColor: '#4CAF50',
    padding: 24,
    paddingTop: 40,
  },
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  tagline: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.9,
    marginTop: 8,
  },
  statsContainer: {
    flexDirection: 'row',
    padding: 16,
    paddingBottom: 0,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    marginHorizontal: 4,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  statIcon: {
    fontSize: 32,
    marginBottom: 8,
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  statLabel: {
    fontSize: 11,
    color: '#666',
    marginTop: 4,
    textAlign: 'center',
  },
  quickActionsCard: {
    backgroundColor: '#FFFFFF',
    margin: 16,
    padding: 20,
    borderRadius: 12,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  actionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  actionButton: {
    width: '48%',
    aspectRatio: 1,
    borderRadius: 12,
    padding: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  actionIcon: {
    fontSize: 40,
    marginBottom: 8,
  },
  actionTitle: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
    textAlign: 'center',
  },
  howItWorksCard: {
    backgroundColor: '#FFFFFF',
    margin: 16,
    marginTop: 0,
    padding: 20,
    borderRadius: 12,
  },
  stepItem: {
    flexDirection: 'row',
    marginBottom: 20,
  },
  stepNumber: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#4CAF50',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  stepNumberText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: 'bold',
  },
  stepContent: {
    flex: 1,
  },
  stepTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  stepDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
  },
  impactBanner: {
    backgroundColor: '#E8F5E9',
    margin: 16,
    marginTop: 0,
    padding: 24,
    borderRadius: 12,
    alignItems: 'center',
  },
  impactTitle: {
    fontSize: 16,
    color: '#2E7D32',
    marginBottom: 8,
  },
  impactValue: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#2E7D32',
  },
  impactSubtext: {
    fontSize: 14,
    color: '#2E7D32',
    opacity: 0.8,
    marginTop: 4,
  },
});

export default HomeScreen;
