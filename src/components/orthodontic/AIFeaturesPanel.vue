<template>
  <div>
    <!-- AI Toggle Button -->
    <button class="ai-toggle-btn" @click="isOpen = !isOpen">
      🤖 Photos AI Settings
    </button>

    <!-- AI Panel -->
    <div class="ai-panel" :class="{ open: isOpen }">
      <div class="ai-panel-header">
        <div class="ai-panel-title">
          🤖 AI Features
        </div>
        <button class="ai-close-btn" @click="isOpen = false">×</button>
      </div>
      
      <div class="ai-option" v-for="(option, key) in options" :key="key" :class="{ disabled: option.disabled }">
        <input type="checkbox" :id="key" v-model="settings[key]" :disabled="option.disabled">
        <div class="ai-option-content">
          <div class="ai-option-title">{{ option.title }}</div>
          <div class="ai-option-desc">{{ option.desc }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIFeaturesPanel',
  data() {
    return {
      isOpen: false,
      settings: {
        colorCorrection: true,
        autoEnhance: true,
        intraoralCrop: true,
        smartFlip: false,
        faceDetection: false,
        backgroundRemoval: false,
        blurDetection: true,
        noiseReduction: false
      },
      options: {
        colorCorrection: { title: 'Color Standardization', desc: 'Auto white balance & color correction' },
        autoEnhance: { title: 'Auto Enhancement', desc: 'Optimize brightness, contrast & sharpness' },
        intraoralCrop: { title: 'Intraoral Auto-Crop', desc: 'Remove black backgrounds from dental photos' },
        smartFlip: { title: 'Intraoral Smart Flip', desc: 'Auto-flip mirror photos (horizontal)' },
        faceDetection: { title: 'Smart Cropping', desc: 'Auto-center face & remove excess background' },
        backgroundRemoval: { title: 'Background Removal', desc: 'Clean white background (slower)' },
        blurDetection: { title: 'Quality Check', desc: 'Detect blurry or low-quality images' },
        noiseReduction: { title: 'Noise Reduction', desc: 'Reduce grain & improve clarity' }
      }
    };
  },
  watch: {
    settings: {
      deep: true,
      handler(val) {
        this.$emit('update:settings', val);
      }
    }
  }
};
</script>

<style lang="scss" scoped>
$photon-primary: #EA5A43;
$photon-primary-soft: #FFE4DE;
$photon-dark: #222222;
$photon-muted: #777777;
$radius-lg: 16px;
$radius-sm: 8px;
$shadow-lg: 0 8px 24px rgba(0,0,0,0.12);

.ai-panel {
  position: fixed;
  top: 120px; /* Adjusted for header */
  right: 32px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: $radius-lg;
  padding: 20px;
  box-shadow: $shadow-lg;
  z-index: 10000;
  max-width: 340px;
  display: none;
  
  &.open { 
    display: block;
    animation: slideInRight 0.3s ease;
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.ai-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0f0f0;
}

.ai-panel-title {
  font-size: 16px;
  font-weight: 700;
  color: $photon-dark;
  display: flex;
  align-items: center;
  gap: 8px;
}

.ai-close-btn {
  background: #f8f9fa;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
  color: $photon-muted;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  
  &:hover { 
    background: $photon-primary-soft;
    color: $photon-primary;
  }
}

.ai-option {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  margin-bottom: 8px;
  border-radius: $radius-sm;
  background: #fafbfc;
  transition: all 0.2s ease;
  
  &:last-child { margin-bottom: 0; }
  &:hover { background: #f1f3f5; }
  
  input[type="checkbox"] {
    margin-top: 2px;
    cursor: pointer;
    accent-color: $photon-primary;
    width: 18px;
    height: 18px;
  }
}

.ai-option-content {
  flex: 1;
}

.ai-option-title {
  font-size: 13px;
  font-weight: 700;
  color: $photon-dark;
  margin-bottom: 4px;
}

.ai-option-desc {
  font-size: 12px;
  color: $photon-muted;
  line-height: 1.4;
}

.ai-toggle-btn {
  position: fixed;
  bottom: 100px;
  right: 32px;
  background: linear-gradient(135deg, $photon-primary 0%, #d94d36 100%);
  color: white;
  border: none;
  border-radius: 50px;
  padding: 16px 24px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(234, 90, 67, 0.4);
  z-index: 9999;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(234, 90, 67, 0.5);
  }
  
  &:active {
    transform: translateY(-1px);
  }
}
</style>
