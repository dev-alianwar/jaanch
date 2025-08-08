export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: 'customer' | 'business' | 'superadmin';
  phone?: string;
  isActive: boolean;
  createdAt: string;
  business?: Business;
}

export interface Business {
  id: string;
  businessName: string;
  businessType: string;
  address: string;
  phone: string;
  registrationNumber: string;
  isVerified: boolean;
  createdAt: string;
}

export interface InstallmentRequest {
  id: string;
  customerId: string;
  businessId: string;
  productName: string;
  productDescription: string;
  productValue: number;
  installmentMonths: number;
  monthlyAmount: number;
  status: 'pending' | 'approved' | 'rejected';
  businessNotes?: string;
  createdAt: string;
  updatedAt: string;
  customer?: User;
  business?: Business;
}

export interface InstallmentPlan {
  id: string;
  requestId: string;
  totalAmount: number;
  paidAmount: number;
  remainingAmount: number;
  totalInstallments: number;
  paidInstallments: number;
  startDate: string;
  endDate: string;
  status: 'active' | 'completed' | 'defaulted';
  createdAt: string;
}

export interface FraudAlert {
  id: string;
  customerId: string;
  alertType: string;
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'active' | 'resolved' | 'dismissed';
  createdAt: string;
  resolvedAt?: string;
}

export interface AuthResponse {
  user: User;
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  phone?: string;
  role: 'customer' | 'business';
  businessName?: string;
  businessType?: string;
  address?: string;
  registrationNumber?: string;
}