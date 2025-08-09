import React from 'react';
import { cn } from '@/lib/utils';

interface ButtonGroupProps {
  children: React.ReactNode;
  orientation?: 'horizontal' | 'vertical';
  className?: string;
}

export const ButtonGroup: React.FC<ButtonGroupProps> = ({
  children,
  orientation = 'horizontal',
  className,
}) => {
  const baseClasses = 'inline-flex';
  
  const orientationClasses = {
    horizontal: 'flex-row',
    vertical: 'flex-col',
  };

  return (
    <div className={cn(baseClasses, orientationClasses[orientation], className)}>
      {React.Children.map(children, (child, index) => {
        if (React.isValidElement(child)) {
          const isFirst = index === 0;
          const isLast = index === React.Children.count(children) - 1;
          
          let additionalClasses = '';
          
          if (orientation === 'horizontal') {
            if (!isFirst && !isLast) {
              additionalClasses = 'rounded-none border-l-0';
            } else if (isFirst) {
              additionalClasses = 'rounded-r-none';
            } else if (isLast) {
              additionalClasses = 'rounded-l-none border-l-0';
            }
          } else {
            if (!isFirst && !isLast) {
              additionalClasses = 'rounded-none border-t-0';
            } else if (isFirst) {
              additionalClasses = 'rounded-b-none';
            } else if (isLast) {
              additionalClasses = 'rounded-t-none border-t-0';
            }
          }

          return React.cloneElement(child, {
            className: cn(child.props.className, additionalClasses),
          });
        }
        return child;
      })}
    </div>
  );
};