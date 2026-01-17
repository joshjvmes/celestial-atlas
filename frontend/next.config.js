/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: false, // Disable for Three.js compatibility
  transpilePackages: ['three'],
  webpack: (config) => {
    config.externals = [...(config.externals || []), { canvas: 'canvas' }];

    // Ensure proper module resolution
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
    };

    return config;
  },
};

module.exports = nextConfig;
