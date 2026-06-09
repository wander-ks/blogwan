<template>
  <div class="container mt-4">
    <div class="mb-3">
      <button class="btn btn-outline-secondary" @click="goBack">
        &larr; 返回
      </button>
    </div>

    <div class="card mb-4" v-if="parentComment.id">
      <div class="card-body">
        <div class="fw-bold">{{ parentComment.author_name }}</div>
        <small class="text-muted">{{ formatDate(parentComment.created_at) }}</small>
        <p class="mt-2">{{ parentComment.content }}</p>
      </div>
    </div>

    <h5>回复（共 {{ totalReplies }} 条）</h5>
    <LoadingSpinner v-if="loading" />
    <div v-else>
      <div v-for="reply in replies" :key="reply.id" class="reply-item mb-3 p-3 border rounded">
        <div class="fw-bold">{{ reply.author_name }}</div>
        <small class="text-muted">{{ timeAgo(reply.created_at) }}</small>
        <p class="mt-2">{{ reply.content }}</p>
      </div>
      <div v-if="replies.length === 0" class="text-muted">暂无回复</div>
      <Pagination 
        v-if="totalPages > 1"
        :current="page" 
        :totalPages="totalPages" 
        @update:current="onPageChange" 
      />
    </div>

    <div class="card mt-4">
      <div class="card-header">发表回复</div>
      <div class="card-body">
        <div v-if="isLogin">
          <textarea class="form-control" rows="3" v-model="replyContent" placeholder="写下你的回复..."></textarea>
          <button class="btn btn-primary mt-2" @click="submitReply" :disabled="submitting">提交回复</button>
        </div>
        <div v-else class="alert alert-info">
          请 <router-link to="/login">登录</router-link> 后回复
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getComments, createComment, getCommentDetail } from '@/api/comment'
import { getToken } from '@/utils/auth'
import { formatDate, timeAgo } from '@/utils/date'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import Pagination from '@/components/Pagination.vue'

const route = useRoute()
const router = useRouter()
const commentId = route.params.commentId

const parentComment = ref({})
const replies = ref([])
const loading = ref(false)
const page = ref(1)
const totalPages = ref(1)
const totalReplies = ref(0)
const replyContent = ref('')
const submitting = ref(false)
const isLogin = computed(() => !!getToken())

const fetchParentComment = async () => {
  try {
    const res = await getCommentDetail(commentId)
    parentComment.value = res.data
  } catch (err) {
    console.error(err)
    router.push('/')
  }
}

const fetchReplies = async () => {
  loading.value = true
  try {
    const params = {
      parent: commentId, // 数字类型，获取指定评论的子评论
      page: page.value
    }
    const res = await getComments(params)
    replies.value = res.data.results
    totalReplies.value = res.data.count
    totalPages.value = Math.ceil(totalReplies.value / 2) || 1
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const onPageChange = (newPage) => {
  page.value = newPage
  fetchReplies()
}

const submitReply = async () => {
  if (!replyContent.value.trim()) return
  submitting.value = true
  try {
    await createComment({
      article: parentComment.value.article,
      parent: parseInt(commentId),
      content: replyContent.value
    })
    replyContent.value = ''
    // 刷新回复列表
    page.value = 1
    await fetchReplies()
    // 可选：显示成功提示
  } catch (err) {
    console.error(err)
    alert('回复失败')
  } finally {
    submitting.value = false
  }
}

const goBack = () => {
  router.go(-1)  // 返回上一页
}

onMounted(() => {
  fetchParentComment()
  fetchReplies()
})
</script>