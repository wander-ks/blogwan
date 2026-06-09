import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue()
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),   // 路径别名，方便导入
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api/v1': {
        target: 'http://127.0.0.1:8080',   // 后端地址
        changeOrigin: true,
      },
      '/media': {
        target: 'http://127.0.0.1:8080',
        changeOrigin: true,
      },
    },
  },
  build: {
    // 输出目录（默认 dist）
    outDir: 'dist',
    // 静态资源存放目录
    assetsDir: 'assets',
    // 是否生成 source map（生产环境建议 false）
    sourcemap: false,
    // 打包 chunk 大小警告限制
    chunkSizeWarningLimit: 1000,
    // 压缩选项（默认 esbuild，也支持 terser）
    minify: 'esbuild',
    // 启用/禁用 brotli 压缩（需要配合服务器）
    // 通常不需要在构建时生成压缩包
    rollupOptions: {
      output: {
        // 分包策略：将 vendor 库分离成单独 chunk
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('vue') || id.includes('vue-router')) {
              return 'vue-vendor'
            }
            if (id.includes('bootstrap')) {
              return 'bootstrap-vendor'
            }
            return 'vendor'
          }
        },
      },
    },
  },

})
