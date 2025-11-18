// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        // Keep proxy timeouts on par with frontend axios (300s) to avoid
        // websocket/HTTP stream cuts during long translations.
        timeout: 300000,
        proxyTimeout: 300000,
      },
      '/files': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        timeout: 300000,
        proxyTimeout: 300000,
      }
    }
  }
})
