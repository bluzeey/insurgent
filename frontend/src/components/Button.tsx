import type { ButtonHTMLAttributes, PropsWithChildren } from 'react';

type Props = PropsWithChildren<ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' | 'ghost' }>;

export function Button({ variant = 'secondary', children, ...props }: Props) {
  return (
    <button className={`button button-${variant}`} {...props}>
      {children}
    </button>
  );
}
