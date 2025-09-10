export interface User {
  id: number;
  name: string;
  email: string;
  joined_at: string;
  bio?: string;
}

export interface Subscription {
  status: 'active' | 'inactive' | 'expired';
  plan: string;
  expires_at: string;
}

export interface LoginHistoryItem {
  date: string;
  ip: string;
  device: string;
}

export interface PageProps {
  user: User;
  subscription: Subscription;
  loginHistory: LoginHistoryItem[];
}

export type PasswordForm = {
  currentPassword: string;
  newPassword: string;
  newPasswordConfirmation: string;
};
