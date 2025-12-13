/**
 * Profile Screen
 *
 * User profile and settings
 */
import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { useApp } from '../context/AppContext';
import { logout } from '../services/api';

const ProfileScreen = ({ navigation }) => {
  const { userId } = useApp();

  const handleLogout = () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Logout',
        style: 'destructive',
        onPress: async () => {
          await logout();
          // Navigate to login screen
        },
      },
    ]);
  };

  const menuItems = [
    {
      icon: '👤',
      title: 'Personal Information',
      onPress: () => Alert.alert('Coming Soon'),
    },
    {
      icon: '🏠',
      title: 'Property Details',
      onPress: () => Alert.alert('Coming Soon'),
    },
    {
      icon: '🔔',
      title: 'Notifications',
      onPress: () => Alert.alert('Coming Soon'),
    },
    {
      icon: '📊',
      title: 'Statistics & Reports',
      onPress: () => Alert.alert('Coming Soon'),
    },
    {
      icon: '❓',
      title: 'Help & FAQ',
      onPress: () => Alert.alert('Coming Soon'),
    },
    {
      icon: '⚙️',
      title: 'Settings',
      onPress: () => Alert.alert('Coming Soon'),
    },
  ];

  return (
    <ScrollView style={styles.container}>
      {/* Profile Header */}
      <View style={styles.profileHeader}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>👤</Text>
        </View>
        <Text style={styles.userName}>User {userId?.substring(0, 8)}</Text>
        <Text style={styles.userEmail}>user@powersave.cy</Text>
      </View>

      {/* Achievements */}
      <View style={styles.achievementsCard}>
        <Text style={styles.cardTitle}>Achievements</Text>
        <View style={styles.badgesContainer}>
          <View style={styles.badge}>
            <Text style={styles.badgeEmoji}>🏆</Text>
            <Text style={styles.badgeName}>First Session</Text>
          </View>
          <View style={styles.badge}>
            <Text style={styles.badgeEmoji}>⚡</Text>
            <Text style={styles.badgeName}>Week Streak</Text>
          </View>
          <View style={styles.badge}>
            <Text style={styles.badgeEmoji}>🌱</Text>
            <Text style={styles.badgeName}>Eco Warrior</Text>
          </View>
        </View>
      </View>

      {/* Menu Items */}
      <View style={styles.menuCard}>
        {menuItems.map((item, index) => (
          <TouchableOpacity
            key={index}
            style={styles.menuItem}
            onPress={item.onPress}
          >
            <View style={styles.menuItemLeft}>
              <Text style={styles.menuIcon}>{item.icon}</Text>
              <Text style={styles.menuTitle}>{item.title}</Text>
            </View>
            <Text style={styles.menuArrow}>›</Text>
          </TouchableOpacity>
        ))}
      </View>

      {/* Logout Button */}
      <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
        <Text style={styles.logoutText}>Logout</Text>
      </TouchableOpacity>

      {/* Version */}
      <Text style={styles.versionText}>Version 1.0.0</Text>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  profileHeader: {
    backgroundColor: '#4CAF50',
    padding: 32,
    alignItems: 'center',
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#FFFFFF',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 12,
  },
  avatarText: {
    fontSize: 40,
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  userEmail: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.9,
  },
  achievementsCard: {
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
  badgesContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  badge: {
    alignItems: 'center',
  },
  badgeEmoji: {
    fontSize: 36,
    marginBottom: 8,
  },
  badgeName: {
    fontSize: 12,
    color: '#666',
  },
  menuCard: {
    backgroundColor: '#FFFFFF',
    margin: 16,
    marginTop: 0,
    borderRadius: 12,
    overflow: 'hidden',
  },
  menuItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  menuItemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  menuIcon: {
    fontSize: 24,
    marginRight: 12,
  },
  menuTitle: {
    fontSize: 16,
    color: '#333',
  },
  menuArrow: {
    fontSize: 24,
    color: '#CCC',
  },
  logoutButton: {
    backgroundColor: '#FFFFFF',
    margin: 16,
    marginTop: 0,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#F44336',
  },
  logoutText: {
    color: '#F44336',
    fontSize: 16,
    fontWeight: '600',
  },
  versionText: {
    textAlign: 'center',
    color: '#999',
    fontSize: 12,
    marginVertical: 16,
  },
});

export default ProfileScreen;
