import type { UserProfileErrors } from '../model/types';

export const mapServerErrors = (serverErrors: UserProfileErrors) => {
  const flatErrors: Record<string, string> = {};
  Object.entries(serverErrors).forEach(([key, value]) => {
    flatErrors[key] = Array.isArray(value) ? value[0].message : String(value);
    });
    return flatErrors;
};