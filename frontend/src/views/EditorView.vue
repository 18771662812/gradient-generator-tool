<template>
  <div class="editor-page">
    <div class="editor-container">
      <div class="editor-layout">
        <div class="editor-left">
          <div class="control-panel">
            <div class="type-selector">
              <button
                @click="currentGradient.type = 'linear'"
                class="type-btn"
                :class="{ active: currentGradient.type === 'linear' }"
              >
                线性渐变
              </button>
              <button
                @click="currentGradient.type = 'radial'"
                class="type-btn"
                :class="{ active: currentGradient.type === 'radial' }"
              >
                径向渐变
              </button>
            </div>
          </div>
          
          <ColorStopEditor
            :stops="currentGradient.stops"
            @update="handleStopUpdate"
            @add="gradientStore.addStop()"
            @remove="gradientStore.removeStop($event)"
          />
          
          <AnglePicker
            v-if="currentGradient.type === 'linear'"
            :angle="currentGradient.angle"
            @update="currentGradient.angle = $event"
          />
        </div>
        
        <div class="editor-right">
          <GradientPreview :css-value="cssValue" />
          
          <CSSOutput :css-value="cssValue" />
          
          <div class="save-panel">
            <h3 class="panel-title">保存方案</h3>
            
            <div class="form-group">
              <input
                v-model="currentGradient.name"
                type="text"
                placeholder="请输入方案名称"
                class="name-input"
              />
            </div>
            
            <div class="form-group toggle-group">
              <label class="toggle-label">
                <input
                  v-model="currentGradient.is_public"
                  type="checkbox"
                  class="toggle-checkbox"
                />
                <span class="toggle-slider"></span>
                <span class="toggle-text">公开到广场</span>
              </label>
            </div>
            
            <button
              @click="handleSave"
              class="btn-save"
              :disabled="saving"
            >
              {{ saving ? '保存中...' : '保存方案' }}
            </button>
            
            <div v-if="saveMessage" class="save-message" :class="saveMessageType">
              {{ saveMessage }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useGradientStore } from '@/stores/gradient'
import api from '@/api'
import AnglePicker from '@/components/AnglePicker.vue'
import ColorStopEditor from '@/components/ColorStopEditor.vue'
import CSSOutput from '@/components/CSSOutput.vue'
import GradientPreview from '@/components/GradientPreview.vue'

const route = useRoute()
const gradientStore = useGradientStore()

const currentGradient = computed(() => gradientStore.currentGradient)
const cssValue = computed(() => gradientStore.generateCSS())

const saving = ref(false)
const saveMessage = ref('')
const saveMessageType = ref('success')

const handleStopUpdate = (index, updates) => {
  gradientStore.updateStop(index, updates)
}

const handleSave = async () => {
  if (!currentGradient.value.name.trim()) {
    saveMessage.value = '请输入方案名称'
    saveMessageType.value = 'error'
    setTimeout(() => { saveMessage.value = '' }, 3000)
    return
  }
  
  saving.value = true
  saveMessage.value = ''
  
  try {
    const data = {
      name: currentGradient.value.name,
      type: currentGradient.value.type,
      angle: currentGradient.value.angle,
      stops: currentGradient.value.stops,
      css_value: cssValue.value,
      is_public: currentGradient.value.is_public
    }
    
    if (currentGradient.value.id) {
      await api.gradients.update(currentGradient.value.id, {
        name: data.name,
        is_public: data.is_public
      })
      saveMessage.value = '更新成功！'
    } else {
      const response = await api.gradients.create(data)
      currentGradient.value.id = response.data.data.id
      saveMessage.value = '保存成功！'
    }
    
    saveMessageType.value = 'success'
    setTimeout(() => { saveMessage.value = '' }, 3000)
  } catch (err) {
    saveMessage.value = err.response?.data?.error || '保存失败，请稍后重试'
    saveMessageType.value = 'error'
    setTimeout(() => { saveMessage.value = '' }, 5000)
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  const gradientId = route.params.id
  
  if (gradientId) {
    try {
      const response = await api.gradients.getById(gradientId)
      gradientStore.loadGradient(response.data.data)
    } catch (err) {
      console.error('Failed to load gradient:', err)
      alert('加载方案失败')
    }
  } else {
    gradientStore.resetGradient()
  }
})
</script>

<style scoped>
.editor-page {
  min-height: 100vh;
  background: #0a0a0f;
  padding: 20px;
}

.editor-container {
  max-width: 1600px;
  width: 100%;
  margin: 0 auto;
}

.editor-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 20px;
  align-items: start;
}

.editor-left {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.editor-right {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.control-panel {
  background: rgba(20, 20, 30, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 16px;
  backdrop-filter: blur(10px);
}

.type-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  background: transparent;
  padding: 0;
}

.type-btn {
  font-size: 13px;
  padding: 9px 0;
  text-align: center;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid #2a2a3a;
  color: #888;
  transition: all 0.15s;
  background: transparent;
}

.type-btn.active {
  background: linear-gradient(135deg, #ff6b6b22, #c084fc22);
  border-color: #84eccc55;
  color: #aaeaff;
}

.save-panel {
  background: rgba(20, 20, 30, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 20px;
  backdrop-filter: blur(10px);
}

.panel-title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 16px 0;
  letter-spacing: 0.3px;
}

.form-group {
  margin-bottom: 14px;
}

.form-group:last-of-type {
  margin-bottom: 16px;
}

.toggle-group {
  margin-bottom: 16px;
}

.name-input {
  width: 100%;
  padding: 10px 14px;
  background: rgba(15, 15, 25, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 13px;
  transition: all 0.2s;
  box-sizing: border-box;
}

.name-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.name-input:focus {
  outline: none;
  border-color: rgba(192, 132, 252, 0.5);
  background: rgba(15, 15, 25, 0.95);
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  margin: 0;
}

.toggle-checkbox {
  display: none;
}

.toggle-slider {
  position: relative;
  width: 40px;
  height: 22px;
  background: rgba(60, 60, 80, 0.6);
  border-radius: 11px;
  transition: background 0.2s;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.toggle-slider::before {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  transition: transform 0.2s;
}

.toggle-checkbox:checked + .toggle-slider {
  background: linear-gradient(135deg, #c084fc 0%, #a855f7 100%);
  border-color: transparent;
}

.toggle-checkbox:checked + .toggle-slider::before {
  transform: translateX(18px);
}

.toggle-text {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.btn-save {
  width: 100%;
  padding: 11px 20px;
  background: rgba(60, 60, 80, 0.8);
  color: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  letter-spacing: 0.3px;
}

.btn-save:hover:not(:disabled) {
  background: rgba(70, 70, 90, 0.9);
  border-color: rgba(255, 255, 255, 0.12);
  transform: translateY(-1px);
}

.btn-save:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.save-message {
  margin-top: 12px;
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 12px;
  text-align: center;
}

.save-message.success {
  background: rgba(34, 197, 94, 0.1);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.save-message.error {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

@media (max-width: 1200px) {
  .editor-layout {
    grid-template-columns: 1fr;
  }
  
  .editor-right {
    order: -1;
  }
}
</style>
