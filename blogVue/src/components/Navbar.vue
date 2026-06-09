<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
    <div class="container">
      <router-link class="navbar-brand" to="/">BlogWan</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item"><router-link class="nav-link" to="/">首页</router-link></li>
          <template v-if="isLoggedIn">
            <li class="nav-item">
              <router-link class="nav-link" to="/inbox">
                收件箱
                <span v-if="unreadCount > 0" class="badge bg-danger ms-1">{{ unreadCount }}</span>
              </router-link>
            </li>
            <li class="nav-item"><router-link class="nav-link" to="/editor">写文章</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/profile">个人中心</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/following">关注列表</router-link></li>
            <li class="nav-item">
              <button class="btn btn-sm btn-outline-light" @click="handleSign" :disabled="signedToday">
                {{ signedToday ? '今日已签到' : '签到' }}
              </button>
            </li>
            <li class="nav-item">
              <span class="badge bg-light text-dark ms-2">积分: {{ pointsBalance }}</span>
            </li>
            <li class="nav-item"><a class="nav-link" href="#" @click.prevent="logout">退出</a></li>
          </template>
          <template v-else>
            <li class="nav-item"><router-link class="nav-link" to="/login">登录</router-link></li>
            <li class="nav-item"><router-link class="nav-link" to="/register">注册</router-link></li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getToken, clearAuth } from '@/utils/auth'
import { getUnreadCount } from '@/api/notification'
import { signIn, getUserPoints } from '@/api/points'

const route = useRoute()
const router = useRouter()
const isLoggedIn = ref(false)
const unreadCount = ref(0)
let interval = null
const pointsBalance = ref(0)
const signedToday = ref(false)


// 刷新登录状态和未读计数
const refreshAuth = () => {
  const loggedIn = !!getToken()
  isLoggedIn.value = loggedIn
  if (loggedIn) {
    fetchUnreadCount()
  } else {
    unreadCount.value = 0
  }
}
const fetchUnreadCount = async () => {
  if (isLoggedIn.value) {
    try {
      const res = await getUnreadCount()
      unreadCount.value = res.data.unread_count
    } catch (e) { console.error(e) }
  }
}
const checkLogin = () => {
  const newStatus = !!getToken()
  if (isLoggedIn.value !== newStatus) {
    isLoggedIn.value = newStatus
    if (newStatus) fetchPoints()
    else pointsBalance.value = 0
  }
}
const logout = () => {
  clearAuth()
  refreshAuth()
  isLoggedIn.value = false
  unreadCount.value = 0
  router.push('/login')
}

const fetchPoints = async () => {
  if (!isLoggedIn.value) return
  try {
    const res = await getUserPoints()
    pointsBalance.value = res.data.balance
    signedToday.value = res.data.signed_today
  } catch (e) {
    console.error('获取积分失败', e)
  }
}

const handleSign = async () => {
  if (signedToday.value) return
  try {
      await signIn()
      // 触发积分刷新
      window.dispatchEvent(new CustomEvent('pointsUpdated'))
      await fetchPoints()
      alert('签到成功，获得积分！')
    } catch (err) {
      const errorMsg = err.response?.data?.message || err.response?.data?.error || '签到失败，请稍后重试'
      alert(errorMsg)
      // 如果后端返回“今日已签到”，更新本地状态
      if (err.response?.status === 400 && errorMsg.includes('已签到')) {
        signedToday.value = true
      }
      console.error(err)
    }
}

// 全局事件监听：积分变动后刷新
const handlePointsUpdated = () => {
  fetchPoints()
}

// 监听路由变化（确保每次页面切换都检查）
watch(() => route.fullPath, () => {
  refreshAuth()
})

// 监听自定义登录/登出事件
const handleAuthChange = () => {
  checkLogin()
  if (isLoggedIn.value) fetchPoints()
}

// 监听路由变化（因为登录后跳转会触发路由变化）
watch(() => route.fullPath, () => {
  checkLogin()
})


onMounted(() => {
  checkLogin()
  if (isLoggedIn.value) fetchPoints()
  // 每30秒轮询一次未读数
  interval = setInterval(fetchUnreadCount, 30000)
  // 监听收件箱页面触发的更新事件
  window.addEventListener('unreadCountUpdated', fetchUnreadCount)
  window.addEventListener('pointsUpdated', handlePointsUpdated)
    window.addEventListener('authStateChanged', handleAuthChange)
  
})

onUnmounted(() => {
  clearInterval(interval)
  window.removeEventListener('unreadCountUpdated', fetchUnreadCount)
  window.removeEventListener('pointsUpdated', handlePointsUpdated)
  window.removeEventListener('authStateChanged', handleAuthChange)
})
</script>