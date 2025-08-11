import React from "react";
import { useForm } from "react-hook-form";
import { useState } from "react";

interface PasswordRecoveryProps {
  isVisible: boolean;
  onClose: () => void;
}

const PasswordRecovery: React.FC<PasswordRecoveryProps> = ({ isVisible, onClose }) => {
  const { register, handleSubmit, formState: { errors }, reset } = useForm();

  const [showSuccess, setShowSuccess] = useState(false);

  const onSubmit = () => {
    setShowSuccess(true);

    setTimeout(() => {
      setShowSuccess(false);
      onClose();
      reset();
    }, 2000);
  };

  if (!isVisible) return null;

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
      reset();
    }
  };

  const handleCancel = () => {
    onClose();
    reset();
  };

  return (
    <div className="fixed inset-0 bg-neutral-800 flex items-center justify-center z-50" onClick={handleBackdropClick}>
      {showSuccess ? (
        <div className="bg-white rounded-lg p-6 max-w-md text-center">
          <h2 className="text-2xl mb-4 font-bold text-green-600">Успешно!</h2>
          <p className="mb-4">Проверьте вашу почту для восстановления пароля</p>
        </div>
      ) : (
        <form
          onSubmit={handleSubmit(onSubmit)}
          className="rounded-lg p-5 bg-white w-sm"
        >
          <h2 className="text-2xl mb-1 font-bold">
            Восстановление пароля
          </h2>
          <label className="text-sm flex flex-col gap-2.5 mb-4">
            Введите ваш email
            <input
              {...register("email", {
                required: "Это поле обязательно",
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: "Некорректный email"
                }
              })}
              type="email"
              placeholder="E-mail"
              className="border-1 rounded-sm w-full pl-4 pt-2 pb-2"
            />
            {errors.email && (
              <span className="text-red-500 text-xs">
                {typeof errors.email.message === 'string' ? errors.email.message : 'Неверный email'}
              </span>
            )}
          </label>
          <div className="flex justify-between">
            <button className="!bg-blue-600 text-white">
              Отправить ссылку
            </button>
            <button
              type="button"
              onClick={() => handleCancel()}
              className="!bg-white">
              Отмена
            </button>
          </div>
        </form >
      )}
    </div >
  )
}

export default PasswordRecovery;
