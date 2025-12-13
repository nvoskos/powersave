/**
 * App Context
 *
 * Global state management using React Context
 */
import React, { createContext, useContext, useState, useEffect } from 'react';
import { getUserId, walletAPI, sessionsAPI } from '../services/api';

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [userId, setUserId] = useState(null);
  const [user, setUser] = useState(null);
  const [walletBalance, setWalletBalance] = useState(0);
  const [totalKwhSaved, setTotalKwhSaved] = useState(0);
  const [greenPoints, setGreenPoints] = useState(0);
  const [loading, setLoading] = useState(true);

  // Load user data on mount
  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      const storedUserId = await getUserId();
      if (storedUserId) {
        setUserId(storedUserId);
        await refreshUserData(storedUserId);
      }
    } catch (error) {
      console.error('Failed to load user data:', error);
    } finally {
      setLoading(false);
    }
  };

  const refreshUserData = async (uid) => {
    try {
      const [walletRes, statsRes] = await Promise.all([
        walletAPI.getBalance(uid),
        sessionsAPI.getUserStats(uid),
      ]);

      setWalletBalance(walletRes.data.current_balance);
      setTotalKwhSaved(statsRes.data.total_kwh_saved);
      setGreenPoints(statsRes.data.total_green_points);
    } catch (error) {
      console.error('Failed to refresh user data:', error);
    }
  };

  const value = {
    userId,
    setUserId,
    user,
    setUser,
    walletBalance,
    setWalletBalance,
    totalKwhSaved,
    setTotalKwhSaved,
    greenPoints,
    setGreenPoints,
    loading,
    refreshUserData,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within AppProvider');
  }
  return context;
};
