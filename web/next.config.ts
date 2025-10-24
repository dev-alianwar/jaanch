import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Note: Static export disabled for now due to cookie-based locale detection
  // output: 'export',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
};

export default nextConfig;
