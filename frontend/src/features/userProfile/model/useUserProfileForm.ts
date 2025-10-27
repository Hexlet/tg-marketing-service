import React, { useEffect, useState } from 'react';
import { useForm, usePage } from '@inertiajs/react';
import { mapServerErrors } from '../libr/mapServerErrors';
import { validateProfile } from './validateProfile';
import type { User, UserProfileProps } from './types';

export const useUserProfileForm = () => {
  const { user, errors: serverErrors = {} } = usePage<UserProfileProps>().props;
  
  const [errors, setErrors] = useState<Record<string, string>>({});

  const { data, setData, post, processing } = useForm<User>({
    first_name: user.first_name || '',
    email: user.email || '',
    company: user.company || '',
  });

  useEffect(() => {
    setErrors(mapServerErrors(serverErrors));
  }, [serverErrors]);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const newErrors = validateProfile(data);
    if (Object.keys(newErrors).length) {
      setErrors(prev => ({ ...prev, ...newErrors }));
      return;
    }

    post('/auth/profile', {
      onSuccess: () => console.log('Profile updated successfully'),
      onError: (serverErrors) => {
        console.log('Error updating the profile', serverErrors);
      },
    });
  };

  return { data, setData, errors, setErrors, handleSubmit, processing };
};