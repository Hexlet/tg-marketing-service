import React from 'react';
import { useUserProfileForm } from '../model/useUserProfileForm';

export const ProfileForm: React.FC = () => {
  const { data, setData, errors, setErrors, handleSubmit, processing } = useUserProfileForm();

  return (
    <div className="flex flex-col gap-6">
      {/* Верхняя строка: Информация о профиле и Подписка Pro */}
      <div className="flex flex-col md:flex-row gap-6">
        {/* Информация о профиле - 2/3 ширины */}
        <form 
          onSubmit={handleSubmit} 
          className="bg-white border border-gray-300 shadow-sm rounded p-6 space-y-4 w-full md:w-2/3"
        >
          <h3 className="text-2xl font-semibold text-gray-800 mb-4 text-left">
            Информация о профиле
          </h3>

          {/* Имя и Email */}
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <label className="block text-gray-700 font-medium mb-1">Имя</label>
              <input
                type="text"
                value={data.first_name}
                onChange={(e) => {
                  setData('first_name', e.target.value);
                  setErrors(prev => ({ ...prev, first_name: '' }));
                }}
                className="border border-gray-300 rounded p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {errors.first_name && <p className="text-red-500 text-sm mt-1">{errors.first_name}</p>}
            </div>

            <div className="flex-1">
              <label className="block text-gray-700 font-medium mb-1">Email</label>
              <input
                type="email"
                value={data.email}
                onChange={(e) => {
                  setData('email', e.target.value);
                  setErrors(prev => ({ ...prev, email: '' }));
                }}
                className="border border-gray-300 rounded p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email}</p>}
            </div>
          </div>

          {/* Компания */}
          <div>
            <label className="block text-gray-700 font-medium mb-1">Компания</label>
            <input
              type="text"
              value={data.company}
              onChange={(e) => {
                setData('company', e.target.value);
                setErrors(prev => ({ ...prev, company: '' }));
              }}
              className="border border-gray-300 rounded p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            {errors.company && <p className="text-red-500 text-sm mt-1">{errors.company}</p>}
          </div>

          <button
            type="submit"
            disabled={processing}
            className="bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold rounded-lg px-6 py-2 shadow-md disabled:opacity-50 transition-colors duration-200"
          >
            {processing ? 'Сохранение...' : 'Сохранить изменения'}
          </button>
        </form>

        {/* Подписка Pro - 1/3 ширины */}
        <div className="bg-white border border-gray-300 shadow-sm rounded p-6 w-full md:w-1/3">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4 text-left">Подписка Pro</h3>
          <p className="text-gray-500">Заглушка для формы подписки.</p>
        </div>
      </div>

      {/* Нижняя строка: Уведомления и Статистика использования */}
      <div className="flex flex-col md:flex-row gap-6">
        {/* Уведомления - ширина как Информация о профиле */}
        <div className="bg-white border border-gray-300 shadow-sm rounded p-6 w-full md:w-2/3">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4 text-left">Уведомления</h3>
          <p className="text-gray-500">Заглушка для формы уведомлений.</p>
        </div>

        {/* Статистика использования - оставшееся место */}
        <div className="bg-white border border-gray-300 shadow-sm rounded p-6 w-full md:w-1/3">
          <h3 className="text-2xl font-semibold text-gray-800 mb-4 text-left">Статистика использования</h3>
          <p className="text-gray-500">Заглушка для статистики.</p>
        </div>
      </div>
    </div>
  );
};
