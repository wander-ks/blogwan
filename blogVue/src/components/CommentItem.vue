<template>
 <div v-if="comment && comment.id" :id="`comment-${comment.id}`" class="comment mb-3 p-3 border rounded">
    <div class="d-flex">
      <div class="flex-grow-1 ms-2">
        <div class="fw-bold">{{ comment.author_name }}</div>
        <small class="text-muted">{{ timeAgo(comment.created_at) }}</small>
        <p class="mt-1">{{ comment.content }}</p>
        <div>
          <!-- 回复按钮：跳转到回复详情页 -->
          <router-link 
            :to="`/comment/${comment.id}/replies`" 
            class="btn btn-sm btn-outline-secondary"
          >
            <i class="bi bi-chat"></i> 回复 ({{ comment.reply_count }})
          </router-link>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { timeAgo } from '@/utils/date'
import { createComment, getReplies } from '@/api/comment'
const props = defineProps(['comment'])
const emit = defineEmits(['reply-submitted'])
const showReplyForm = ref(false)
const replyContent = ref('')
const showReplies = ref(false)
const replies = ref([])
const loadingReplies = ref(false)

const loadReplies = async () => {
  loadingReplies.value = true
  try {
    const res = await getReplies(props.comment.id)
    replies.value = Array.isArray(res.data) 
      ? res.data.filter(r => r && typeof r.id === 'number')
      : []
  } catch (e) {
    console.error(e)
  } finally {
    loadingReplies.value = false
  }
}

</script>

<style scoped>
.comment {
  background-color: #fff;
  transition: background-color 0.2s;
}
.comment:hover {
  background-color: #f8f9fa;
}
.replies {
  border-left: 2px solid #dee2e6;
}
</style>