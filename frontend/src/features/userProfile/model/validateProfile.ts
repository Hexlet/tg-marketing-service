import type { User } from './types';

export const validateProfile = (data: User) => {
  const errors: Record<string, string> = {};
  if (!data.first_name.trim()) errors.first_name = 'Имя обязательно';
  if (!data.email.trim()) errors.email = 'Email обязателен';
  return errors;
};
