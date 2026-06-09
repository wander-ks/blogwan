<template>
  <div>
    <h2>{{ username }} 的文章</h2>
    <div class="row mb-4">
      <div class="col-md-6">
        <input type="text" class="form-control" placeholder="搜索标题..." v-model="search" @keyup.enter="fetchArticles" />
      </div>
      <div class="col-md-3">
        <button class="btn btn-primary" @click="fetchArticles">搜索</button>
      </div>
      <div class="col-md-3" v-if="currentUser && currentUser !== username">
        <button v-if="isFollowing" class="btn btn-outline-danger" @click="unfollow">取消关注</button>
        <button v-else class="btn btn-outline-primary" @click="follow">关注</button>
      </div>
    </div>
    <LoadingSpinner v-if="loading" />
    <div v-else>
      <ArticleCard v-for="article in articles" :key="article.id" :article="article" />
      <div v-if="articles.length === 0" class="alert alert-info">暂无文章</div>
      <Pagination :current="page" :totalPages="totalPages" @update:current="onPageChange" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getUserArticles } from '@/api/follow'
import { getFollowStatus, followUser, unfollowUser } from '@/api/follow'
import { getToken } from '@/utils/auth'
import ArticleCard from '@/components/ArticleCard.vue'
import Pagination from '@/components/Pagination.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const route = useRoute()
const router = useRouter()
const username = route.params.username
const currentUser = ref(null) // 从 token 解析
const articles = ref([])
const loading = ref(false)
const page = ref(1)
const totalPages = ref(1)
const search = ref('')
const isFollowing = ref(false)

const fetchArticles = async () => {
  loading.value = true
  try {
    const params = { page: page.value, search: search.value, author__username: username }
    const res = await getUserArticles(username, { params }) // 实际调用 getArticles 带参数
    articles.value = res.data.results
    totalPages.value = Math.ceil(res.data.count / 2) || 1
  } catch (e) { console.error(e) } finally { loading.value = false }
}
const onPageChange = (newPage) => { page.value = newPage; fetchArticles() }
const checkFollowStatus = async () => {
  if (currentUser.value && currentUser.value !== username) {
    const res = await getFollowStatus(currentUser.value) // 需要获取当前用户的ID
    isFollowing.value = res.data.is_following
  }
}
const follow = async () => { await followUser(currentUser.value); await checkFollowStatus() }
const unfollow = async () => { await unfollowUser(currentUser.value); await checkFollowStatus() }

onMounted(() => {
  // 解析 token 获取当前用户名
  const token = getToken()
  if (token) {
    const payload = JSON.parse(atob(token.split('.')[1]))
    currentUser.value = payload.username
  }
  fetchArticles()
  checkFollowStatus()
})
</script>