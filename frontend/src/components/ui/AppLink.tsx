import React from 'react';
import { Link } from 'react-router-dom';
import type { LinkProps } from 'react-router-dom';

type Size = 'sm' | 'md' | 'lg';
type Scheme = 'primary' | 'accent' | 'danger' | 'default';

interface AppLinkProps extends Omit<LinkProps, 'href' | 'label' | 'size'> {
  to: string;
  label?: string | React.ReactElement;
  size?: Size;
  isDisabled?: boolean;
  variant?: 'solid' | 'outline' | 'text';
  leftIcon?: React.ReactElement;
  rightIcon?: React.ReactElement;
  scheme?: Scheme;
  children?: React.ReactNode;
}

const sizeClasses: Record<Size, string> = {
  sm: 'text-sm py-1 px-3',
  md: 'text-base py-2 px-4',
  lg: 'text-lg py-3 px-6',
};

const schemeClasses: Record<Scheme, string> = {
  primary: 'text-white bg-blue-600 hover:bg-blue-700',
  accent: 'text-white bg-purple-600 hover:bg-purple-700',
  danger: 'text-white bg-red-600 hover:bg-red-700',
  default: 'text-gray-700 hover:text-gray-900',
};

const variantClasses: Record<'solid' | 'outline' | 'text', string> = {
  solid: '',
  outline: 'border border-current bg-transparent',
  text: 'bg-transparent',
};

const AppLink: React.FC<AppLinkProps> = ({
  to,
  label,
  size = 'md',
  isDisabled = false,
  variant = 'text',
  leftIcon,
  rightIcon,
  scheme = 'default',
  children,
  className = '',
  onClick,
  ...rest
}) => {
  const baseClass = `
    inline-flex items-center justify-center cursor-pointer select-none
    transition-colors duration-200
    ${sizeClasses[size]} ${schemeClasses[scheme]} ${variantClasses[variant]}
    ${isDisabled ? 'opacity-50 pointer-events-none' : ''}
  `;

  return (
    <Link
      to={to}
      className={`${baseClass} ${className}`}
      onClick={isDisabled ? undefined : onClick}
      {...rest}
    >
      {leftIcon && <span className="mr-2">{leftIcon}</span>}
      {label || children}
      {rightIcon && <span className="ml-2">{rightIcon}</span>}
    </Link>
  );
};

export default AppLink;
