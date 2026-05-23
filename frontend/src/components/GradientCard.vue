<template>
  <div class="gradient-card" @click="handleClick">
    <div class="gradient-preview" :style="{ background: gradient.css_value }"></div>
    
    <div class="card-content">
      <div class="card-header">
        <h3 class="gradient-name">{{ gradient.name }}</h3>
        <span v-if="showAuthor" class="author">by {{ gradient.author }}</span>
      </div>
      
      <div class="card-footer">
        <span class="timestamp">{{ formatDate(gradient.created_at) }}</span>
        
        <div class="card-actions">
          <span v-if="showPublicBadge && gradient.is_public" class="badge badge-public">公开</span>
          <span v-if="showPublicBadge && !gradient.is_public" class="badge badge-private">私有</span>
          
          <button
            v-if="showFavoriteButton"
            @click.stop="handleFavorite"
            class="btn-icon"
            :class="{ 'is-favorited': gradient.is_favorited }"
            :disabled="favoriteLoading"
          >
            {{ gradient.is_favorited ? '❤️' : '🤍' }}
          </button>
          
          <button
            v-if="showEditButton"
            @click.stop="handleEdit"
            class="btn-icon"
            title="编辑"
          >
            ✏️
          </button>
          
          <button
            v-if="showDeleteButton"
            @click.stop="handleDelete"
            class="btn-icon btn-danger"
            title="删除"
          >
            🗑️
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  gradient: {
    type: Object,
    required: true
  },
  showAuthor: {
    type: Boolean,
    default: false
  },
  showPublicBadge: {
    type: Boolean,
    default: false
  },
  showFavoriteButton: {
    type: Boolean,
    default: false
  },
  showEditButton: {
    type: Boolean,
    default: false
  },
  showDeleteButton: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click', 'favorite', 'edit', 'delete'])

const favoriteLoading = ref(false)

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  if (days < 30) return `${Math.floor(days / 7)}周前`
  if (days < 365) return `${Math.floor(days / 30)}个月前`
  return `${Math.floor(days / 365)}年前`
}

const handleClick = () => {
  emit('click', props.gradient)
}

const handleFavorite = async () => {
  favoriteLoading.value = true
  try {
    await emit('favorite', props.gradient)
  } finally {
    favoriteLoading.value = false
  }
}

const handleEdit = () => {
  emit('edit', props.gradient)
}

const handleDelete = () => {
  emit('delete', props.gradient)
}
</script>

<style scoped>
.gradient-card {
  background: #1a1a24;
  border: 1px solid #2a2a3a;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}

.gradient-card:hover {
  border-color: #3a3a4a;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.gradient-preview {
  width: 100%;
  height: 180px;
}

.card-content {
  padding: 16px;
}

.card-header {
  margin-bottom: 12px;
}

.gradient-name {
  font-size: 16px;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.author {
  font-size: 13px;
  color: #7c6aff;
  font-weight: 500;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.timestamp {
  font-size: 12px;
  color: #6a6a7a;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-public {
  background: rgba(78, 205, 196, 0.15);
  color: #4ecdc4;
}

.badge-private {
  background: rgba(160, 160, 176, 0.15);
  color: #a0a0b0;
}

.btn-icon {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-icon:hover {
  background: rgba(255, 255, 255, 0.05);
}

.btn-icon:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-icon.is-favorited {
  animation: heartbeat 0.3s ease;
}

.btn-danger:hover {
  background: rgba(255, 107, 107, 0.15);
}

@keyframes heartbeat {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.2); }
}
</style>
