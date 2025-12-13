/**
 * Waste Wallet Screen
 *
 * Shows current balance, coverage percentage, and transaction history
 */
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  TouchableOpacity,
  RefreshControl,
} from 'react-native';
import { walletAPI } from '../services/api';
import { useApp } from '../context/AppContext';

const WasteWalletScreen = ({ navigation }) => {
  const { userId } = useApp();
  const [balance, setBalance] = useState(null);
  const [coverage, setCoverage] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadData();
  }, [userId]);

  const loadData = async () => {
    if (!userId) return;

    try {
      setLoading(true);
      const [balanceRes, coverageRes, transactionsRes] = await Promise.all([
        walletAPI.getBalance(userId),
        walletAPI.getCoverage(userId),
        walletAPI.getTransactions(userId, { limit: 10 }),
      ]);

      setBalance(balanceRes.data);
      setCoverage(coverageRes.data);
      setTransactions(transactionsRes.data);
    } catch (error) {
      console.error('Failed to load wallet data:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
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
      {/* Balance Card */}
      <View style={styles.balanceCard}>
        <Text style={styles.balanceLabel}>Waste Wallet Balance</Text>
        <Text style={styles.balanceAmount}>€{balance?.current_balance || 0}</Text>
        <Text style={styles.balanceSubtext}>
          Total Earned: €{balance?.total_earned || 0}
        </Text>
      </View>

      {/* Coverage Card */}
      {coverage && (
        <View style={styles.coverageCard}>
          <Text style={styles.cardTitle}>Waste Fee Coverage</Text>

          {/* Progress Bar */}
          <View style={styles.progressBarContainer}>
            <View
              style={[
                styles.progressBar,
                { width: `${Math.min(coverage.coverage_percentage, 100)}%` },
              ]}
            />
          </View>

          <View style={styles.coverageStats}>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>
                {coverage.coverage_percentage}%
              </Text>
              <Text style={styles.statLabel}>Covered</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>
                {coverage.months_covered} mo
              </Text>
              <Text style={styles.statLabel}>Months</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>
                €{coverage.remaining_to_cover}
              </Text>
              <Text style={styles.statLabel}>Remaining</Text>
            </View>
          </View>

          {coverage.coverage_percentage >= 100 ? (
            <View style={styles.successBanner}>
              <Text style={styles.successText}>
                🎉 Waste fee fully covered!
              </Text>
            </View>
          ) : (
            <View style={styles.tipBox}>
              <Text style={styles.tipText}>
                💡 Complete {Math.ceil((coverage.remaining_to_cover / 0.18))} more sessions to cover 100%
              </Text>
            </View>
          )}
        </View>
      )}

      {/* Transaction History */}
      <View style={styles.transactionsCard}>
        <View style={styles.cardHeader}>
          <Text style={styles.cardTitle}>Recent Transactions</Text>
          <TouchableOpacity onPress={() => navigation.navigate('AllTransactions')}>
            <Text style={styles.seeAllText}>See All</Text>
          </TouchableOpacity>
        </View>

        {transactions.length === 0 ? (
          <Text style={styles.emptyText}>No transactions yet</Text>
        ) : (
          transactions.map((tx) => (
            <View key={tx.transaction_id} style={styles.transactionItem}>
              <View style={styles.transactionLeft}>
                <Text style={styles.transactionType}>
                  {tx.type === 'CREDIT' ? '💰' : '💸'} {formatTransactionType(tx.type)}
                </Text>
                <Text style={styles.transactionDate}>
                  {formatDate(tx.created_at)}
                </Text>
              </View>
              <View style={styles.transactionRight}>
                <Text
                  style={[
                    styles.transactionAmount,
                    tx.type === 'CREDIT' ? styles.creditAmount : styles.debitAmount,
                  ]}
                >
                  {tx.type === 'CREDIT' ? '+' : '-'}€{tx.amount}
                </Text>
                <Text style={styles.transactionBalance}>
                  Balance: €{tx.balance_after}
                </Text>
              </View>
            </View>
          ))
        )}
      </View>

      {/* Donation Button */}
      <TouchableOpacity
        style={styles.donateButton}
        onPress={() => navigation.navigate('Donate')}
      >
        <Text style={styles.donateButtonText}>
          ❤️ Donate to Energy Solidarity
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

// Helper functions
const formatTransactionType = (type) => {
  const types = {
    CREDIT: 'Savings Credit',
    DEBIT: 'Payment',
    DONATION: 'Donation',
    PAYMENT_TO_MUNICIPALITY: 'Waste Fee Payment',
  };
  return types[type] || type;
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
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
  balanceCard: {
    backgroundColor: '#4CAF50',
    margin: 16,
    padding: 24,
    borderRadius: 16,
    alignItems: 'center',
  },
  balanceLabel: {
    color: '#FFFFFF',
    fontSize: 16,
    opacity: 0.9,
  },
  balanceAmount: {
    color: '#FFFFFF',
    fontSize: 48,
    fontWeight: 'bold',
    marginVertical: 8,
  },
  balanceSubtext: {
    color: '#FFFFFF',
    fontSize: 14,
    opacity: 0.8,
  },
  coverageCard: {
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
  progressBarContainer: {
    height: 12,
    backgroundColor: '#E0E0E0',
    borderRadius: 6,
    overflow: 'hidden',
    marginBottom: 16,
  },
  progressBar: {
    height: '100%',
    backgroundColor: '#4CAF50',
  },
  coverageStats: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 16,
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  successBanner: {
    backgroundColor: '#E8F5E9',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  successText: {
    color: '#2E7D32',
    fontSize: 16,
    fontWeight: '600',
  },
  tipBox: {
    backgroundColor: '#FFF3E0',
    padding: 12,
    borderRadius: 8,
  },
  tipText: {
    color: '#E65100',
    fontSize: 14,
  },
  transactionsCard: {
    backgroundColor: '#FFFFFF',
    margin: 16,
    marginTop: 0,
    padding: 20,
    borderRadius: 12,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  seeAllText: {
    color: '#4CAF50',
    fontSize: 14,
    fontWeight: '600',
  },
  emptyText: {
    textAlign: 'center',
    color: '#999',
    fontSize: 14,
    paddingVertical: 20,
  },
  transactionItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  transactionLeft: {
    flex: 1,
  },
  transactionType: {
    fontSize: 15,
    color: '#333',
    fontWeight: '500',
  },
  transactionDate: {
    fontSize: 12,
    color: '#999',
    marginTop: 4,
  },
  transactionRight: {
    alignItems: 'flex-end',
  },
  transactionAmount: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  creditAmount: {
    color: '#4CAF50',
  },
  debitAmount: {
    color: '#F44336',
  },
  transactionBalance: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  donateButton: {
    backgroundColor: '#FF5722',
    margin: 16,
    marginTop: 0,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  donateButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default WasteWalletScreen;
