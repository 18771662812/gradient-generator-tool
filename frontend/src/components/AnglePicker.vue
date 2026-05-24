<template>
  <div class="angle-picker">
    <h3 class="picker-title">角度</h3>
    
    <div class="picker-container">
      <div class="angle-dial" @mousedown="startDrag">
        <svg width="120" height="120" viewBox="0 0 120 120">
          <circle
            cx="60"
            cy="60"
            r="50"
            fill="none"
            stroke="rgba(255, 255, 255, 0.08)"
            stroke-width="1.5"
          />
          <line
            :x1="60"
            :y1="60"
            :x2="lineX"
            :y2="lineY"
            stroke="url(#gradient)"
            stroke-width="2.5"
            stroke-linecap="round"
          />
          <circle
            :cx="lineX"
            :cy="lineY"
            r="6"
            fill="#60a5fa"
          />
          <defs>
            <linearGradient id="gradient" gradientUnits="userSpaceOnUse" x1="10" y1="10" x2="110" y2="110">
              <stop offset="0%" style="stop-color:#c084fc;stop-opacity:1" />
              <stop offset="100%" style="stop-color:#60a5fa;stop-opacity:1" />
            </linearGradient>
          </defs>
        </svg>
        <div class="angle-display">{{ angle }}°</div>
      </div>
      
      <div class="angle-input-group">
        <input
          type="number"
          :value="angle"
          @input="handleInput"
          min="0"
          max="360"
          class="angle-input"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  angle: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update'])

const isDragging = ref(false)

const lineX = computed(() => {
  const radians = (props.angle - 90) * (Math.PI / 180)
  return 60 + Math.cos(radians) * 50
})

const lineY = computed(() => {
  const radians = (props.angle - 90) * (Math.PI / 180)
  return 60 + Math.sin(radians) * 50
})

const calculateAngle = (event) => {
  const dial = event.currentTarget
  const rect = dial.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2
  const deltaX = event.clientX - centerX
  const deltaY = event.clientY - centerY
  
  let angle = Math.atan2(deltaY, deltaX) * (180 / Math.PI) + 90
  if (angle < 0) angle += 360
  
  return Math.round(angle)
}

const startDrag = (event) => {
  isDragging.value = true
  const newAngle = calculateAngle(event)
  emit('update', newAngle)
}

const handleMouseMove = (event) => {
  if (!isDragging.value) return
  
  const dial = document.querySelector('.angle-dial')
  if (!dial) return
  
  const rect = dial.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2
  const deltaX = event.clientX - centerX
  const deltaY = event.clientY - centerY
  
  let angle = Math.atan2(deltaY, deltaX) * (180 / Math.PI) + 90
  if (angle < 0) angle += 360
  
  emit('update', Math.round(angle))
}

const stopDrag = () => {
  isDragging.value = false
}

const handleInput = (event) => {
  let value = parseInt(event.target.value)
  if (isNaN(value)) value = 0
  if (value < 0) value = 0
  if (value > 360) value = 360
  emit('update', value)
}

onMounted(() => {
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', stopDrag)
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', stopDrag)
})
</script>

<style scoped>
.angle-picker {
  background: rgba(20, 20, 30, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 20px;
  backdrop-filter: blur(10px);
}

.picker-title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 16px 0;
  letter-spacing: 0.3px;
}

.picker-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.angle-dial {
  position: relative;
  cursor: pointer;
  user-select: none;
  flex-shrink: 0;
}

.angle-display {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 18px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  pointer-events: none;
}

.angle-input-group {
  flex: 1;
  display: flex;
  align-items: center;
}

.angle-input {
  width: 100%;
  padding: 10px 14px;
  background: rgba(15, 15, 25, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 13px;
  text-align: center;
  font-weight: 600;
  transition: all 0.2s;
}

.angle-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.angle-input:focus {
  outline: none;
  border-color: rgba(192, 132, 252, 0.5);
  background: rgba(15, 15, 25, 0.95);
}

.angle-input::-webkit-inner-spin-button,
.angle-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>
