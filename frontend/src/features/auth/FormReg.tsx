import { useForm } from "react-hook-form";
import axios from "axios";
import { CHECK_ICON_BASE64 } from "../../constants/icons";
import SocialAuth from "@/components/ui/SocialAuth";
import Divider from "@/components/ui/Divider";
import InputFieldForm from "@/components/ui/InputFieldForm";

const FormReg: React.FC = () => {
  const { register, handleSubmit, watch, formState: { errors } } = useForm();

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
          <SocialAuth network="yandex" />
          <SocialAuth network="vk" />
          <SocialAuth network="github" />
        </div>
        <Divider text="или" />
        <InputFieldForm
          type='email'
          name='email'
          placeholder='Введите e-mail'
          register={register}
          required='Это поле обязательно'
          error={errors.email}
          pattern={{
            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
            message: 'Некорректный email адрес'
          }}
        />
        <InputFieldForm
          type='password'
          name='password'
          placeholder='Введите пароль'
          register={register}
          required='Это поле обязательно'
          error={errors.password}
          minLength={{
            value: 8,
            message: "Пароль должен содержать минимум 8 символов"
          }}
        />
        <InputFieldForm
          type='password'
          name='confirmPassword'
          placeholder='Повторите пароль'
          register={register}
          required='Это поле обязательно'
          error={errors.confirmPassword}
          validateWith="password"
          watch={watch}
        />
        <label className='flex gap-2 items-center cursor-pointer'>
          <input
            type="checkbox"
            className={`appearance-none w-5 h-5 border border-gray-300 cursor-pointer rounded-sm checked:bg-blue-500 checked:border-blue-600 ${CHECK_ICON_BASE64} checked:bg-[length:14px_14px] checked:bg-center checked:bg-no-repeat`}
          />
          Я принимаю
          <a href="!#">
            условия
          </a>
        </label>
        <div
          className='flex flex-col gap-2.5 items-center'
        >
          <button type='submit' className='!bg-blue-600 text-white w-full'>
            Зарегистрироваться
          </button>
          <p>
            Уже есть аккаунт?
            <a href="#" className="ml-1">
              Войти
            </a>
          </p>
        </div>
      </form >
    </>
  )
};

export default FormReg;
