<template>
  <div class="plaza-page">
    <div class="plaza-container">
      <div class="plaza-header">
        <h1 class="title">公共广场</h1>
        <p class="subtitle">探索社区创作的精美渐变方案</p>
      </div>
      
      <div v-if="loading" class="loading">加载中...</div>
      
      <div v-else-if="error" class="error-message">{{ error }}</div>
      
      <div v-else-if="gradients.length === 0" class="empty-state">
        <div class="empty-icon">🎨</div>
        <p>暂无公开方案</p>
        <p class="empty-hint">成为第一个分享作品的人吧！</p>
      </div>
      
      <div v-else class="gradients-grid">
        <GradientCard
          v-for="gradient in gradients"
          :key="gradient.id"
          :gradient="gradient"
          :show-author="true"
          :show-favorite-button="true"
          @click="handleCardClick"
          @favorite="handleFavorite"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useGradientStore } from '@/stores/gradient'
import api from '@/api'
import GradientCard from '@/components/GradientCard.vue'

const router = useRouter()
const authStore = useAuthStore()
const gradientStore = useGradientStore()

const gradients = ref([])
const loading = ref(true)
const error = ref('')

const loadGradients = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await api.plaza.getAll()
    gradients.value = response.data.data
  } catch (err) {
    error.value = '加载失败，请稍后重试'
    console.error('Failed to load plaza gradients:', err)
  } finally {
    loading.value = false
  }
}

const handleCardClick = (gradient) => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  gradientStore.loadGradient(gradient)
  router.push('/editor')
}

const handleFavorite = async (gradient) => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    router.push('/login')
    return
  }
  
  try {
    if (gradient.is_favorited) {
      await api.favorites.remove(gradient.id)
      gradient.is_favorited = false
    } else {
      await api.favorites.add(gradient.id)
      gradient.is_favorited = true
    }
  } catch (err) {
    const errorMsg = err.response?.data?.error || '操作失败'
    alert(errorMsg)
  }
}

onMounted(() => {
  loadGradients()
})
</script>

<style scoped>
.plaza-page {
  min-height: 100vh;
  background: #0f0f13;
  padding: 40px 24px;
}

.plaza-container {
  max-width: 1400px;
  margin: 0 auto;
}

.plaza-header {
  text-align: center;
  margin-bottom: 48px;
}

.title {
  font-size: 48px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 12px 0;
}

.subtitle {
  font-size: 18px;
  color: #a0a0b0;
  margin: 0;
}

.loading {
  text-align: center;
  padding: 80px 20px;
  font-size: 16px;
  color: #a0a0b0;
}

.error-message {
  text-align: center;
  padding: 80px 20px;
  color: #ff6b6b;
  font-size: 16px;
}

.empty-state {
  text-align: center;
  padding: 120px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 24px;
}

.empty-state p {
  font-size: 18px;
  color: #a0a0b0;
  margin: 8px 0;
}

.empty-hint {
  font-size: 14px;
  color: #6a6a7a;
}

.gradients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

@media (max-width: 768px) {
  .plaza-header {
    margin-bottom: 32px;
  }
  
  .title {
    font-size: 36px;
  }
  
  .subtitle {
    font-size: 16px;
  }
  
  .gradients-grid {
    grid-template-columns: 1fr;
  }
}
</style>
