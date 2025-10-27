import React from 'react';
import { ProfileForm } from '@/features/userProfile';

export const UserProfilePage: React.FC = () => (
  <div className="w-full p-6 text-left">
    <div className="mb-6">
      <h1 className="!text-3xl font-bold mb-1">Личный кабинет</h1>
      <h2 className="text-xl text-gray-600 mb-6">Управление аккаунтом и подпиской</h2>
    </div>
    <ProfileForm />
  </div>
);
