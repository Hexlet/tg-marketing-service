import { useState } from 'react';
import type { UserProfileProps, User } from '@/features/userProfile/model/types';

/**
 * Мок для usePage — возвращает тестовые данные, имитируя ответ от Inertia.
 */
export const usePage = <T extends UserProfileProps>() => {
  const mockPage: { props: T } = {
    props: {
      user: {
        first_name: 'Иван',
        email: 'ivan@example.com',
        company: 'ООО Пример',
      },
      errors: {}, // имитация serverErrors
    } as T,
  };

  return mockPage;
};

/**
 * Мок для useForm — имитирует работу формы Inertia.
 */
export const useForm = <T extends User>(initialData: T) => {
  const [data, setDataState] = useState<T>(initialData);
  const [processing, setProcessing] = useState(false);

  const setData = <K extends keyof T>(key: K, value: T[K]) => {
    setDataState((prev) => ({ ...prev, [key]: value }));
  };

  const post = (
    url: string,
    {
      onSuccess,
      onError,
    }: {
      onSuccess?: () => void;
      onError?: (errors: Record<string, string>) => void;
    } = {}
  ) => {
    setProcessing(true);

    // имитация сетевого запроса
    setTimeout(() => {
      setProcessing(false);

      // Пример: если email содержит "error", возвращаем ошибку
      if (data.email.includes('error')) {
        onError?.({
          email: 'Некорректный email',
        });
      } else {
        onSuccess?.();
      }
    }, 1000);
  };

  return {
    data,
    setData,
    post,
    processing,
  };
};