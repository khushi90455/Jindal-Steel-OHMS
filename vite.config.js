import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

// Disable PWA when building for Electron — service workers conflict with file:// protocol
const isElectronBuild = process.env.ELECTRON === 'true';

// https://vite.dev/config/
export default defineConfig({
  base: './',
  plugins: [
    react(),
    !isElectronBuild && VitePWA({
      registerType: 'autoUpdate',
      devOptions: {
        enabled: true
      },
      manifest: {
        name: 'JSPulse OHMS Dashboard',
        short_name: 'JSPulse OHMS',
        description: 'Occupational Health Center Dashboard',
        theme_color: '#0f172a',
        background_color: '#f8fafc',
        display: 'standalone',
        icons: [
          {
            src: 'logo.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'logo.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}']
      }
    })
  ].filter(Boolean),
})
