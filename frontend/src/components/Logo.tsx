export interface LogoProps extends React.ComponentPropsWithoutRef<"svg"> {
  size?: number | string;
}

export function Logo({ size, ...others }: LogoProps) {
  return (
    <svg
      {...others}
      width={size || 200}
      height={size || 200}
      viewBox="0 0 200 200"
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <linearGradient id="gradient" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#1a6dfb" />
          <stop offset="100%" stopColor="#4dc3ff" />
        </linearGradient>
      </defs>
      <path
        d="M100 10 L130 40 L140 90 Q100 50 60 90 Q70 40 100 10 Z"
        fill="url(#gradient)"
      />
      <path
        d="M100 110 Q140 150 130 160 L100 190 L70 160 Q60 150 100 110 Z"
        fill="url(#gradient)"
      />
      <path
        d="M70 80 Q60 110 100 140 Q140 110 130 80 L100 50 Z"
        fill="#ffffff"
      />
    </svg>
  );
}
