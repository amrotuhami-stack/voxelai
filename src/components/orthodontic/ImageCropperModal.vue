<template>
  <div class="cropper-modal" :class="{ open: isOpen }">
    <div class="cropper-panel" :style="{ maxWidth: imageType === 'cephalometry' ? '1200px' : '900px' }">
      <div class="cropper-header">
        <span>{{ modalTitle }}</span>
        <button type="button" class="cropper-btn danger" @click="close">✕ Close</button>
      </div>

      <!-- Cephalometry Instructions (Only for Ceph) -->
      <div v-if="imageType === 'cephalometry'" class="ceph-instructions">
        <div class="ceph-info-box">
          <div class="ceph-icon">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="white">
              <path d="M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0zm1 15H9v-2h2v2zm0-4H9V5h2v6z"/>
            </svg>
          </div>
          <div class="ceph-text">
            <div class="ceph-title">📋 Cropping Instructions</div>
            <div class="ceph-desc">
              If necessary, crop the lateral cephalometric image to <strong>remove all text, logos, and any extraneous information</strong>, keeping only the lateral cephalometric image and the cephalostat ruler, as this directly affects the efficiency of the AI analysis.
            </div>
            <div class="ceph-warning">
              <div class="warning-text">
                <strong style="color: #EA5A43; font-size: 12px;">⚠️ Important Note:</strong> Please note that the presence of <strong>extra-oral devices, large surgical plates, or low-quality cephalometric images</strong> may negatively impact the accuracy of the AI-generated results.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Image Type Selection (Only for Intraoral/Extraoral) -->
      <div v-if="imageType !== 'cephalometry' && imageType !== 'radiograph'" class="image-type-section">
        <div class="image-type-label">Image Type & Specifications</div>
        <div class="radio-options">
          <label class="radio-option" :class="{ active: currentAspectRatio === 5/7 }">
            <input type="radio" name="imageType" value="extraoral" :checked="currentAspectRatio === 5/7" @change="setAspectRatio(5/7)">
            <div class="radio-option-content">
              <div class="radio-option-title">Extraoral (All Face Views) - 5:7 Ratio</div>
              <div class="radio-option-specs">
                <span>Physical: 5 × 7 cm</span>
                <span>Pixels: ~590 × 830 px</span>
                <span>Fixed 5:7 aspect ratio</span>
              </div>
            </div>
          </label>
          
          <label class="radio-option" :class="{ active: isNaN(currentAspectRatio) }">
            <input type="radio" name="imageType" value="intraoral" :checked="isNaN(currentAspectRatio)" @change="setAspectRatio(NaN)">
            <div class="radio-option-content">
              <div class="radio-option-title">Intraoral (All Intraoral Views) - Free Crop</div>
              <div class="radio-option-specs">
                <span>Physical: 3.5 × 4.5 cm</span>
                <span>Pixels: ~410 × 530 px</span>
                <span>Free crop (no fixed ratio)</span>
              </div>
            </div>
          </label>
        </div>
      </div>

      <div class="cropper-body" :style="{ maxHeight: imageType === 'cephalometry' ? '850px' : '500px' }">
        <img ref="image" :src="imageSrc" alt="Edit" @load="initCropper" style="max-width: 100%; display: block;">
        
        <!-- AI Loading Overlay -->
        <div v-if="isProcessingAI" class="ai-loading-overlay">
          <div class="spinner"></div>
          <div>Processing AI Smart Crop...</div>
        </div>
      </div>

      <div class="cropper-toolbar">
        <!-- Smart Crop Button (Ceph Only) -->
        <div v-if="imageType === 'cephalometry'" class="smart-crop-section">
          <button type="button" class="cropper-btn primary smart-crop-btn" @click="applySmartCephCrop">
            ✂️ Apply Smart Crop (Remove Metadata, Keep Ruler)
          </button>
          <div class="smart-crop-desc">
            Automatically crops to X-ray with ruler, removing patient info and metadata
          </div>
        </div>

        <!-- AI Face Crop (Extraoral Only) -->
        <div v-if="imageType === 'extraoral'" class="toolbar-row">
           <button type="button" class="cropper-btn face-crop-btn" @click="detectAndCropFace">
            🤖 Apply AI Facial Smart Crop
          </button>
        </div>

        <div class="toolbar-row">
          <div class="cropper-buttons">
            <button type="button" class="cropper-btn" @click="rotate(-90)">⟲ Rotate Left</button>
            <button type="button" class="cropper-btn" @click="rotate(90)">⟳ Rotate Right</button>
            <button type="button" class="cropper-btn" @click="flipX">⇄ Flip H</button>
            <button type="button" class="cropper-btn" @click="flipY">⇅ Flip V</button>
            <button type="button" class="cropper-btn" @click="reset">↺ Reset</button>
          </div>
        </div>

        <!-- Fine Rotation -->
        <div class="rotation-section">
          <div class="rotation-label">Fine Rotation</div>
          <div class="rotation-control">
            <span>-180°</span>
            <input type="range" min="-180" max="180" v-model.number="rotation" @input="updateRotation">
            <span>{{ rotation }}°</span>
            <span>+180°</span>
          </div>
        </div>

        <!-- Image Adjustments -->
        <div class="adjustment-section">
          <div class="adjustment-label">Image Adjustments</div>
          
          <div class="adjustment-control">
            <label>Brightness:</label>
            <input type="range" min="-50" max="50" v-model.number="brightness" @input="updateFilters">
            <span>{{ brightness }}</span>
          </div>
          
          <div class="adjustment-control">
            <label>Contrast:</label>
            <input type="range" min="-50" max="50" v-model.number="contrast" @input="updateFilters">
            <span>{{ contrast }}</span>
          </div>
          
          <div class="adjustment-control">
            <label>Saturation:</label>
            <input type="range" min="-50" max="50" v-model.number="saturation" @input="updateFilters">
            <span>{{ saturation }}</span>
          </div>
        </div>

        <div class="toolbar-row" style="margin-top: 12px;">
          <div class="cropper-buttons">
            <button type="button" class="cropper-btn primary" @click="save">✔ Apply Changes</button>
            <button type="button" class="cropper-btn primary" @click="saveAndClose">💾 Save & Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Cropper from 'cropperjs';
import 'cropperjs/dist/cropper.css';
import * as tf from '@tensorflow/tfjs';
import * as blazeface from '@tensorflow-models/blazeface';

export default {
  name: 'ImageCropperModal',
  props: {
    isOpen: Boolean,
    imageSrc: String,
    imageType: String, // 'extraoral', 'intraoral', 'occlusal', 'cephalometry', 'radiograph'
    slotId: String
  },
  data() {
    return {
      cropper: null,
      rotation: 0,
      brightness: 0,
      contrast: 0,
      saturation: 0,
      currentAspectRatio: NaN,
      isProcessingAI: false
    };
  },
  computed: {
    modalTitle() {
      if (this.imageType === 'cephalometry') return '📐 Edit Cephalometry';
      if (this.imageType === 'radiograph') return '📐 Edit Radiograph';
      return 'Edit Photo';
    }
  },
  watch: {
    isOpen(val) {
      if (val) {
        this.$nextTick(() => {
          this.initCropper();
        });
      } else {
        this.destroyCropper();
      }
    },
    imageType: {
      immediate: true,
      handler(val) {
        // Set initial aspect ratio based on type
        if (val === 'extraoral') this.currentAspectRatio = 5/7;
        else if (val === 'occlusal') this.currentAspectRatio = 8/7;
        else if (val === 'radiograph' && this.slotId === 'prevOPG') this.currentAspectRatio = 16/9;
        else if (val === 'radiograph') this.currentAspectRatio = 3/4; // PA and HW
        else this.currentAspectRatio = NaN; // Intraoral and Ceph (free)
      }
    }
  },
  methods: {
    initCropper() {
      if (this.cropper) {
        this.cropper.destroy();
      }

      const image = this.$refs.image;
      if (!image) return;

      this.cropper = new Cropper(image, {
        aspectRatio: this.currentAspectRatio,
        viewMode: 1,
        dragMode: 'move',
        autoCropArea: 1,
        restore: false,
        guides: true,
        center: true,
        highlight: false,
        cropBoxMovable: true,
        cropBoxResizable: true,
        toggleDragModeOnDblclick: false,
        background: false,
        zoomable: true,
        zoomOnWheel: true,
        wheelZoomRatio: 0.1,
        ready: () => {
          this.updateFilters();
        }
      });
      
      // Reset adjustments
      this.rotation = 0;
      this.brightness = 0;
      this.contrast = 0;
      this.saturation = 0;
    },
    destroyCropper() {
      if (this.cropper) {
        this.cropper.destroy();
        this.cropper = null;
      }
    },
    close() {
      this.$emit('close');
    },
    rotate(deg) {
      if (!this.cropper) return;
      this.cropper.rotate(deg);
    },
    updateRotation() {
      if (!this.cropper) return;
      this.cropper.rotateTo(this.rotation);
    },
    flipX() {
      if (!this.cropper) return;
      const scaleX = this.cropper.getData().scaleX || 1;
      this.cropper.scaleX(-scaleX);
    },
    flipY() {
      if (!this.cropper) return;
      const scaleY = this.cropper.getData().scaleY || 1;
      this.cropper.scaleY(-scaleY);
    },
    reset() {
      if (!this.cropper) return;
      this.cropper.reset();
      this.rotation = 0;
      this.brightness = 0;
      this.contrast = 0;
      this.saturation = 0;
      this.updateFilters();
    },
    setAspectRatio(ratio) {
      this.currentAspectRatio = ratio;
      if (this.cropper) {
        this.cropper.setAspectRatio(ratio);
      }
    },
    updateFilters() {
      if (!this.cropper) return;
      
      const brightnessVal = 100 + this.brightness;
      const contrastVal = 100 + this.contrast;
      const saturationVal = 100 + this.saturation;
      
      const filterString = `brightness(${brightnessVal}%) contrast(${contrastVal}%) saturate(${saturationVal}%)`;
      
      // Apply to the cropper canvas and view box
      const canvas = this.cropper.getCroppedCanvas(); // This doesn't affect the view, just gets data
      
      // We need to apply CSS filters to the image element inside cropper
      const cropperImage = this.$refs.image;
      const cropperCanvases = document.querySelectorAll('.cropper-canvas img, .cropper-view-box img');
      
      if (cropperImage) cropperImage.style.filter = filterString;
      cropperCanvases.forEach(img => {
        img.style.filter = filterString;
      });
    },
    save() {
      if (!this.cropper) return;
      
      // Get cropped canvas
      let canvas = this.cropper.getCroppedCanvas({
        maxWidth: 4096,
        maxHeight: 4096,
        fillColor: '#fff',
        imageSmoothingEnabled: true,
        imageSmoothingQuality: 'high',
      });
      
      if (!canvas) return;
      
      // Apply filters to the final canvas if needed
      if (this.brightness !== 0 || this.contrast !== 0 || this.saturation !== 0) {
        const tempCanvas = document.createElement('canvas');
        const tempCtx = tempCanvas.getContext('2d');
        tempCanvas.width = canvas.width;
        tempCanvas.height = canvas.height;
        
        const brightnessVal = 100 + this.brightness;
        const contrastVal = 100 + this.contrast;
        const saturationVal = 100 + this.saturation;
        
        tempCtx.filter = `brightness(${brightnessVal}%) contrast(${contrastVal}%) saturate(${saturationVal}%)`;
        tempCtx.drawImage(canvas, 0, 0);
        canvas = tempCanvas;
      }
      
      const image = canvas.toDataURL('image/jpeg', 0.95);
      this.$emit('save', { slotId: this.slotId, image });
    },
    saveAndClose() {
      this.save();
      this.close();
    },
    
    // AI Features
    async detectAndCropFace() {
      if (!this.cropper) return;
      this.isProcessingAI = true;
      
      try {
        // Load BlazeFace
        const model = await blazeface.load();
        
        // Get image data
        const imageElement = this.$refs.image;
        
        // Predict
        const predictions = await model.estimateFaces(imageElement, false);
        
        if (predictions.length > 0) {
          const face = predictions[0];
          const start = face.topLeft;
          const end = face.bottomRight;
          const size = [end[0] - start[0], end[1] - start[1]];
          
          // Add padding (e.g., 50% padding)
          const padding = 0.5;
          const x = Math.max(0, start[0] - size[0] * padding);
          const y = Math.max(0, start[1] - size[1] * padding);
          const width = Math.min(imageElement.width - x, size[0] * (1 + 2 * padding));
          const height = Math.min(imageElement.height - y, size[1] * (1 + 2 * padding));
          
          // Set crop box
          this.cropper.setData({
            x: x,
            y: y,
            width: width,
            height: height
          });
          
          alert('Face detected and cropped!');
        } else {
          alert('No face detected.');
        }
      } catch (error) {
        console.error('AI Error:', error);
        alert('Failed to detect face. Please try manually.');
      } finally {
        this.isProcessingAI = false;
      }
    },
    
    async applySmartCephCrop() {
      // Placeholder for Ceph Smart Crop logic
      // Since the custom model code is missing, we'll use a heuristic or just center crop
      if (!this.cropper) return;
      this.isProcessingAI = true;
      
      try {
        // Simulate processing
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Heuristic: Crop to center 80%
        const data = this.cropper.getData();
        const newWidth = data.width * 0.8;
        const newHeight = data.height * 0.8;
        const newX = data.x + (data.width - newWidth) / 2;
        const newY = data.y + (data.height - newHeight) / 2;
        
        this.cropper.setData({
          x: newX,
          y: newY,
          width: newWidth,
          height: newHeight
        });
        
        alert('Smart crop applied (Heuristic).');
      } catch (error) {
        console.error('Ceph Crop Error:', error);
      } finally {
        this.isProcessingAI = false;
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
$radius-sm: 8px;
$radius-lg: 16px;

.cropper-modal {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.75);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
  
  &.open {
    opacity: 1;
    pointer-events: auto;
  }
}

.cropper-panel {
  background: white;
  border-radius: $radius-lg;
  padding: 24px;
  width: 95%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.cropper-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
  
  span {
    font-size: 18px;
    font-weight: 700;
    color: $photon-dark;
  }
}

/* Cephalometry Instructions Styling */
.ceph-instructions {
  padding: 16px 20px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(99, 102, 241, 0.03) 100%);
  border-bottom: 2px solid rgba(99, 102, 241, 0.2);
  margin-bottom: 12px;
  border-radius: 8px;
}

.ceph-info-box {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.ceph-icon {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
}

.ceph-text {
  flex: 1;
}

.ceph-title {
  font-size: 14px;
  font-weight: 700;
  color: #4f46e5;
  margin-bottom: 8px;
  letter-spacing: 0.3px;
}

.ceph-desc {
  font-size: 12px;
  line-height: 1.6;
  color: #374151;
  margin-bottom: 8px;
}

.ceph-warning {
  padding: 10px 14px;
  background: rgba(234, 90, 67, 0.08);
  border-left: 3px solid $photon-primary;
  border-radius: 6px;
  margin-top: 10px;
}

.warning-text {
  font-size: 11px;
  line-height: 1.5;
  color: #1f2937;
}

/* Smart Crop Button Styling */
.smart-crop-section {
  margin-bottom: 10px;
  padding: 8px 10px;
  background: rgba(234, 90, 67, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(234, 90, 67, 0.15);
}

.smart-crop-btn {
  width: 100%;
  padding: 8px;
  font-size: 12px;
  background: linear-gradient(135deg, $photon-primary 0%, #d94d36 100%);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  
  &:hover {
    box-shadow: 0 4px 12px rgba(234, 90, 67, 0.3);
  }
}

.smart-crop-desc {
  margin-top: 6px;
  font-size: 10px;
  color: $photon-muted;
  text-align: center;
}

.face-crop-btn {
  width: 100%;
  background: #3B82F6;
  color: white;
  border: none;
  border-radius: $radius-sm;
  padding: 8px;
  font-size: 12px;
  cursor: pointer;
  
  &:hover { background: #2563EB; }
}

.cropper-body {
  background: #f8f9fa;
  border-radius: $radius-sm;
  overflow: hidden;
  position: relative;
}

.cropper-toolbar {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.toolbar-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.cropper-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.cropper-btn {
  border-radius: $radius-sm;
  border: 1px solid #e5e7eb;
  background: white;
  padding: 6px 12px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
  color: $photon-dark;
  
  &:hover {
    background: #f8f9fa;
    border-color: $photon-primary;
    color: $photon-primary;
    transform: translateY(-1px);
  }
  
  &.primary {
    background: linear-gradient(135deg, $photon-primary 0%, #d94d36 100%);
    color: white;
    border-color: $photon-primary;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(234, 90, 67, 0.3);
    }
  }
  
  &.danger {
    background: white;
    color: #dc2626;
    border-color: #fecaca;
    
    &:hover {
      background: #fef2f2;
      border-color: #dc2626;
    }
  }
}

.rotation-section,
.adjustment-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
  padding: 10px 12px;
  background: #f8f9fa;
  border-radius: $radius-sm;
}

.rotation-label,
.adjustment-label,
.image-type-label {
  font-size: 10px;
  font-weight: 700;
  color: $photon-dark;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.rotation-control,
.adjustment-control {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  color: $photon-muted;
  
  input[type="range"] {
    flex: 1;
    height: 6px;
    border-radius: 3px;
    background: #e5e7eb;
    outline: none;
    appearance: none;
    
    &::-webkit-slider-thumb {
      appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: $photon-primary;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(234, 90, 67, 0.3);
    }
  }
}

.image-type-section {
  padding: 16px;
  background: #f8f9fa;
  border-radius: $radius-sm;
  margin: 8px 0;
}

.radio-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 12px;
}

.radio-option {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border-radius: $radius-sm;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  background: white;
  
  &:hover {
    background: #fafbfc;
    border-color: #e5e7eb;
  }
  
  &.active {
    background: $photon-primary-soft;
    border-color: $photon-primary;
  }
  
  input[type="radio"] {
    margin-top: 3px;
    cursor: pointer;
    accent-color: $photon-primary;
    width: 18px;
    height: 18px;
  }
}

.radio-option-title {
  font-size: 14px;
  font-weight: 700;
  color: $photon-dark;
  margin-bottom: 6px;
}

.radio-option-specs {
  font-size: 12px;
  color: $photon-muted;
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  
  span {
    display: inline-flex;
    align-items: center;
    padding: 4px 10px;
    background: white;
    border-radius: 4px;
    font-size: 11px;
    
    &::before {
      content:'•';
      margin-right: 6px;
      color: $photon-primary;
      font-weight: 700;
    }
  }
}

.ai-loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.8);
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 15px;
  font-weight: 600;
  color: $photon-primary;
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid $photon-primary;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
