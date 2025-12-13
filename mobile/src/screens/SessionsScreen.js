/**
 * Saving Sessions Screen
 *
 * Schedule and manage energy saving sessions
 */
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
  Alert,
} from 'react-native';
import { sessionsAPI } from '../services/api';
import { useApp } from '../context/AppContext';

const SessionsScreen = ({ navigation }) => {
  const { userId, refreshUserData } = useApp();
  const [sessions, setSessions] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadData();
  }, [userId]);

  const loadData = async () => {
    if (!userId) return;

    try {
      setLoading(true);
      const [sessionsRes, statsRes] = await Promise.all([
        sessionsAPI.getUserSessions(userId, { limit: 20 }),
        sessionsAPI.getUserStats(userId),
      ]);

      setSessions(sessionsRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const handleScheduleSession = () => {
    const tomorrow17 = new Date();
    tomorrow17.setDate(tomorrow17.getDate() + 1);
    tomorrow17.setHours(17, 0, 0, 0);

    Alert.alert(
      'Schedule Session',
      `Schedule saving session for tomorrow at 17:00?`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Schedule',
          onPress: async () => {
            try {
              await sessionsAPI.createSession(userId, {
                scheduled_start: tomorrow17.toISOString(),
                duration_hours: 3,
                allocation_type: 'WASTE_WALLET',
              });
              Alert.alert('Success', 'Session scheduled!');
              loadData();
            } catch (error) {
              Alert.alert('Error', 'Failed to schedule session');
            }
          },
        },
      ]
    );
  };

  const handleStartSession = async (sessionId) => {
    try {
      await sessionsAPI.startSession(sessionId);
      Alert.alert('Started!', 'Session is now in progress');
      loadData();
    } catch (error) {
      Alert.alert('Error', 'Failed to start session');
    }
  };

  const handleCompleteSession = async (sessionId) => {
    // In production, this would get actual consumption from smart meter
    const mockConsumption = (Math.random() * 1.5 + 0.5).toFixed(2);

    try {
      const result = await sessionsAPI.completeSession(sessionId, mockConsumption);
      Alert.alert('Session Complete!', result.data.message);
      await refreshUserData(userId);
      loadData();
    } catch (error) {
      Alert.alert('Error', 'Failed to complete session');
    }
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#4CAF50" />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Stats Card */}
      {stats && (
        <View style={styles.statsCard}>
          <Text style={styles.statsTitle}>Your Impact</Text>
          <View style={styles.statsGrid}>
            <View style={styles.statBox}>
              <Text style={styles.statValue}>{stats.completed_sessions}</Text>
              <Text style={styles.statLabel}>Sessions</Text>
            </View>
            <View style={styles.statBox}>
              <Text style={styles.statValue}>{stats.total_kwh_saved}</Text>
              <Text style={styles.statLabel}>kWh Saved</Text>
            </View>
            <View style={styles.statBox}>
              <Text style={styles.statValue}>€{stats.total_eur_saved}</Text>
              <Text style={styles.statLabel}>Earned</Text>
            </View>
            <View style={styles.statBox}>
              <Text style={styles.statValue}>{stats.total_green_points}</Text>
              <Text style={styles.statLabel}>Points</Text>
            </View>
          </View>
        </View>
      )}

      {/* Schedule Button */}
      <TouchableOpacity
        style={styles.scheduleButton}
        onPress={handleScheduleSession}
      >
        <Text style={styles.scheduleButtonText}>
          📅 Schedule New Session
        </Text>
      </TouchableOpacity>

      {/* Sessions List */}
      <View style={styles.sessionsCard}>
        <Text style={styles.cardTitle}>Your Sessions</Text>

        {sessions.length === 0 ? (
          <View style={styles.emptyState}>
            <Text style={styles.emptyIcon}>⚡</Text>
            <Text style={styles.emptyText}>
              No sessions yet. Schedule your first session!
            </Text>
          </View>
        ) : (
          sessions.map((session) => (
            <SessionItem
              key={session.session_id}
              session={session}
              onStart={() => handleStartSession(session.session_id)}
              onComplete={() => handleCompleteSession(session.session_id)}
            />
          ))
        )}
      </View>
    </ScrollView>
  );
};

const SessionItem = ({ session, onStart, onComplete }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'SCHEDULED':
        return '#2196F3';
      case 'IN_PROGRESS':
        return '#FF9800';
      case 'COMPLETED':
        return '#4CAF50';
      case 'FAILED':
        return '#F44336';
      default:
        return '#999';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'SCHEDULED':
        return '📅';
      case 'IN_PROGRESS':
        return '⚡';
      case 'COMPLETED':
        return '✅';
      case 'FAILED':
        return '❌';
      default:
        return '❓';
    }
  };

  return (
    <View style={styles.sessionItem}>
      <View style={styles.sessionHeader}>
        <View>
          <Text style={styles.sessionDate}>
            {formatDateTime(session.scheduled_start)}
          </Text>
          <View style={styles.statusBadge}>
            <Text style={[styles.statusDot, { color: getStatusColor(session.status) }]}>
              {getStatusIcon(session.status)}
            </Text>
            <Text style={[styles.statusText, { color: getStatusColor(session.status) }]}>
              {session.status}
            </Text>
          </View>
        </View>

        {session.status === 'COMPLETED' && (
          <View style={styles.sessionResults}>
            <Text style={styles.resultValue}>+{session.saved_kwh} kWh</Text>
            <Text style={styles.resultLabel}>€{session.saved_eur}</Text>
          </View>
        )}
      </View>

      {session.status === 'SCHEDULED' && (
        <TouchableOpacity style={styles.actionButton} onPress={onStart}>
          <Text style={styles.actionButtonText}>Start Session</Text>
        </TouchableOpacity>
      )}

      {session.status === 'IN_PROGRESS' && (
        <TouchableOpacity
          style={[styles.actionButton, styles.completeButton]}
          onPress={onComplete}
        >
          <Text style={styles.actionButtonText}>Complete Session</Text>
        </TouchableOpacity>
      )}

      {session.status === 'COMPLETED' && session.green_points_earned > 0 && (
        <View style={styles.pointsBadge}>
          <Text style={styles.pointsText}>
            🌟 +{session.green_points_earned} points
          </Text>
        </View>
      )}
    </View>
  );
};

const formatDateTime = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString('en-GB', {
    weekday: 'short',
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  statsCard: {
    backgroundColor: '#FFFFFF',
    margin: 16,
    padding: 20,
    borderRadius: 12,
  },
  statsTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  statBox: {
    width: '48%',
    backgroundColor: '#F5F5F5',
    padding: 16,
    borderRadius: 8,
    marginBottom: 12,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  scheduleButton: {
    backgroundColor: '#4CAF50',
    margin: 16,
    marginTop: 0,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  scheduleButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  sessionsCard: {
    backgroundColor: '#FFFFFF',
    margin: 16,
    marginTop: 0,
    padding: 20,
    borderRadius: 12,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  emptyIcon: {
    fontSize: 48,
    marginBottom: 12,
  },
  emptyText: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
  },
  sessionItem: {
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
    paddingVertical: 16,
  },
  sessionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  sessionDate: {
    fontSize: 15,
    color: '#333',
    fontWeight: '500',
    marginBottom: 6,
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusDot: {
    fontSize: 12,
    marginRight: 6,
  },
  statusText: {
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'uppercase',
  },
  sessionResults: {
    alignItems: 'flex-end',
  },
  resultValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  resultLabel: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  actionButton: {
    backgroundColor: '#2196F3',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  completeButton: {
    backgroundColor: '#4CAF50',
  },
  actionButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
  },
  pointsBadge: {
    backgroundColor: '#FFF3E0',
    padding: 8,
    borderRadius: 6,
    marginTop: 8,
    alignItems: 'center',
  },
  pointsText: {
    color: '#F57C00',
    fontSize: 14,
    fontWeight: '500',
  },
});

export default SessionsScreen;
