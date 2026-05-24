<script setup>
import { ref } from 'vue'
import { recommendGradients } from '@/api/index.js'
import { useGradientStore } from '@/stores/gradient'

const gradientStore = useGradientStore()

const baseColor = ref('#ff6b6b')
const schemes = ref([])
const loading = ref(false)
const error = ref('')
const hasLoaded = ref(false)

async function fetchRecommend() {
  loading.value = true
  error.value = ''
  try {
    const res = await recommendGradients(baseColor.value)
    schemes.value = res.data.schemes
    hasLoaded.value = true
  } catch (e) {
    error.value = '推荐失败，请重试'
    schemes.value = []
  } finally {
    loading.value = false
  }
}

function applyScheme(index) {
  const scheme = schemes.value[index]
  if (!scheme) return
  gradientStore.setType('linear')
  gradientStore.setAngle(scheme.angle)
  gradientStore.setStops(scheme.stops)
}

function onColorChange(e) {
  baseColor.value = e.target.value
}
</script>

<template>
  <div class="recommend-panel">
    <div class="rec-top">
      <div class="rec-left">
        <span class="rec-title">智能推荐</span>
        <span class="rec-desc">选择基准色，自动生成 5 套配色方案</span>
      </div>
      <label class="color-pick-btn">
        <div class="color-swatch" :style="{ background: baseColor }"></div>
        <span class="color-pick-label">{{ baseColor }}</span>
        <input type="color" class="color-native" :value="baseColor" @input="onColorChange" />
      </label>
    </div>

    <button class="gen-btn" @click="fetchRecommend" :disabled="loading">
      <i class="ti ti-sparkles" aria-hidden="true"></i>
      {{ loading ? '生成中...' : '生成推荐' }}
    </button>

    <div class="error-msg" v-if="error">{{ error }}</div>

    <div class="schemes-row" v-if="schemes.length > 0">
      <div
        v-for="(scheme, i) in schemes"
        :key="i"
        class="scheme-card"
        @click="applyScheme(i)"
      >
        <div class="scheme-preview" :style="{ background: scheme.css_value }">
          <span class="scheme-hover">加载</span>
        </div>
        <div class="scheme-footer">
          <span class="scheme-name">{{ scheme.name }}</span>
        </div>
      </div>
    </div>

    <div class="empty-hint" v-else-if="!loading && !hasLoaded">
      <i class="ti ti-palette" aria-hidden="true"></i>
      <span>选好基准色后点击「生成推荐」</span>
    </div>
  </div>
</template>

<style scoped>
.recommend-panel {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.rec-top {
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: 12px;
}

.rec-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 2px;
  flex: 1;
}

.rec-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 0.3px;
}

.rec-desc {
  font-size: 12px;
  color: var(--text-muted);
}

.color-pick-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-mid);
  background: var(--bg-deep);
  cursor: pointer;
  position: relative;
  flex-shrink: 0;
}
.color-swatch {
  width: 22px;
  height: 22px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-mid);
  flex-shrink: 0;
}
.color-pick-label {
  font-size: 13px;
  color: var(--text-secondary);
  font-family: monospace;
}
.color-native {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  cursor: pointer;
}

.gen-btn {
  width: 100%;
  padding: 9px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
  background: transparent;
  border: 1px solid var(--border-mid);
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: border-color 0.15s, background 0.15s;
}
.gen-btn:hover:not(:disabled) {
  border-color: var(--accent-purple);
  background: rgba(192, 132, 252, 0.06);
  color: var(--accent-purple);
}
.gen-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.error-msg {
  font-size: 12px;
  color: var(--danger);
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.25);
  border-radius: var(--radius-md);
  padding: 7px 10px;
}

.schemes-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.scheme-card {
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--border-subtle);
  cursor: pointer;
  transition: border-color 0.15s, transform 0.15s;
}
.scheme-card:hover {
  border-color: var(--accent-purple);
  transform: translateY(-2px);
}

.scheme-preview {
  height: 60px;
  width: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.scheme-hover {
  opacity: 0;
  font-size: 12px;
  font-weight: 600;
  color: #fff;
  background: rgba(0, 0, 0, 0.45);
  padding: 3px 10px;
  border-radius: 4px;
  transition: opacity 0.15s;
  pointer-events: none;
}
.scheme-card:hover .scheme-hover {
  opacity: 1;
}

.scheme-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px 4px 6px;
  background: var(--bg-deep);
}
.scheme-name {
  font-size: 10px;
  color: var(--text-muted);
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.empty-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 20px;
  color: var(--text-hint);
  font-size: 12px;
  border: 1px dashed var(--border-subtle);
  border-radius: var(--radius-md);
}
.empty-hint .ti { font-size: 16px; }
</style>
