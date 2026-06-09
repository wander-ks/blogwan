<template>
  <div class="row justify-content-center">
    <div class="col-md-10">
      <div class="card">
        <div class="card-header">{{ isEdit ? '编辑文章' : '发布新文章' }}</div>
        <div class="card-body">
          <!-- 表单 (Form) -->
          <form @submit.prevent="submit">
            <div class="mb-3">
              <label class="form-label">标题</label>
              <input type="text" class="form-control" v-model="form.title" required />
            </div>
            <div class="mb-3">
              <label class="form-label">封面图</label>
              <input type="file" class="form-control" @change="handleCoverUpload" accept="image/*" />
              <div v-if="form.cover_image" class="mt-2">
                <img :src="form.cover_image" style="max-height: 150px;" />
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">正文（支持Markdown）</label>
              <textarea class="form-control" rows="12" v-model="form.content" required></textarea>
            </div>
            <div class="form-check mb-3">
              <input type="checkbox" class="form-check-input" v-model="form.is_published" />
              <label class="form-check-label">立即发布</label>
            </div>
            <!-- 按钮组 -->
            <button type="submit" class="btn btn-primary" :disabled="submitting">保存</button>
            <router-link to="/" class="btn btn-secondary ms-2">取消</router-link>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { createArticle, updateArticle, getArticle } from '@/api/article'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const submitting = ref(false)
const form = ref({
  title: '',
  content: '',
  cover_image: null,
  is_published: true,
})

const loadArticle = async () => {
  if (!isEdit.value) return
  // 发布成功后触发积分刷新
  window.dispatchEvent(new CustomEvent('pointsUpdated'))
  const res = await getArticle(route.params.id)
  form.value = {
    title: res.data.title,
    content: res.data.content,
    cover_image: res.data.cover_image,
    is_published: res.data.is_published,
  }
}

const handleCoverUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    form.value.cover_file = file
    form.value.cover_image = URL.createObjectURL(file)
  }
}

const submit = async () => {
  submitting.value = true
  try {
    let data
    if (form.value.cover_file) {
      const fd = new FormData()
      fd.append('title', form.value.title)
      fd.append('content', form.value.content)
      fd.append('is_published', form.value.is_published)
      fd.append('cover_image', form.value.cover_file)
      data = fd
    } else {
      data = {
        title: form.value.title,
        content: form.value.content,
        is_published: form.value.is_published,
        cover_image: form.value.cover_image,
      }
    }
    if (isEdit.value) {
      await updateArticle(route.params.id, data)
    } else {
      await createArticle(data)
    }
    router.push('/')
  } catch (err) {
    console.error(err)
    alert('保存失败')
  } finally {
    submitting.value = false
  }
}

onMounted(loadArticle)
</script>