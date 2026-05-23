<template>
  <div class="css-output">
    <h3 class="output-title">CSS 代码</h3>
    
    <div class="output-container">
      <pre class="css-code">{{ cssValue }}</pre>
      
      <button 
        @click="handleCopy" 
        class="btn-copy"
        :class="{ 'copied': copied }"
      >
        {{ copied ? '已复制' : '复制 CSS' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  cssValue: {
    type: String,
    required: true
  }
})

const copied = ref(false)
let copyTimeout = null

const handleCopy = async () => {
  try {
    await navigator.clipboard.writeText(props.cssValue)
    copied.value = true
    
    if (copyTimeout) clearTimeout(copyTimeout)
    copyTimeout = setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
    alert('复制失败，请手动复制')
  }
}
</script>

<style scoped>
.css-output {
  background: rgba(20, 20, 30, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 8px;
  padding: 20px;
  backdrop-filter: blur(10px);
}

.output-title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 12px 0;
  letter-spacing: 0.3px;
}

.output-container {
  position: relative;
}

.css-code {
  background: rgba(10, 10, 20, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 6px;
  padding: 14px;
  color: #4ade80;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.6;
  overflow-x: auto;
  margin: 0 0 10px 0;
  white-space: pre-wrap;
  word-break: break-all;
}

.btn-copy {
  width: 100%;
  padding: 9px 16px;
  background: rgba(30, 30, 45, 0.8);
  color: rgba(255, 255, 255, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-copy:hover {
  background: rgba(40, 40, 55, 0.9);
  color: rgba(255, 255, 255, 0.9);
  border-color: rgba(255, 255, 255, 0.12);
}

.btn-copy.copied {
  background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
  color: #ffffff;
  border-color: transparent;
}
</style>
