import type { UserProfileErrors } from '../model/types';

export const mapServerErrors = (serverErrors: UserProfileErrors) => {
  return Object.entries(serverErrors).reduce<Record<string, string>>(
    (acc, [key, value]) => {
      acc[key] = Array.isArray(value) ? value[0].message : String(value);
      return acc;
    },
    {}
  );
};
