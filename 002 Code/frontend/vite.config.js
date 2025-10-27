import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['BudgetlyApp.png'],
      manifest: {
        name: 'Budgetly - 예산 관리',
        short_name: 'Budgetly',
        description: '효율적인 예산 관리 애플리케이션',
        theme_color: '#3e56f6',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: '/',
        icons: [
          {
            src: '/BudgetlyApp.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/BudgetlyApp.png',
            sizes: '512x512',
            type: 'image/png'
          },
          {
            src: '/BudgetlyApp.png',
            sizes: '192x192',
            type: 'image/png',
            purpose: 'maskable'
          },
          {
            src: '/BudgetlyApp.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable'
          }
        ]
      },
      workbox: {
        cleanupOutdatedCaches: true,
        skipWaiting: true
      }
    })
  ],
  server: {
    port: 3000,
    open: true,
    host: '0.0.0.0', // 외부 접속 허용
    allowedHosts: [
      'ec2-43-203-136-37.ap-northeast-2.compute.amazonaws.com', // 허용할 호스트 추가
      'localhost',
      '127.0.0.1'
    ],
    // 개발 중 캐싱 방지
    headers: {
      'Cache-Control': 'no-store'
    }
  },
  // 빌드 시 파일명에 해시 추가로 캐시 무효화
  build: {
    rollupOptions: {
      output: {
        // 파일명에 해시 추가
        entryFileNames: '[name].[hash].js',
        chunkFileNames: '[name].[hash].js',
        assetFileNames: '[name].[hash].[ext]'
      }
    }
  }
})