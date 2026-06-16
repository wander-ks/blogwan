<template>
  <div class="container mt-4">
    <h2>收件箱</h2>
    <ul class="list-group mt-3">
      <li v-for="msg in messages" :key="msg.id" class="list-group-item" :class="{ 'table-secondary': !msg.is_read }">
        <div class="d-flex justify-content-between">
          <strong>{{ msg.title }}</strong>
          <small>{{ formatDate(msg.created_at) }}</small>
        </div>
        <p class="mt-2">{{ msg.content }}</p>
        <div class="mt-2">
          <button v-if="!msg.is_read" class="btn btn-sm btn-outline-primary" @click="markRead(msg.id)">标记已读</button>
          <button class="btn btn-sm btn-outline-danger ms-2" @click="deleteMsg(msg.id)">删除</button>
          <!-- 判断是否为下载链接 -->
          <a v-if="msg.link && msg.link.includes('/download-file/')" :href="msg.link" class="btn btn-sm btn-outline-success ms-2" @click="markReadAndDownload(msg.id, msg.link, $event)">
            下载
          </a>
          <router-link v-else-if="msg.link" :to="msg.link" class="btn btn-sm btn-outline-secondary ms-2" @click="markReadBeforeNavigate(msg.id, $event)">
            查看详情
          </router-link>

        </div>
      </li>
    </ul>
    <div v-if="messages.length === 0" class="text-center text-muted mt-4">暂无消息</div>
    <Pagination v-model:current="page" :totalPages="totalPages" @update:current="loadMessages" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { getMessages, deleteMessage, markMessageRead } from '@/api/notification'
import { formatDate } from '@/utils/date'
import Pagination from '@/components/Pagination.vue'
import { useRouter } from 'vue-router'

const messages = ref([])
const page = ref(1)
const totalPages = ref(1)
const router = useRouter()

// 标记已读并下载（用于下载链接）
const markReadAndDownload = async (id, link, event) => {
  event.preventDefault()           // 阻止默认跳转
  await markMessageRead(id)        // 标记已读
  // 触发下载
  window.location.href = link
  // 更新本地消息状态（可选）
  const msg = messages.value.find(m => m.id === id)
  if (msg) msg.is_read = true
  // 通知导航栏更新角标
  window.dispatchEvent(new CustomEvent('unreadCountUpdated'))
}


const loadMessages = async () => {
    try {
    const res = await getMessages({ page: page.value })
    messages.value = res.data.results
    totalPages.value = Math.ceil(res.data.count / 2) || 1
    }catch (err) {
        console.error(err)
    }
}
// 监听页码变化，自动重新加载
watch(page, () => {
  loadMessages()
})

const markRead = async (id) => {
  await markMessageRead(id)
  await loadMessages()
  window.dispatchEvent(new CustomEvent('unreadCountUpdated'))
}

const deleteMsg = async (id) => {
  await deleteMessage(id)
  await loadMessages()
  window.dispatchEvent(new CustomEvent('unreadCountUpdated'))
}



// 查看详情前先标记已读，再跳转
const markReadBeforeNavigate = async (id, event) => {
  // 阻止默认的 router-link 跳转，先标记已读再手动跳转
  event.preventDefault()
  await markMessageRead(id)
  // 更新本地列表中的该消息状态为已读（避免重新加载整个列表，提升体验）
  const msg = messages.value.find(m => m.id === id)
  if (msg) msg.is_read = true
  // 通知导航栏更新角标
  window.dispatchEvent(new CustomEvent('unreadCountUpdated'))
  // 获取链接：优先从 event.currentTarget 取，如果为 null 则从 event.target 向上查找
  let linkEl = event.currentTarget
  if (!linkEl) linkEl = event.target.closest('router-link') || event.target
  const link = linkEl?.getAttribute('to')
  if (link) router.push(link)
}

onMounted(async () => {

  // 通知导航栏更新未读角标
  window.dispatchEvent(new CustomEvent('unreadCountUpdated'))
  // 加载消息列表
  await loadMessages()
})


</script>