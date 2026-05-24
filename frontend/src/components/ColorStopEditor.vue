<template>
  <div class="color-stop-editor">
    <div class="editor-header">
      <h3 class="editor-title">色标</h3>
      <button 
        @click="$emit('add')" 
        class="btn-add"
        :disabled="stops.length >= 8"
      >
        + 添加
      </button>
    </div>
    
    <div class="stops-list">
      <div 
        v-for="(stop, index) in stops" 
        :key="index"
        class="stop-item"
      >
        <div class="stop-color">
          <input
            type="color"
            :value="stop.color"
            @input="handleColorChange(index, $event.target.value)"
            class="color-picker"
          />
          <input
            type="text"
            :value="stop.color"
            @input="handleColorChange(index, $event.target.value)"
            class="color-input"
            placeholder="#000000"
          />
        </div>
        
        <div class="stop-position">
          <input
            type="range"
            :value="stop.position"
            @input="handlePositionChange(index, $event.target.value)"
            min="0"
            max="100"
            class="position-slider"
          />
          <div class="position-value">
            <input
              type="number"
              :value="stop.position"
              @input="handlePositionChange(index, $event.target.value)"
              min="0"
              max="100"
              class="position-input"
            />
            <span class="position-unit">%</span>
          </div>
        </div>
        
        <button
          @click="$emit('remove', index)"
          class="btn-remove"
          :disabled="stops.length <= 2"
          title="删除"
        >
          ×
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  stops: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['update', 'add', 'remove'])

const handleColorChange = (index, color) => {
  emit('update', index, { color })
}

const handlePositionChange = (index, position) => {
  emit('update', index, { position: Number(position) })
}
</script>

<style scoped>
.color-stop-editor {
  background: rgba(20, 20, 30, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 20px;
  backdrop-filter: blur(10px);
}

.editor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.editor-title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  letter-spacing: 0.3px;
}

.btn-add {
  padding: 6px 12px;
  background: rgba(30, 30, 45, 0.8);
  color: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 5px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-add:hover:not(:disabled) {
  background: rgba(40, 40, 55, 0.9);
  color: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 255, 255, 0.12);
}

.btn-add:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.stops-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.stop-item {
  display: grid;
  grid-template-columns: 140px 1fr 32px;
  gap: 12px;
  align-items: center;
  padding: 12px;
  background: rgba(15, 15, 25, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 6px;
  transition: all 0.2s;
}

.stop-item:hover {
  background: rgba(15, 15, 25, 0.8);
  border-color: rgba(255, 255, 255, 0.08);
}

.stop-color {
  display: flex;
  gap: 8px;
  align-items: center;
}

.color-picker {
  width: 36px;
  height: 36px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  cursor: pointer;
  background: transparent;
  flex-shrink: 0;
}

.color-picker::-webkit-color-swatch-wrapper {
  padding: 2px;
}

.color-picker::-webkit-color-swatch {
  border: none;
  border-radius: 4px;
}

.color-input {
  flex: 1;
  padding: 8px 10px;
  background: rgba(10, 10, 20, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 5px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 12px;
  font-family: 'Consolas', 'Monaco', monospace;
  transition: all 0.2s;
}

.color-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.color-input:focus {
  outline: none;
  border-color: rgba(192, 132, 252, 0.4);
  background: rgba(10, 10, 20, 0.95);
}

.stop-position {
  display: flex;
  gap: 10px;
  align-items: center;
}

.position-slider {
  flex: 1;
  height: 4px;
  background: rgba(60, 60, 80, 0.5);
  border-radius: 2px;
  outline: none;
  -webkit-appearance: none;
  cursor: pointer;
}

.position-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 14px;
  height: 14px;
  background: #60a5fa;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.position-slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}

.position-slider::-moz-range-thumb {
  width: 14px;
  height: 14px;
  background: #60a5fa;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.2s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.position-slider::-moz-range-thumb:hover {
  transform: scale(1.15);
}

.position-value {
  display: flex;
  align-items: center;
  gap: 4px;
}

.position-input {
  width: 42px;
  padding: 6px 8px;
  background: rgba(10, 10, 20, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 5px;
  color: rgba(255, 255, 255, 0.9);
  font-size: 12px;
  text-align: center;
  font-weight: 500;
  transition: all 0.2s;
}

.position-input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.position-input:focus {
  outline: none;
  border-color: rgba(192, 132, 252, 0.4);
  background: rgba(10, 10, 20, 0.95);
}

.position-input::-webkit-inner-spin-button,
.position-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.position-unit {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 500;
}

.btn-remove {
  width: 32px;
  height: 32px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 5px;
  font-size: 20px;
  line-height: 1;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.btn-remove:hover:not(:disabled) {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.3);
  color: #f87171;
}

.btn-remove:disabled {
  opacity: 0.25;
  cursor: not-allowed;
}
</style>
