import React from 'react';
import { useState } from 'react';
import PasswordRecovery from '../modals/PasswordRecovery';
import { useForm } from "react-hook-form";
import axios from "axios";
import { SocialIcon } from "react-social-icons";

const FormAuth: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();

  console.log(errors);


  const [showModal, setShowModal] = useState(false);

  const openModal = () => {
    setShowModal(true);
  }

  const closeModal = () => {
    setShowModal(false);
  }

  const onSubmit = async (data: any) => {
    try {
      const response = await axios.post('https://2466feea1e3f0642.mokky.dev/items', data);
      console.log('Успешный ответ от сервера:', response.data);
    } catch {

    }
  }

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)} className='max-w-sm flex flex-col justify-center m-auto h-screen gap-3 p-5'>
        <div>
          <h2 className='font-bold text-center text-2xl mb-2'>
            Войти в систему
          </h2>
          <p className='text-center'>
            Используйте привычный способ входа
          </p>
        </div>
        <div className='flex gap-3 justify-center'>
          <a href='#' className='!p-0 cursor-pointer'>
            <SocialIcon network='yandex' style={{ height: 40, width: 40 }} ></SocialIcon>
          </a>
          <a href='#' className='!p-0 cursor-pointer'>
            <SocialIcon network='vk' style={{ height: 40, width: 40 }}></SocialIcon>
          </a>
          <a href='#' className='!p-0 cursor-pointer'>
            <SocialIcon network='github' style={{ height: 40, width: 40 }}></SocialIcon>
          </a>
        </div>
        <div className='flex items-center justify-between gap-2'>
          <span className='w-full h-px bg-gray-300 block'></span>
          <span className='text-lg text-gray-400'>
            или
          </span>
          <span className='w-full h-px bg-gray-300 block'></span>
        </div>
        <input
          {...register("email", { required: 'This is required.', })}
          type="email"
          placeholder='E-mail'
          className='border-1 rounded-sm pl-3 pt-2 pb-2'
        />
        <input
          {...register("password", { required: 'This is required.' })}
          type="password"
          placeholder='Пароль'
          className='border-1 rounded-sm pl-3 pt-2 pb-2'
        />
        <label className='flex gap-2 items-center cursor-pointer'>
          <input
            type="checkbox"
            className="appearance-none w-5 h-5 border border-gray-300 cursor-pointer rounded-sm checked:bg-blue-500 checked:border-blue-600 checked:bg-[url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgd2lkdGg9IjI0IiBoZWlnaHQ9IjI0Ij48cGF0aCBkPSJNOSAxNi4xN0w0LjgzIDEybC0xLjQyIDEuNDFMOSAxOSAyMSA3bC0xLjQxLTEuNDFMOSAxNi4xN3oiIGZpbGw9IndoaXRlIi8+PC9zdmc+)] checked:bg-[length:14px_14px] checked:bg-center checked:bg-no-repeat"
          />
          Запомнить меня
        </label>
        <div
          className='flex flex-col gap-2.5 items-center'
        >
          <button type='submit' className='!bg-blue-600 text-white w-full'>
            Войти
          </button>
          <button type='button' onClick={openModal} className='!bg-white w-max'>
            Забыли пароль?
          </button>
        </div>
      </form>
      <PasswordRecovery isVisible={showModal} onClose={closeModal} />
    </>
  )
}

export default FormAuth;
