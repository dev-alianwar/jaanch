import React from 'react';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive' | 'success';
    size?: 'sm' | 'md' | 'lg' | 'xl';
    loading?: boolean;
    icon?: React.ReactNode;
    iconPosition?: 'left' | 'right';
    fullWidth?: boolean;
    children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
    variant = 'primary',
    size = 'md',
    loading = false,
    icon,
    iconPosition = 'left',
    fullWidth = false,
    className,
    disabled,
    children,
    ...props
}) => {
    const baseClasses = [
        'inline-flex items-center justify-center rounded-lg font-medium',
        'transition-all duration-200 ease-in-out',
        'focus:outline-none focus:ring-2 focus:ring-offset-2',
        'disabled:opacity-50 disabled:pointer-events-none',
        'transform hover:scale-105 active:scale-95',
    ].join(' ');

    const variants = {
        primary: [
            'bg-gradient-to-r from-primary-600 to-primary-700',
            'text-white shadow-lg hover:shadow-xl',
            'hover:from-primary-700 hover:to-primary-800',
            'focus:ring-primary-500',
            'dark:from-primary-500 dark:to-primary-600',
        ].join(' '),

        secondary: [
            'bg-white border-2 border-gray-400',
            'text-gray-900 shadow-md hover:shadow-lg',
            'hover:bg-gray-50 hover:text-gray-900',
            'focus:ring-primary-500 font-semibold',
            'dark:from-gray-700 dark:to-gray-800',
            'dark:text-gray-100 dark:hover:from-gray-600 dark:hover:to-gray-700',
        ].join(' '),

        outline: [
            'border-2 border-primary-700 bg-white',
            'text-primary-700 hover:bg-primary-600 hover:text-white',
            'focus:ring-primary-500 shadow-md hover:shadow-lg',
            'dark:border-primary-400 dark:text-primary-400',
            'dark:hover:bg-primary-400 dark:hover:text-gray-900',
        ].join(' '),

        ghost: [
            'bg-transparent text-gray-700 hover:bg-gray-100',
            'focus:ring-gray-500 transition-colors',
            'dark:text-gray-300 dark:hover:bg-gray-800',
        ].join(' '),

        destructive: [
            'bg-gradient-to-r from-red-600 to-red-700',
            'text-white shadow-lg hover:shadow-xl',
            'hover:from-red-700 hover:to-red-800',
            'focus:ring-red-500',
        ].join(' '),

        success: [
            'bg-gradient-to-r from-green-600 to-green-700',
            'text-white shadow-lg hover:shadow-xl',
            'hover:from-green-700 hover:to-green-800',
            'focus:ring-green-500',
        ].join(' '),
    };

    const sizes = {
        sm: 'px-3 py-2 text-sm gap-2',
        md: 'px-4 py-2.5 text-base gap-2',
        lg: 'px-6 py-3 text-lg gap-3',
        xl: 'px-8 py-4 text-xl gap-4 min-h-[56px]',
    };

    const widthClass = fullWidth ? 'w-full' : '';

    const renderIcon = (position: 'left' | 'right') => {
        if (loading && position === 'left') {
            return <Loader2 className="h-4 w-4 animate-spin" />;
        }

        if (icon && iconPosition === position) {
            return <span className="flex-shrink-0">{icon}</span>;
        }

        return null;
    };

    return (
        <button
            className={cn(
                baseClasses,
                variants[variant],
                sizes[size],
                widthClass,
                className
            )}
            disabled={disabled || loading}
            {...props}
        >
            {renderIcon('left')}
            <span>{children}</span>
            {renderIcon('right')}
        </button>
    );
};