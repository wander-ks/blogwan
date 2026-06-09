<template>
  <div class="container mt-4">
    <h2>关注列表</h2>
    <ul class="list-group mt-3">
      <li v-for="follow in followingList" :key="follow.id" class="list-group-item d-flex justify-content-between align-items-center">
        <router-link :to="`/user/${follow.followed_user_info.username}/articles`">
          {{ follow.followed_user_info.username }}
        </router-link>
        <button class="btn btn-sm btn-danger" @click="unfollow(follow.followed_user_info.id)">取消关注</button>
      </li>
    </ul>
    <div v-if="followingList.length === 0" class="text-muted mt-3">暂无关注</div>
    <!-- 分页组件 -->
    <Pagination 
      v-if="totalPages > 1"
      :current="page" 
      :totalPages="totalPages" 
      @update:current="onPageChange" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted,watch } from 'vue'
import { getFollowingList, unfollowUser } from '@/api/follow'
import Pagination from '@/components/Pagination.vue'

const followingList = ref([])
const page = ref(1)
const totalPages = ref(1)


const loadFollowing = async () => {
try {
  const res = await getFollowingList({ page: page.value })   // 传递 page 参数
    followingList.value = res.data.results
    totalPages.value = Math.ceil(res.data.count / 2) || 1
  } catch (err) {
    console.error(err)
  }  
}  

const onPageChange = (newPage) => {
  page.value = newPage
  loadFollowing()
}

const unfollow = async (userId) => {
  await unfollowUser(userId)
  // 取消关注后，如果当前页只有一条数据且不是第一页，回退一页
  if (followingList.value.length === 1 && page.value > 1) {
    page.value -= 1
  }
  await loadFollowing()
}

watch(page, () => {
  loadFollowing()
})

onMounted(loadFollowing)
</script>