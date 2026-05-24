<script setup>
import { ref, computed } from 'vue'
import { recommendGradients } from '@/api/index.js'
import { useGradientStore } from '@/stores/gradient'

const gradientStore = useGradientStore()

const baseColor = ref('#ff6b6b')
const schemes = ref([])
const loading = ref(false)
const error = ref('')
const selectedIndex = ref(null)
const hasLoaded = ref(false)

const selectedScheme = computed(() =>
  selectedIndex.value !== null ? schemes.value[selectedIndex.value] : null
)

async function fetchRecommend() {
  loading.value = true
  error.value = ''
  selectedIndex.value = null
  try {
    const res = await recommendGradients(baseColor.value)
    schemes.value = res.data.schemes
    hasLoaded.value = true
    if (schemes.value.length > 0) {
      selectedIndex.value = 0
    }
  } catch (e) {
    error.value = '推荐失败，请重试'
    schemes.value = []
  } finally {
    loading.value = false
  }
}

function selectScheme(index) {
  selectedIndex.value = index
}

function applyScheme() {
  if (!selectedScheme.value) return
  const scheme = selectedScheme.value
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
      <span class="rec-desc">选择基准色，自动生成 5 套配色方案</span>
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
        :class="{ active: selectedIndex === i }"
        @click="selectScheme(i)"
      >
        <div class="scheme-preview" :style="{ background: scheme.css_value }"></div>
        <div class="scheme-footer">
          <span class="active-dot" v-if="selectedIndex === i"></span>
          <span class="scheme-name">{{ scheme.name }}</span>
        </div>
      </div>
    </div>

    <div class="empty-hint" v-else-if="!loading && !hasLoaded">
      <i class="ti ti-palette" aria-hidden="true"></i>
      <span>选好基准色后点击「生成推荐」</span>
    </div>

    <div class="rec-actions" v-if="selectedScheme">
      <div class="selected-css">{{ selectedScheme.css_value }}</div>
      <button class="apply-btn" @click="applyScheme">
        加载到编辑器 <i class="ti ti-arrow-right" aria-hidden="true"></i>
      </button>
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
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}
.rec-desc {
  font-size: 12px;
  color: var(--text-muted);
  flex: 1;
}

.color-pick-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-mid);
  background: var(--bg-deep);
  cursor: pointer;
  position: relative;
  flex-shrink: 0;
}
.color-swatch {
  width: 18px;
  height: 18px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-mid);
  flex-shrink: 0;
}
.color-pick-label {
  font-size: 12px;
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
  border-color: var(--border-mid);
  transform: translateY(-2px);
}
.scheme-card.active {
  border-color: rgba(192, 132, 252, 0.6);
  box-shadow: 0 0 0 1px rgba(192, 132, 252, 0.2);
}

.scheme-preview {
  height: 60px;
  width: 100%;
}

.scheme-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 5px 4px 6px;
  background: var(--bg-deep);
}
.active-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--accent-purple);
  flex-shrink: 0;
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

.rec-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.selected-css {
  font-size: 11px;
  font-family: monospace;
  color: var(--accent-teal);
  background: var(--bg-deep);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 8px 10px;
  word-break: break-all;
  line-height: 1.6;
}
.apply-btn {
  width: 100%;
  padding: 9px;
  font-size: 13px;
  font-weight: 500;
  color: #fff;
  background: var(--grad-main);
  border: none;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: opacity 0.15s;
}
.apply-btn:hover { opacity: 0.88; }
</style>
