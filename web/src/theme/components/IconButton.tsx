import React from 'react';
import { cn } from '@/lib/utils';

interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  icon: React.ReactNode;
  tooltip?: string;
}

export const IconButton: React.FC<IconButtonProps> = ({
  variant = 'ghost',
  size = 'md',
  icon,
  tooltip,
  className,
  ...props
}) => {
  const baseClasses = [
    'inline-flex items-center justify-center rounded-lg',
    'transition-all duration-200 ease-in-out',
    'focus:outline-none focus:ring-2 focus:ring-offset-2',
    'disabled:opacity-50 disabled:pointer-events-none',
    'transform hover:scale-110 active:scale-95',
  ].join(' ');

  const variants = {
    primary: [
      'bg-primary-600 text-white shadow-lg hover:shadow-xl',
      'hover:bg-primary-700 focus:ring-primary-500',
    ].join(' '),
    
    secondary: [
      'bg-gray-200 text-gray-900 shadow-md hover:shadow-lg',
      'hover:bg-gray-300 focus:ring-gray-500',
      'dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600',
    ].join(' '),
    
    outline: [
      'border-2 border-primary-600 bg-transparent text-primary-600',
      'hover:bg-primary-600 hover:text-white focus:ring-primary-500',
      'dark:border-primary-400 dark:text-primary-400',
    ].join(' '),
    
    ghost: [
      'bg-transparent text-gray-600 hover:bg-gray-100',
      'focus:ring-gray-500 dark:text-gray-400 dark:hover:bg-gray-800',
    ].join(' '),
  };

  const sizes = {
    sm: 'w-8 h-8 text-sm',
    md: 'w-10 h-10 text-base',
    lg: 'w-12 h-12 text-lg',
  };

  return (
    <button
      className={cn(baseClasses, variants[variant], sizes[size], className)}
      title={tooltip}
      {...props}
    >
      {icon}
    </button>
  );
};