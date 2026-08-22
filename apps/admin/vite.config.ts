import path from "node:path";
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const envDir = path.resolve(import.meta.dirname, "../../.envs/local/admin");

  const env = loadEnv(mode, envDir, "");

  return {
    envDir,

    plugins: [react()],

    server: {
      port: Number(env.VITE_PORT ?? 3001),
      strictPort: true,

      proxy: {
        "/api": {
          target: env.VITE_API_URL ?? "http://localhost:8000",
          changeOrigin: true,
        },
      },
    },
  };
});