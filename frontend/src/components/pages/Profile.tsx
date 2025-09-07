import React, { useState } from 'react';
import { Head, usePage, Inertia } from '@inertiajs/react';

interface User {
  id: number;
  name: string;
  email: string;
  joined_at: string;
  bio?: string;
}

interface Subscription {
  status: 'active' | 'inactive' | 'expired';
  plan: string;
  expires_at: string;
}

interface LoginHistoryItem {
  date: string;
  ip: string;
  device: string;
}

interface PageProps {
  user: User;
  subscription: Subscription;
  loginHistory: LoginHistoryItem[];
}

export default function Profile() {
  const { user, subscription, loginHistory } = usePage<PageProps>().props;

  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newPasswordConfirmation, setnewPasswordConfirmation] = useState('');

  const handlePasswordChange = (e: React.FormEvent) => {
    e.preventDefault();
    Inertia.post('/user/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
      new_password_confirmation: newPasswordConfirmation,
    });
  };

  const handleLogout = () => {
    Inertia.post('/Logout');
  };
  return (
    <div className="profile-page">
      <Head title={`Профиль ${user.name}`} />
      <h1>Профиль</h1>
      <p>
        <strong>ID:</strong>
        {user.id}
      </p>
      <p>
        <strong>Имя:</strong>
        {user.name}
      </p>
      <p>
        <strong>Email:</strong>
        {user.email}
      </p>
      <p>
        <strong>Дата регистрации:</strong>
        {user.joined_at}
      </p>
      <p>
        <strong>О себе:</strong>
        {user.bio}
      </p>
      <div className="subscription">
        <h2>Статус подписки</h2>
        <p>План: {subscription.plan}</p>
        <p>Статус: {subscription.status}</p>
        <p>Срок действия: {subscription.expires_at}</p>
      </div>
      <div className="login-history">
        <h2>История заходов</h2>
        <ul>
          {loginHistory.map((item, index) => (
            <li key={index}>
              {item.date} - {item.ip} - {item.device}
            </li>
          ))}
        </ul>
      </div>
      <div className="change-password">
        <h2>Смена пароля</h2>
        <form onSubmit={handlePasswordChange}>
          <input
            type="password"
            placeholder="Текущий пароль"
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
          />
          <input
            type="password"
            placeholder="Новый пароль"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
          <input
            type="password"
            placeholder="Подтвердите новый пароль"
            value={newPasswordConfirmation}
            onChange={(e) => setnewPasswordConfirmation(e.target.value)}
          />
          <button type="submit">Сменить пароль</button>
        </form>
      </div>
      <div className="logout">
        <button onClick={handleLogout}>Выйти</button>
      </div>
    </div>
  );
}
