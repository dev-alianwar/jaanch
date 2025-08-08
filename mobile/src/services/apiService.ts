import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { Platform } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Configure API base URL
const API_BASE_URL = Platform.OS === 'web' 
  ? 'http://localhost:8000' 
  : 'http://10.0.2.2:8000'; // Android emulator, use your IP for iOS

interface LoginResponse {
  user: {
    id: string;
    email: string;
    role: 'customer' | 'business' | 'superadmin';
    first_name: string;
    last_name: string;
    phone?: string;
    is_active: boolean;
  };
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

interface RegisterData {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone?: string;
  role: 'customer' | 'business';
}

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.api.interceptors.request.use(
      (config) => {
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle token refresh
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = await AsyncStorage.getItem('refresh_token');
            if (refreshToken) {
              const response = await this.refreshToken(refreshToken);
              
              // Update stored tokens
              await AsyncStorage.multiSet([
                ['access_token', response.access_token],
                ['refresh_token', response.refresh_token],
              ]);
              
              // Update authorization header
              this.setAuthToken(response.access_token);
              originalRequest.headers.Authorization = `Bearer ${response.access_token}`;
              
              // Retry original request
              return this.api(originalRequest);
            }
          } catch (refreshError) {
            // Refresh failed, redirect to login
            await AsyncStorage.multiRemove(['access_token', 'refresh_token']);
            this.clearAuthToken();
            // You might want to emit an event here to trigger logout in the app
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  setAuthToken(token: string) {
    this.api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  clearAuthToken() {
    delete this.api.defaults.headers.common['Authorization'];
  }

  // Authentication endpoints
  async login(email: string, password: string): Promise<LoginResponse> {
    const response: AxiosResponse<LoginResponse> = await this.api.post('/auth/login', {
      email,
      password,
    });
    return response.data;
  }

  async register(userData: RegisterData): Promise<LoginResponse> {
    const response: AxiosResponse<LoginResponse> = await this.api.post('/auth/register', userData);
    return response.data;
  }

  async logout(): Promise<void> {
    await this.api.post('/auth/logout');
  }

  async refreshToken(refreshToken: string): Promise<LoginResponse> {
    const response: AxiosResponse<LoginResponse> = await this.api.post('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.api.get('/auth/me');
    return response.data;
  }

  // Business endpoints
  async getVerifiedBusinesses() {
    const response = await this.api.get('/installments/businesses');
    return response.data;
  }

  // Installment request endpoints
  async createInstallmentRequest(requestData: any) {
    const response = await this.api.post('/installments/requests', requestData);
    return response.data;
  }

  async getMyRequests(page = 1, size = 10, status?: string) {
    const params = new URLSearchParams({ page: page.toString(), size: size.toString() });
    if (status) params.append('status_filter', status);
    
    const response = await this.api.get(`/installments/my-requests?${params}`);
    return response.data;
  }

  async getBusinessRequests(page = 1, size = 10, status?: string) {
    const params = new URLSearchParams({ page: page.toString(), size: size.toString() });
    if (status) params.append('status_filter', status);
    
    const response = await this.api.get(`/installments/business-requests?${params}`);
    return response.data;
  }

  // Approval endpoints
  async approveRequest(requestId: string, notes?: string) {
    const response = await this.api.post(`/approvals/requests/${requestId}/approve`, {
      business_notes: notes,
    });
    return response.data;
  }

  async rejectRequest(requestId: string, notes: string) {
    const response = await this.api.post(`/approvals/requests/${requestId}/reject`, {
      business_notes: notes,
    });
    return response.data;
  }

  async getCustomerHistory(customerId: string) {
    const response = await this.api.get(`/approvals/customer-history/${customerId}`);
    return response.data;
  }

  // History endpoints
  async getMyHistory() {
    const response = await this.api.get('/history/my-history');
    return response.data;
  }

  async getActivePlans(page = 1, size = 10) {
    const params = new URLSearchParams({ page: page.toString(), size: size.toString() });
    const response = await this.api.get(`/history/active-plans?${params}`);
    return response.data;
  }

  // Admin endpoints (superadmin only)
  async getDashboardOverview() {
    const response = await this.api.get('/admin/dashboard/overview');
    return response.data;
  }

  async getSystemMetrics(period = '30d') {
    const response = await this.api.get(`/admin/dashboard/metrics?period=${period}`);
    return response.data;
  }

  async getFraudSummary() {
    const response = await this.api.get('/admin/dashboard/fraud-summary');
    return response.data;
  }

  // Fraud detection endpoints
  async analyzeCustomerRisk(customerId: string) {
    const response = await this.api.post(`/fraud/analyze/${customerId}`);
    return response.data;
  }

  async getFraudAlerts(page = 1, size = 10) {
    const params = new URLSearchParams({ page: page.toString(), size: size.toString() });
    const response = await this.api.get(`/fraud/alerts?${params}`);
    return response.data;
  }

  // Error handling helper
  handleApiError(error: any): string {
    if (error.response?.data?.error?.message) {
      return error.response.data.error.message;
    } else if (error.response?.data?.detail) {
      return error.response.data.detail;
    } else if (error.message) {
      return error.message;
    } else {
      return 'An unexpected error occurred';
    }
  }
}

export const apiService = new ApiService();