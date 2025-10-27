import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    open: true,
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