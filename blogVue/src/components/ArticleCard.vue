<template>
  <!-- Bootstrap 卡片组件 (Card) -->
  <div class="card mb-3 shadow-sm">
    <div class="row g-0">   <!-- 网格行 (Grid Row) -->
      <div class="col-md-4" v-if="article.cover_image">
        <!-- 图片 (Image) -->
        <img :src="article.cover_image" class="img-fluid rounded-start" style="height: 180px; width: 100%; object-fit: cover;" />
      </div>
      <div class="col-md-8">
        <!-- 卡片主体 (Card Body) -->
        <div class="card-body">
          <router-link :to="`/articles/${article.id}`" class="text-decoration-none">
            <h5 class="card-title">{{ article.title }}</h5>
          </router-link>
          <!-- 卡片文本 (Card Text) -->
          <p class="card-text text-muted small">
            <span><i class="bi bi-person"></i> {{ article.author_name }}</span>
            <span class="ms-3"><i class="bi bi-calendar"></i> {{ timeAgo(article.created_at) }}</span>
            <span class="ms-3"><i class="bi bi-eye"></i> {{ article.views }}</span>
            <span class="ms-3"><i class="bi bi-heart"></i> {{ article.likes }}</span>
          </p>
          <p class="card-text">{{ truncate(article.content) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { timeAgo } from '@/utils/date'
const props = defineProps(['article'])
const truncate = (text, len = 120) => text?.length > len ? text.slice(0, len) + '...' : text
</script>