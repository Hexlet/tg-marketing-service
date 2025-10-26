export interface User {
  first_name: string;
  email: string;
  company: string;
}

export type UserProfileErrors = Record<string, { message: string; code: string }[]>;

export interface UserProfileProps {
  user: User;
  errors?: UserProfileErrors;
  [key: string]: unknown;
}