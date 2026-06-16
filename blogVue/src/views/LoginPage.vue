<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <!-- 卡片组件 (Card) -->
      <div class="card">
        <div class="card-header">登录</div>
        <div class="card-body">
          <!-- 警告框 (Alert) 用于错误信息 -->
          <div class="alert alert-danger" v-if="error">{{ error }}</div>
          <!-- 表单 (Form) -->
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label class="form-label">用户名</label>
              <input type="text" class="form-control" v-model="form.username" required />
            </div>
            <div class="mb-3">
              <label class="form-label">密码</label>
              <input type="password" class="form-control" v-model="form.password" required autocomplete="current-password" />
            </div>
            <!-- 按钮 (Button) -->
            <button type="submit" class="btn btn-primary w-100" :disabled="loading">登录</button>
          </form>
          <p class="mt-3">没有账号？<router-link to="/register">立即注册</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/auth'
import { setToken, setRefreshToken } from '@/utils/auth'

const router = useRouter()
const form = ref({ username: '', password: '' })
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await login(form.value)
    setToken(res.data.access)
    setRefreshToken(res.data.refresh)
    // 触发自定义事件，通知导航栏登录状态已改变
    window.dispatchEvent(new CustomEvent('authStateChanged'))
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>