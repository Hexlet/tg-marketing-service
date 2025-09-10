import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Input } from '@/components/ui/input';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
// import { Head, usePage } from '@inertiajs/react';
// import { Inertia } from '@inertiajs/inertia';

export default function Profile() {
  // const { user, subscription, loginHistory } = usePage<PageProps>().props;
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<PasswordForm>();

  const [avatar, setAvatar] = useState<File | null>(null);
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null);

  const user = {
    id: 1,
    name: 'Иван Иванов',
    email: 'ivan@example.com',
    joined_at: '2024-01-15',
    bio: 'Люблю React',
  };

  const subscription = {
    status: 'active' as const,
    plan: 'Pro',
    expires_at: '2025-12-31',
  };

  const loginHistory = [
    { date: '2025-09-01', ip: '192.168.0.1', device: 'Chrome' },
    { date: '2025-09-05', ip: '192.168.0.2', device: 'Safari' },
  ];

  const onSubmit = (data: PasswordForm) => {
    console.log('Пароль изменён', data);
  };

  const handleLogout = () => {
    console.log('Выход');
  };
  return (
    <>
      {/* <Head title={`Профиль ${user.name}`} />Закомментирован, так как подтягивается от inertiajs/react */}
      <div className="p-6 max-w-xl mx-auto space-y-6">
        <h1 className="text-2xl font-bold">Профиль</h1>

        {/* Фото */}
        <div className="space-y-2">
          <h2 className="text-lg font-semibold">Фото</h2>
          <Avatar className="w-24 h-24">
            <AvatarImage src={avatarPreview} alt="Превью аватара" />
            <AvatarFallback>Аватар</AvatarFallback>
          </Avatar>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => {
              if (e.target.files && e.target.files[0]) {
                const file = e.target.files[0];
                setAvatar(file);
                setAvatarPreview(URL.createObjectURL(file));
              }
            }}
          />
          <button
            onClick={() => {
              if (avatar) {
                console.log('Файл выбран:', avatar);
              }
            }}
            disabled={!avatar}
          >
            Сохранить аватар
          </button>
        </div>

        {/* Данные пользователя */}
        <div className="space-y-1">
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
        </div>

        {/* Подписка */}
        <div className="subscription">
          <h2 className="text-lg font-semibold">Статус подписки</h2>
          <p>План: {subscription.plan}</p>
          <p>Статус: {subscription.status}</p>
          <p>Срок действия: {subscription.expires_at}</p>
        </div>

        {/* История заходов */}
        <div className="login-history">
          <h2 className="text-lg font-semibold">История заходов</h2>
          <ul className="list-disc list-inside">
            {loginHistory.map((item, index) => (
              <li key={index}>
                {item.date} - {item.ip} - {item.device}
              </li>
            ))}
          </ul>
        </div>

        {/* Смена пароля */}
        <div className="change-password">
          <h2 className="text-lg font-semibold">Смена пароля</h2>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-3">
            <Input
              type="password"
              placeholder="Текущий пароль"
              {...register('currentPassword', {
                required: 'Введите текущий пароль',
              })}
            />
            {errors.currentPassword && (
              <p className="text-red-500">{errors.currentPassword.message}</p>
            )}
            <Input
              type="password"
              placeholder="Новый пароль"
              {...register('newPassword', {
                required: 'Введите новый пароль',
                minLength: {
                  value: 6,
                  message: 'Пароль должен быть минимум 6 символов',
                },
              })}
            />
            <Input
              type="password"
              placeholder="Подтвердите новый пароль"
              {...register('newPasswordConfirmation', {
                validate: (value, formValues) =>
                  value === formValues.newPassword || 'Пароли не совпадают',
              })}
            />
            {errors.newPasswordConfirmation && (
              <p className="text-red-500">
                {errors.newPasswordConfirmation.message}
              </p>
            )}
            <button type="submit">Сменить пароль</button>
          </form>
        </div>

        {/* Выход */}
        <div className="logout">
          <button onClick={handleLogout}>Выйти</button>
        </div>
      </div>
    </>
  );
}
