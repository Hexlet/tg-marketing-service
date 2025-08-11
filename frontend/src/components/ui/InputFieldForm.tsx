import React from "react";
import type { UseFormRegister, FieldError, Merge, FieldErrorsImpl, RegisterOptions, UseFormWatch } from "react-hook-form";

interface InputFieldFormProps {
  type: string;
  placeholder: string;
  register: UseFormRegister<any>;
  error?: FieldError | Merge<FieldError, FieldErrorsImpl<any>> | undefined;
  name: string;
  required: boolean | string;
  watch?: UseFormWatch<any>;
  validateWith?: string;
  pattern?: {
    value: RegExp;
    message: string;
  }
  minLength?: {
    value: number;
    message: string;
  }
}

const InputFieldForm: React.FC<InputFieldFormProps> = ({ type, placeholder, register, error, name, required, pattern, watch,
  validateWith, minLength }) => {

  const registerOptions: RegisterOptions = {
    required: required,
  }

  if (pattern) {
    registerOptions.pattern = pattern;
  }

  if (minLength) {
    registerOptions.minLength = minLength;
  }

  if (validateWith && watch) {
    registerOptions.validate = (value: string) =>
      value === watch(validateWith) || "Пароли не совпадают";
  }

  return (
    <div className="flex flex-col">
      <input
        {...register(name, registerOptions)}
        type={type}
        placeholder={placeholder}
        className='border-1 rounded-sm pl-3 pt-2 pb-2'
      />
      {error && (
        <span className='text-red-500'>
          {error.message?.toString() || 'Ошибка заполнения'}
        </span>
      )}
    </div>
  )
}

export default InputFieldForm;
