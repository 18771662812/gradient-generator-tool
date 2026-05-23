<template>
  <div class="gradient-preview">
    <h3 class="preview-title">实时预览</h3>
    
    <div class="preview-container">
      <div class="preview-main" :style="{ background: cssValue }"></div>
      
      <div class="preview-grid">
        <div class="preview-button" :style="{ background: cssValue }">
          <span class="card-label">点击按钮</span>
        </div>
        <div class="preview-card" :style="{ background: cssValue }">
          <div class="card-content">
            <span class="card-label">示例卡片</span>
            <div class="card-lines">
              <div class="line line-long"></div>
              <div class="line line-short"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  cssValue: {
    type: String,
    required: true
  }
})
</script>

<style scoped>
.gradient-preview {
  background: rgba(20, 20, 30, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 20px;
  backdrop-filter: blur(10px);
  position: sticky;
  top: 20px;
}

.preview-title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 16px 0;
  letter-spacing: 0.3px;
}

.preview-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.preview-main {
  width: 100%;
  height: 280px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.preview-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.preview-button {
  height: 60px;
  border-radius: 30px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.preview-card {
  height: 120px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  position: relative;
  overflow: hidden;
  padding: 16px;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.card-label {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  z-index: 1;
  letter-spacing: 0.3px;
}

.card-lines {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.line {
  height: 8px;
  background: rgba(255, 255, 255, 0.25);
  border-radius: 4px;
}

.line-long {
  width: 100%;
}

.line-short {
  width: 60%;
}

@media (max-width: 768px) {
  .preview-grid {
    grid-template-columns: 1fr;
  }
}
</style>
