import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useGradientStore = defineStore('gradient', () => {
  const currentGradient = ref({
    id: null,
    name: '未命名方案',
    type: 'linear',
    angle: 90,
    stops: [
      { color: '#ff6b6b', position: 0 },
      { color: '#4ecdc4', position: 100 }
    ],
    is_public: false
  })

  const generateCSS = () => {
    const { type, angle, stops } = currentGradient.value
    const sortedStops = [...stops].sort((a, b) => a.position - b.position)
    const stopsStr = sortedStops.map(s => `${s.color} ${s.position}%`).join(', ')
    
    if (type === 'linear') {
      return `linear-gradient(${angle}deg, ${stopsStr})`
    } else {
      return `radial-gradient(circle, ${stopsStr})`
    }
  }

  const loadGradient = (gradient) => {
    currentGradient.value = {
      id: gradient.id,
      name: gradient.name,
      type: gradient.type,
      angle: gradient.angle,
      stops: gradient.stops,
      is_public: gradient.is_public
    }
  }

  const resetGradient = () => {
    currentGradient.value = {
      id: null,
      name: '未命名方案',
      type: 'linear',
      angle: 90,
      stops: [
        { color: '#ff6b6b', position: 0 },
        { color: '#4ecdc4', position: 100 }
      ],
      is_public: false
    }
  }

  const addStop = () => {
    if (currentGradient.value.stops.length >= 8) return
    
    const positions = currentGradient.value.stops.map(s => s.position).sort((a, b) => a - b)
    let newPosition = 50
    
    for (let i = 0; i < positions.length - 1; i++) {
      const gap = positions[i + 1] - positions[i]
      if (gap > 10) {
        newPosition = positions[i] + gap / 2
        break
      }
    }
    
    currentGradient.value.stops.push({
      color: '#ffffff',
      position: newPosition
    })
  }

  const removeStop = (index) => {
    if (currentGradient.value.stops.length <= 2) return
    currentGradient.value.stops.splice(index, 1)
  }

  const updateStop = (index, updates) => {
    Object.assign(currentGradient.value.stops[index], updates)
  }

  const setType = (type) => {
    currentGradient.value.type = type
  }

  const setAngle = (angle) => {
    currentGradient.value.angle = angle
  }

  const setStops = (stops) => {
    currentGradient.value.stops = stops.map(s => ({ ...s }))
  }

  return {
    currentGradient,
    generateCSS,
    loadGradient,
    resetGradient,
    addStop,
    removeStop,
    updateStop,
    setType,
    setAngle,
    setStops
  }
})
