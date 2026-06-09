<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header">个人资料</div>
        <div class="card-body">
          <form @submit.prevent="updateProfile">
            <div class="mb-3">
              <label>用户名</label>
              <input type="text" class="form-control" v-model="profile.username" disabled />
            </div>
            <div class="mb-3">
              <label>邮箱</label>
              <input type="email" class="form-control" v-model="profile.email" disabled />
            </div>
            <div class="mb-3">
              <label>个人简介</label>
              <textarea class="form-control" rows="3" v-model="profile.bio"></textarea>
            </div>
            <div class="mb-3">
              <label>头像</label>
              <input type="file" class="form-control" @change="handleAvatarUpload" accept="image/*" />
              <div class="mt-2" v-if="profile.avatar">
                <img :src="profile.avatar" class="avatar-md" />
              </div>
            </div>
            <button type="submit" class="btn btn-primary" :disabled="saving">保存修改</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getProfile, updateProfile as updateUserProfile } from '@/api/auth'

const profile = ref({ username: '', email: '', bio: '', avatar: null })
const saving = ref(false)
const avatarFile = ref(null)

const loadProfile = async () => {
  const res = await getProfile()
  profile.value = res.data
}

const handleAvatarUpload = (e) => {
  avatarFile.value = e.target.files[0]
  if (avatarFile.value) {
    profile.value.avatar = URL.createObjectURL(avatarFile.value)
  }
}

const updateProfile = async () => {
  saving.value = true
  try {
    let data = { bio: profile.value.bio }
    if (avatarFile.value) {
      const fd = new FormData()
      fd.append('bio', profile.value.bio)
      fd.append('avatar', avatarFile.value)
      data = fd
    }
    await updateUserProfile(data)   // 调用重命名后的 API 函数
    alert('更新成功')
  } catch (err) {
    console.error(err)
    alert('更新失败')
  } finally {
    saving.value = false
  }
}

onMounted(loadProfile)
</script>