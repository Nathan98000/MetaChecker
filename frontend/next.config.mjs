/** @type {import('next').NextConfig} */
const nextConfig = {
  // Static export so the Tauri shell can serve the UI without a Node server.
  output: "export",
  reactStrictMode: true,
};

export default nextConfig;
