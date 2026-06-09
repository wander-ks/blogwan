<template>
  <div v-if="loading"><LoadingSpinner /></div>
    <div v-else-if="error">{{ error }}</div>
  <div v-else-if="article">
    <!-- 文章主体卡片 -->
    <div class="card mb-4">
      <div class="card-body">
        <h1>{{ article.title }}</h1>
        <div class="text-muted mb-3">
          <span>作者: {{ article.author?.username }}</span>
          <span class="ms-3">发布时间: {{ formatDate(article.created_at) }}</span>
          <span class="ms-3">阅读: {{ article.views }}</span>
          <span class="ms-3">点赞: {{ article.likes }}</span>
        </div>
        <div class="markdown-body" v-html="article.content"></div>
        <hr />
        <div class="d-flex justify-content-between align-items-center">
          <!-- 按钮组件 (Button) -->
          <button class="btn btn-outline-danger" @click="toggleLike">
            {{ liked ? '已点赞' : '点赞' }} ({{ article.likes }})
          </button>
          <button class="btn btn-outline-info ms-2" @click="handleDownload" :disabled="isAuthor">
            下载 (1积分)
          </button>
          <!-- 关注按钮：仅当登录用户不是作者时显示 -->
            <button 
                v-if="isLogin && !isAuthor" 
                class="btn ms-2" 
                :class="isFollowing ? 'btn-outline-secondary' : 'btn-outline-primary'"
                @click="toggleFollow"
              >
              {{ isFollowing ? '已关注' : '关注' }}
            </button>
          <div v-if="isAuthor">
            <router-link :to="`/editor/${article.id}`" class="btn btn-warning me-2">编辑</router-link>
            <button class="btn btn-danger" @click="confirmDelete">删除</button>
          </div>
        </div>
      </div>
    </div>

     <!-- 评论区域 -->
    <div class="card mt-4">
      <div class="card-header bg-white fw-bold">评论</div>
      <div class="card-body">
        <!-- 发表评论表单 -->
        <div v-if="isLogin" class="mb-4">
          <textarea class="form-control" rows="3" v-model="newComment" placeholder="写下你的评论..."></textarea>
          <button class="btn btn-primary mt-2" @click="submitComment">发布评论</button>
        </div>
        <div v-else class="alert alert-info">
          请 <router-link to="/login">登录</router-link> 后评论
        </div>

        <!-- 评论列表 -->
        <LoadingSpinner v-if="commentsLoading" />
        <div v-else>
          <CommentItem
            v-for="comment in comments"
            :key="comment.id"
            :comment="comment"
            @reply-submitted="refreshComments"
          />
          <div v-if="comments.length === 0" class="text-muted text-center py-4">
            暂无评论，快来抢沙发吧～
          </div>
          <Pagination 
            :current="commentPage" 
            :totalPages="commentTotalPages" 
            @update:current="onCommentPageChange" 
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getArticle, deleteArticle } from '@/api/article'
import { getComments, createComment } from '@/api/comment'
import { likeArticle } from '@/api/like'
import { getToken } from '@/utils/auth'
import { formatDate } from '@/utils/date'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import CommentItem from '@/components/CommentItem.vue'
import { watch, nextTick } from 'vue'
import Pagination from '@/components/Pagination.vue'
import { followUser, unfollowUser, getFollowStatus } from '@/api/follow'
import { downloadArticle } from '@/api/article'
import { getUserPoints } from '@/api/points'

const route = useRoute()
const router = useRouter()
const article = ref(null)
const comments = ref([])
const loading = ref(true)
const newComment = ref('')
const liked = ref(false)
const error = ref(null)
const commentsLoading = ref(false)
const commentPage = ref(1)
const commentTotalPages = ref(1)
const isFollowing = ref(false)
const userPoints = ref(0)

const isLogin = computed(() => !!getToken())
// 判断当前用户是否为作者（通过解析 JWT 中的 user_id，或后端返回的作者 id）
const isAuthor = computed(() => {
  if (!article.value || !isLogin.value) return false
  const token = getToken()
  if (!token) return false
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return article.value.author?.id === payload.user_id
  } catch {
    return false
  }
})


// 获取文章详情
const fetchArticle = async () => {
  loading.value = true
  try {
    const res = await getArticle(route.params.id)
    article.value = res.data
  } finally {
    loading.value = false
  }
}

const fetchComments = async () => {
  commentsLoading.value = true
  try {
    // 必须同时传递 article 和 page 参数
    const params = {
      article: route.params.id,
      parent: 'null', // 关键：只获取顶级评论
      page: commentPage.value
    }
    const res = await getComments(params)
    comments.value = res.data.results
    commentTotalPages.value = Math.ceil(res.data.count / 2) || 1
  } catch (e) {
    console.error(e)
  } finally {
    commentsLoading.value = false
  }
}


// 提交顶级评论
const submitComment = async () => {
  if (!newComment.value.trim()) return
  try {
    await createComment({ article: route.params.id, content: newComment.value })
    newComment.value = ''
    commentPage.value = 1
    await fetchComments()
}catch (err) {
    console.error(err)
    alert('发布失败：' + (err.response?.data?.message || '请稍后重试'))
  }
}




const handleDownload = async () => {
  try {
    const res = await downloadArticle(route.params.id)
    // 后端返回的是 { message: '...' }
    alert(res.data.message || '下载请求已提交，请前往收件箱获取链接')
    // 积分已扣除，触发刷新
    window.dispatchEvent(new CustomEvent('pointsUpdated'))
  } catch (err) {
    const errorMsg = err.response?.data?.error || '下载失败，请稍后重试'
    alert(errorMsg)
  }
}

const onCommentPageChange = (page) => {
  commentPage.value = page
}

const refreshComments = () => {
  fetchComments()
}

const confirmDelete = async () => {
  if (confirm('确定删除这篇文章吗？')) {
    await deleteArticle(route.params.id)
    router.push('/')
  }
}
const toggleLike = async () => {
  if (!isLogin.value) return router.push('/login')
  const res = await likeArticle(route.params.id)
  article.value.likes = res.data.likes_count
  liked.value = res.data.liked
  // 触发积分刷新
  window.dispatchEvent(new CustomEvent('pointsUpdated'))
}
const scrollToComment = () => {
  const hash = route.hash
  if (hash && hash.startsWith('#comment-')) {
    const element = document.getElementById(hash.substring(1))
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'center' })
      element.style.backgroundColor = '#fff3cd'
      setTimeout(() => {
        element.style.backgroundColor = ''
      }, 2000)
    }
  }
}

const fetchCommentsAndScroll = async () => {
  await fetchComments()
  await nextTick()
  scrollToComment()
}


// 检查是否已关注作者
const checkFollowStatus = async () => {
  if (!isLogin.value || isAuthor.value) return
  try {
    const res = await getFollowStatus(article.value.author.id)
    isFollowing.value = res.data.is_following
  } catch (e) {
    console.error(e)
  }
}

// 关注/取消关注
const toggleFollow = async () => {
  if (!isLogin.value) return router.push('/login')
  try {
    if (isFollowing.value) {
      await unfollowUser(article.value.author.id)
      isFollowing.value = false
    } else {
      await followUser(article.value.author.id)
      isFollowing.value = true
    }
  } catch (err) {
    console.error(err)
    alert(err.response?.data?.error || '操作失败')
  }
}


const fetchDetail = async () => {
  loading.value = true
  error.value = null
  try {
    const res = await getArticle(route.params.id)
    article.value = res.data
    // 获取关注状态
    await checkFollowStatus()
  }catch (err) {
    error.value = '加载文章失败，请稍后重试。'
    console.error(err)
  }finally {
    loading.value = false
  }
}


// 监听 commentPage 的变化，自动重新获取评论
watch(commentPage, () => {
  fetchComments()
})

onMounted(() => {
  fetchArticle()
  fetchDetail()
  fetchCommentsAndScroll()
})

watch(() => route.hash, () => {
  fetchCommentsAndScroll()
})
</script>