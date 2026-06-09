<template>
  <nav v-if="totalPages > 1">
    <!-- Bootstrap 分页组件 (Pagination) -->
    <ul class="pagination justify-content-center">
      <li class="page-item" :class="{ disabled: current === 1 }">
        <a class="page-link" href="#" @click.prevent="changePage(current - 1)">上一页</a>
      </li>
      <li class="page-item" v-for="page in visiblePages" :key="page" :class="{ active: page === current }">
        <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
      </li>
      <li class="page-item" :class="{ disabled: current === totalPages }">
        <a class="page-link" href="#" @click.prevent="changePage(current + 1)">下一页</a>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ current: Number, totalPages: Number })
const emit = defineEmits(['update:current'])

const visiblePages = computed(() => {
  let start = Math.max(1, props.current - 2)
  let end = Math.min(props.totalPages, start + 4)
  start = Math.max(1, end - 4)
  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
})

const changePage = (page) => {
  if (page >= 1 && page <= props.totalPages) emit('update:current', page)
}
</script>