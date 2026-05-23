<template>
  <div class="favorites-page">
    <div class="favorites-container">
      <div class="page-header">
        <h1 class="title">我的收藏</h1>
        <p class="subtitle">你收藏的精美渐变方案</p>
      </div>
      
      <div v-if="loading" class="loading">加载中...</div>
      
      <div v-else-if="error" class="error-message">{{ error }}</div>
      
      <div v-else-if="gradients.length === 0" class="empty-state">
        <div class="empty-icon">⭐</div>
        <p>还没有收藏任何方案</p>
        <p class="empty-hint">去广场发现更多精彩作品吧！</p>
        <router-link to="/plaza" class="btn-explore">探索广场</router-link>
      </div>
      
      <div v-else class="gradients-grid">
        <GradientCard
          v-for="gradient in gradients"
          :key="gradient.id"
          :gradient="gradient"
          :show-author="true"
          :show-favorite-button="true"
          @click="handleCardClick"
          @favorite="handleUnfavorite"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGradientStore } from '@/stores/gradient'
import api from '@/api'
import GradientCard from '@/components/GradientCard.vue'

const router = useRouter()
const gradientStore = useGradientStore()

const gradients = ref([])
const loading = ref(true)
const error = ref('')

const loadFavorites = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await api.favorites.getAll()
    gradients.value = response.data.data.map(g => ({
      ...g,
      is_favorited: true
    }))
  } catch (err) {
    error.value = '加载失败，请稍后重试'
    console.error('Failed to load favorites:', err)
  } finally {
    loading.value = false
  }
}

const handleCardClick = (gradient) => {
  gradientStore.loadGradient(gradient)
  router.push('/editor')
}

const handleUnfavorite = async (gradient) => {
  try {
    await api.favorites.remove(gradient.id)
    gradients.value = gradients.value.filter(g => g.id !== gradient.id)
  } catch (err) {
    const errorMsg = err.response?.data?.error || '取消收藏失败'
    alert(errorMsg)
  }
}

onMounted(() => {
  loadFavorites()
})
</script>

<style scoped>
.favorites-page {
  min-height: 100vh;
  background: #0f0f13;
  padding: 40px 24px;
}

.favorites-container {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
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
  margin-bottom: 32px;
}

.btn-explore {
  display: inline-block;
  padding: 14px 32px;
  background: #7c6aff;
  color: #ffffff;
  text-decoration: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-explore:hover {
  background: #6a58e6;
  transform: translateY(-1px);
}

.gradients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

@media (max-width: 768px) {
  .page-header {
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
