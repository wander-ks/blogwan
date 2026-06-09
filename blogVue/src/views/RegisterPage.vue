<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header bg-primary text-white">注册新账号</div>
        <div class="card-body">
          <!-- 错误提示 -->
          <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ errorMessage }}
            <button type="button" class="btn-close" @click="errorMessage = ''"></button>
          </div>

          <form @submit.prevent="handleRegister">
            <div class="mb-3">
              <label for="username" class="form-label">用户名</label>
              <input
                type="text"
                id="username"
                class="form-control"
                :class="{ 'is-invalid': errors.username }"
                v-model="form.username"
                required
                autofocus
              />
              <div class="invalid-feedback" v-if="errors.username">{{ errors.username }}</div>
            </div>

            <div class="mb-3">
              <label for="email" class="form-label">电子邮箱</label>
              <input
                type="email"
                id="email"
                class="form-control"
                :class="{ 'is-invalid': errors.email }"
                v-model="form.email"
                required
              />
              <div class="invalid-feedback" v-if="errors.email">{{ errors.email }}</div>
            </div>

            <div class="mb-3">
              <label for="password" class="form-label">密码</label>
              <input
                type="password"
                id="password"
                class="form-control"
                :class="{ 'is-invalid': errors.password }"
                v-model="form.password"
                required
              />
              <div class="invalid-feedback" v-if="errors.password">{{ errors.password }}</div>
            </div>

            <div class="mb-3">
              <label for="password2" class="form-label">确认密码</label>
              <input
                type="password"
                id="password2"
                class="form-control"
                :class="{ 'is-invalid': errors.password2 }"
                v-model="form.password2"
                required
              />
              <div class="invalid-feedback" v-if="errors.password2">{{ errors.password2 }}</div>
            </div>

            <button type="submit" class="btn btn-primary w-100" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
              注册
            </button>
          </form>

          <p class="mt-3 text-center">
            已有账号？<router-link to="/login">立即登录</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/auth'

const router = useRouter()

// 表单数据
const form = reactive({
  username: '',
  email: '',
  password: '',
  password2: '',
})

// 表单验证错误
const errors = reactive({
  username: '',
  email: '',
  password: '',
  password2: '',
})

const loading = ref(false)
const errorMessage = ref('')

// 前端基础验证
const validateForm = () => {
  let isValid = true
  // 重置错误
  Object.keys(errors).forEach(key => errors[key] = '')

  if (!form.username.trim()) {
    errors.username = '用户名不能为空'
    isValid = false
  } else if (form.username.length < 3) {
    errors.username = '用户名至少需要3个字符'
    isValid = false
  }

  if (!form.email.trim()) {
    errors.email = '邮箱不能为空'
    isValid = false
  } else if (!/^\S+@\S+\.\S+$/.test(form.email)) {
    errors.email = '请输入有效的邮箱地址'
    isValid = false
  }

  if (!form.password) {
    errors.password = '密码不能为空'
    isValid = false
  } else if (form.password.length < 6) {
    errors.password = '密码至少需要6个字符'
    isValid = false
  }

  if (form.password !== form.password2) {
    errors.password2 = '两次输入的密码不一致'
    isValid = false
  }

  return isValid
}

const handleRegister = async () => {
  if (!validateForm()) return

  loading.value = true
  errorMessage.value = ''

  try {
    // 调用后端注册接口
    await register({
      username: form.username,
      email: form.email,
      password: form.password,
      password2: form.password2,
    })
    // 注册成功，提示并跳转到登录页
    alert('注册成功！请登录')
    router.push('/login')
  } catch (err) {
    // 处理后端返回的错误（如用户名已存在、邮箱重复等）
    if (err.response?.data) {
      const data = err.response.data
      if (data.username) errorMessage.value = data.username[0]
      else if (data.email) errorMessage.value = data.email[0]
      else if (data.detail) errorMessage.value = data.detail
      else errorMessage.value = '注册失败，请稍后重试'
    } else {
      errorMessage.value = '网络错误，请检查后端服务'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 可添加组件内样式（可选） */
</style>