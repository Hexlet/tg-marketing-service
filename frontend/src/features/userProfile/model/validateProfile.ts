import type { User } from './types';

export const validateProfile = (data: User) => {
  const PrErrors: Record<string, string> = {};
  if (!data.first_name.trim()) PrErrors.first_name = 'Имя обязательно';
  if (!data.email.trim()) PrErrors.email = 'Email обязателен';
  return PrErrors;
};
