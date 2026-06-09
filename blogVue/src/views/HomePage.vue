<template>
  <div>
    <div class="row mb-4">
      <!-- 下拉框：筛选作者 -->
      <div class="col-md-3">
        <select class="form-select" v-model="filterAuthor">
          <option value="">全部</option>
          <option v-if="currentUsername" :value="currentUsername">我的文章</option>
        </select>
      </div>
      <!-- 搜索框 -->
      <div class="col-md-6">
        <input 
          type="text" 
          class="form-control" 
          placeholder="搜索文章标题或内容..." 
          v-model="search" 
          @keyup.enter="fetchArticles"
        />
      </div>
      <div class="col-md-3">
        <button class="btn btn-primary w-100" @click="fetchArticles">搜索</button>
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
import { ref, onMounted, watch } from 'vue'
import { getArticles } from '@/api/article'
import ArticleCard from '@/components/ArticleCard.vue'
import Pagination from '@/components/Pagination.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import { getToken } from '@/utils/auth'
import { getProfile } from '@/api/auth'

const articles = ref([])
const loading = ref(false)
const page = ref(1)
const totalPages = ref(1)
const search = ref('')
const authorFilter = ref('')
const authors = ref([])
const filterAuthor = ref('')      // 筛选作者，空字符串表示全部
const currentUsername = ref(null) // 当前登录用户名


const fetchCurrentUser = async () => {
  try {
    const res = await getProfile()
    currentUsername.value = res.data.username
  } catch (e) {
    console.error('获取用户信息失败', e)
  }
}

const fetchArticles = async () => {
  loading.value = true
  try {
    const params = { page: page.value, search: search.value }
    // 关键：只有当 filterAuthor 有值且等于当前用户名时，才添加作者筛选
    if (filterAuthor.value && filterAuthor.value === currentUsername.value) {
      params.author__username = currentUsername.value
    }
    const res = await getArticles(params)
    articles.value = res.data.results
    totalPages.value = Math.ceil(res.data.count / 2) || 1

  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const onPageChange = (newPage) => {
  page.value = newPage
  fetchArticles()
}

// 监听筛选作者变化，重置页码并重新加载
watch(filterAuthor, () => {
  page.value = 1
  fetchArticles()
})

// 监听搜索内容变化，重置页码并重新加载
watch(search, () => {
  page.value = 1
  fetchArticles()
})


onMounted(() => {
  fetchCurrentUser()
  fetchArticles()
})
</script>