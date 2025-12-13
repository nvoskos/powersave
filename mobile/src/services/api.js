/**
 * API Service
 *
 * Central service for all API calls to PowerSave backend
 */
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// API Configuration
const API_BASE_URL = __DEV__
  ? 'http://localhost:8000/api/v1'  // Development
  : 'https://api.powersave.cy/api/v1';  // Production

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor (add auth token)
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor (handle errors)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, logout user
      await AsyncStorage.removeItem('authToken');
      await AsyncStorage.removeItem('userId');
    }
    return Promise.reject(error);
  }
);

/**
 * Authentication API
 */
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  registerProperty: (userId, propertyData) =>
    api.post(`/auth/register-property?user_id=${userId}`, propertyData),
  getUser: (userId) => api.get(`/auth/users/${userId}`),
};

/**
 * Waste Wallet API
 */
export const walletAPI = {
  getBalance: (userId) => api.get(`/wallet/${userId}/balance`),
  getTransactions: (userId, params = {}) =>
    api.get(`/wallet/${userId}/transactions`, { params }),
  getCoverage: (userId) => api.get(`/wallet/${userId}/coverage`),
  getMonthlySummary: (userId, year, month) =>
    api.get(`/wallet/${userId}/summary/${year}/${month}`),
  donate: (userId, amount, fundId) =>
    api.post(`/wallet/${userId}/donate`, {
      amount,
      recipient_fund_id: fundId,
    }),
};

/**
 * Saving Sessions API
 */
export const sessionsAPI = {
  createSession: (userId, sessionData) =>
    api.post(`/sessions?user_id=${userId}`, sessionData),
  getSession: (sessionId) => api.get(`/sessions/${sessionId}`),
  getUserSessions: (userId, params = {}) =>
    api.get(`/sessions/user/${userId}`, { params }),
  startSession: (sessionId) => api.post(`/sessions/${sessionId}/start`),
  completeSession: (sessionId, actualConsumption) =>
    api.post(`/sessions/${sessionId}/complete`, {
      actual_consumption_kwh: actualConsumption,
    }),
  getUserStats: (userId) => api.get(`/sessions/user/${userId}/stats`),
};

/**
 * Helper functions
 */
export const setAuthToken = async (token) => {
  await AsyncStorage.setItem('authToken', token);
};

export const setUserId = async (userId) => {
  await AsyncStorage.setItem('userId', userId);
};

export const getUserId = async () => {
  return await AsyncStorage.getItem('userId');
};

export const logout = async () => {
  await AsyncStorage.removeItem('authToken');
  await AsyncStorage.removeItem('userId');
};

export default api;
