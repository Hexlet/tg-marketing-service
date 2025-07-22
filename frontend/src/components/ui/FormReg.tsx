import { useForm } from "react-hook-form";
import axios from "axios";
import { SocialIcon } from "react-social-icons";
import { CHECK_ICON_BASE64 } from "../../constants/icons";

const FormReg: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();

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
            Регистрация
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
          {...register("email", {
            required: 'Это поле обязательно',
          })}
          type="email"
          placeholder='E-mail'
          className='border-1 rounded-sm pl-3 pt-2 pb-2'
        />
        {errors.email && (
          <span className='text-red-500'>
            {typeof errors.email.message === 'string' ? errors.email.message : "Неверный email"}
          </span>
        )}
        <input
          {...register("password", {
            required: 'Это поле обязательно',
          })}
          type="password"
          placeholder='Пароль'
          className='border-1 rounded-sm pl-3 pt-2 pb-2'
        />
        {errors.password && (
          <span className='text-red-500'>
            {typeof errors.password.message === 'string' ? errors.password.message : "Неверный пароль"}
          </span>
        )}
        <input
          {...register("password", {
            required: 'Это поле обязательно',
          })}
          type="password"
          placeholder='Повторите пароль'
          className='border-1 rounded-sm pl-3 pt-2 pb-2'
        />
        {errors.password && (
          <span className='text-red-500'>
            {typeof errors.password.message === 'string' ? errors.password.message : "Неверный пароль"}
          </span>
        )}
        <label className='flex gap-2 items-center cursor-pointer'>
          <input
            type="checkbox"
            className={`appearance-none w-5 h-5 border border-gray-300 cursor-pointer rounded-sm checked:bg-blue-500 checked:border-blue-600 ${CHECK_ICON_BASE64} checked:bg-[length:14px_14px] checked:bg-center checked:bg-no-repeat`}
          />
          Я принимаю условия
        </label>
        <div
          className='flex flex-col gap-2.5 items-center'
        >
          <button type='submit' className='!bg-blue-600 text-white w-full'>
            Зарегистрироваться
          </button>
          <p>
            Уже есть аккаунт?
            <a href="#">
              Войти
            </a>
          </p>
        </div>
      </form>
    </>
  )
};

export default FormReg;
