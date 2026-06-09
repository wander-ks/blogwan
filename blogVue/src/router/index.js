import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '@/utils/auth'

const routes = [
  { path: '/', name: 'Home', component: () => import('@/views/HomePage.vue') },
  { path: '/login', name: 'Login', component: () => import('@/views/LoginPage.vue'), meta: { guestOnly: true } },
  { path: '/register', name: 'Register', component: () => import('@/views/RegisterPage.vue'), meta: { guestOnly: true } },
  { path: '/articles/:id', name: 'ArticleDetail', component: () => import('@/views/ArticleDetail.vue') },
  { path: '/editor', name: 'ArticleEditor', component: () => import('@/views/ArticleEditor.vue'), meta: { requiresAuth: true } },
  { path: '/editor/:id', name: 'ArticleEdit', component: () => import('@/views/ArticleEditor.vue'), meta: { requiresAuth: true } },
  { path: '/profile', name: 'Profile', component: () => import('@/views/ProfilePage.vue'), meta: { requiresAuth: true } },
  { path: '/inbox', name: 'Inbox',  component: () => import('@/views/InboxPage.vue'), meta: { requiresAuth: true } },
  { path: '/comment/:commentId/replies',name: 'ReplyPage', component: () => import('@/views/ReplyPage.vue'),meta: { requiresAuth: false }  // 允许未登录查看回复，但发表回复需登录
  },
  { path: '/following', name: 'Following',component: () => import('@/views/FollowingPage.vue'), meta: { requiresAuth: true } },
  { path: '/user/:username/articles', name: 'UserArticles', component: () => import('@/views/UserArticlesPage.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = !!getToken()
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
  } else if (to.meta.guestOnly && isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router