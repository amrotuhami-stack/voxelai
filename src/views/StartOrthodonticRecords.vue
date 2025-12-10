<template>
  <div class="ortho-records-page">
    <!-- Top Header -->
    <header class="top-header">
      <div class="header-content">
        <!-- Left: Branding Section -->
        <div class="branding-section">
          <div class="dual-logo-container">
            <img src="https://voxel-assets.s3.amazonaws.com/media/images/V3Di_qR8KLMj.original.png" 
                 alt="Voxel3Di Logo" 
                 crossorigin="anonymous">
            <img src="https://voxel-assets.s3.amazonaws.com/media/images/Logocephalo.original.png" 
                 alt="Cephalo.ai Logo" 
                 crossorigin="anonymous">
          </div>
          <div class="branding-text">
            <div class="branding-title">Orthodontic Records</div>
            <div class="branding-subtitle">AI-Powered Cephalometric Analysis</div>
          </div>
        </div>
        
        <!-- Right: Patient Information Card -->
        <div class="patient-info-card">
          <!-- Patient Name -->
          <div class="info-item">
            <div class="info-icon orange">
              <svg width="12" height="12" viewBox="0 0 16 16" fill="white">
                <path d="M8 8a3 3 0 100-6 3 3 0 000 6zm0 1.5c-2.33 0-7 1.17-7 3.5V14h14v-1c0-2.33-4.67-3.5-7-3.5z"/>
              </svg>
            </div>
            <div class="info-text">
              <div class="info-label">Patient</div>
              <div class="info-value">{{ patient.name || '-' }}</div>
            </div>
          </div>
          
          <div class="divider"></div>
          
          <!-- DOB -->
          <div class="info-item">
            <div class="info-icon indigo">
              <svg width="12" height="12" viewBox="0 0 16 16" fill="white">
                <path d="M14 2h-3V0H9v2H7V0H5v2H2C.89 2 0 2.89 0 4v10a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2zm0 12H2V7h12v7z"/>
              </svg>
            </div>
            <div class="info-text">
              <div class="info-label">DOB</div>
              <div class="info-value">{{ patient.dob || '-' }}</div>
            </div>
          </div>
          
          <div class="divider"></div>
          
          <!-- Case ID -->
          <div class="info-item">
            <div class="info-icon emerald">
              <svg width="12" height="12" viewBox="0 0 16 16" fill="white">
                <path d="M9 0H4a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V5l-5-5zm4 14H4V2h4v4h5v8z"/>
              </svg>
            </div>
            <div class="info-text">
              <div class="info-label">Case ID</div>
              <div class="info-value">{{ patient.caseId || '-' }}</div>
            </div>
          </div>
          
          <div class="divider"></div>
          
          <!-- Gender -->
          <div class="info-item">
            <div class="info-icon violet">
              <svg width="12" height="12" viewBox="0 0 16 16" fill="white">
                <path d="M8 1a3.5 3.5 0 100 7 3.5 3.5 0 000-7zM12.5 3h2v2h-2v2h-2V5h-1.5a4.5 4.5 0 11-3 1.5V8.5h2v2h-2v3.5H6v-3.5H4v-2h2V6.5A4.5 4.5 0 0112.5 3z"/>
              </svg>
            </div>
            <div class="info-text">
              <div class="info-label">Gender</div>
              <div class="info-value">{{ patient.gender || '-' }}</div>
            </div>
          </div>
          
          <div class="divider"></div>
          
          <!-- Race -->
          <div class="info-item">
            <div class="info-icon amber">
              <svg width="12" height="12" viewBox="0 0 16 16" fill="white">
                <path d="M11 1a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V3a2 2 0 012-2h6zM5 0a3 3 0 00-3 3v10a3 3 0 003 3h6a3 3 0 003-3V3a3 3 0 00-3-3H5zm3 12a1 1 0 100-2 1 1 0 000 2z"/>
              </svg>
            </div>
            <div class="info-text">
              <div class="info-label">Race</div>
              <div class="info-value">{{ patient.race || '-' }}</div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <div class="main-container">
      <!-- LEFT PANEL -->
      <div class="left-panel">
        <!-- Workflow Steps -->
        <div class="workflow-steps">
          <!-- Step 1 -->
          <button class="step-btn" :class="{ active: currentStep === 1 }" @click="currentStep = 1">
            <div class="step-label">STEP 1</div>
            <div class="step-title">Case Photos</div>
          </button>
          
          <!-- Arrow 1 -->
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" class="step-arrow" :class="{ active: currentStep >= 1 }">
            <path d="M7 4L13 10L7 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          
          <!-- Step 2 -->
          <button class="step-btn" :class="{ active: currentStep === 2 }" @click="currentStep = 2">
            <div class="step-label">STEP 2</div>
            <div class="step-title">Cephalo.ai<br>Digitisation</div>
          </button>
          
          <!-- Arrow 2 -->
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" class="step-arrow" :class="{ active: currentStep >= 2 }">
            <path d="M7 4L13 10L7 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          
          <!-- Step 3 -->
          <button class="step-btn" :class="{ active: currentStep === 3 }" @click="currentStep = 3">
            <div class="step-label">STEP 3</div>
            <div class="step-title">Analysis &<br>Reports</div>
          </button>
          
          <!-- Arrow 3 -->
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" class="step-arrow" :class="{ active: currentStep >= 3 }">
            <path d="M7 4L13 10L7 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          
          <!-- Step 4 -->
          <button class="step-btn" :class="{ active: currentStep === 4 }" @click="currentStep = 4">
            <div class="step-label">STEP 4</div>
            <div class="step-title">Full Case<br>Report</div>
          </button>
        </div>
        
        <!-- Upload Section -->
        <div class="upload-section">
          <!-- Branding Logo -->
          <div class="branding">
            <div class="cephalo-logo">
              <img src="https://voxel-assets.s3.amazonaws.com/media/images/Logocephalo.original.png" 
                   alt="Cephalo.ai Logo"
                   crossorigin="anonymous">
            </div>
          </div>
          
          <!-- Upload Button -->
          <label class="upload-button">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 0a1 1 0 011 1v8h8a1 1 0 110 2h-8v8a1 1 0 11-2 0v-8H1a1 1 0 110-2h8V1a1 1 0 011-1z"/>
            </svg>
            <div class="upload-text">
              <div class="upload-main-text">Start Cephalo.Ai</div>
              <div class="upload-sub-text">Upload Patient's Lateral Cephalometry</div>
            </div>
            <input type="file" accept="image/*" @change="handleMainUpload" hidden>
          </label>
          
          <!-- Cephalometry Preview -->
          <div v-if="cephalometryImage" class="ceph-preview-container">
            <div class="preview-title">Uploaded Cephalometry</div>
            <div class="ceph-preview">
              <img :src="cephalometryImage" alt="Cephalometry Preview" />
            </div>
            <button @click="editCephalometry" class="edit-ceph-btn">
              ✏️ Edit Cephalometry
            </button>
            <button @click="startAnalysis" class="start-analysis-btn">
              🚀 Start Cephalo.ai Analysis
            </button>
          </div>
          
          <!-- Cephalometry Auto-Crop Option -->
          <div class="ceph-auto-crop-option">
            <label class="auto-crop-label">
              <input type="checkbox" v-model="smartCropEnabled">
              <div class="auto-crop-text">
                <div class="auto-crop-title">Smart Cephalometry Crop</div>
                <div class="auto-crop-desc">Automatically crops to X-ray with ruler only, removing metadata</div>
              </div>
            </label>
          </div>
        </div>
      </div>
      
      <!-- RIGHT PANEL -->
      <div class="right-panel">
        <!-- EXTRAORAL VIEWS -->
        <div class="section-header">
          <div class="section-title">EXTRAORAL VIEWS</div>
          <div class="section-subtitle">Order: Frontal rest • Profile smile • Right profile • Left 3/4 • Submento-vertex • Profile Smiling</div>
        </div>
        
        <div class="photo-grid extraoral-grid">
          <PhotoSlot 
            v-for="(slot, index) in extraoralSlots" 
            :key="slot.id"
            :slot-data="slot"
            @upload="handlePhotoUpload"
            @edit="handlePhotoEdit"
          />
        </div>

        <!-- INTRAORAL & OCCLUSAL VIEWS -->
        <div class="section-header">
          <div class="section-title">INTRAORAL & OCCLUSAL VIEWS</div>
          <div class="section-subtitle">Order: Right buccal • Frontal occlusion • Left buccal • Maxillary occlusl • Smile close-up • Mandibular occlusal</div>
        </div>
        
        <div class="photo-grid intraoral-grid">
          <PhotoSlot 
            v-for="(slot, index) in intraoralSlots" 
            :key="slot.id"
            :slot-data="slot"
            @upload="handlePhotoUpload"
            @edit="handlePhotoEdit"
          />
        </div>

        <!-- RADIOGRAPHS SECTION -->
        <div class="section-header" style="margin-top: 40px;">
          <div class="section-title">RADIOGRAPHS</div>
          <div class="section-subtitle">Upload diagnostic radiographic images</div>
        </div>
        
        <div class="photo-grid radiographs-grid">
          <PhotoSlot 
            v-for="(slot, index) in radiographSlots" 
            :key="slot.id"
            :slot-data="slot"
            @upload="handlePhotoUpload"
            @edit="handlePhotoEdit"
          />
        </div>

        <!-- Bottom Actions -->
        <div class="bottom-actions">
          <button type="button" class="btn btn-outline" @click="resetForm">Reset Form</button>
          <button type="button" class="btn btn-primary" @click="exportPDF">Export PDF</button>
        </div>
      </div>
    </div>

    <!-- Image Cropper Modal -->
    <ImageCropperModal
      :is-open="cropperModal.isOpen"
      :image-src="cropperModal.imageSrc"
      :image-type="cropperModal.imageType"
      :slot-id="cropperModal.slotId"
      @close="closeCropperModal"
      @save="handleCropperSave"
    />

    <!-- AI Features Panel -->
    <AIFeaturesPanel @update:settings="handleAISettingsUpdate" />
  </div>
</template>

<script>
import PhotoSlot from '@/components/orthodontic/PhotoSlot.vue';
import ImageCropperModal from '@/components/orthodontic/ImageCropperModal.vue';
import AIFeaturesPanel from '@/components/orthodontic/AIFeaturesPanel.vue';
import html2canvas from 'html2canvas';
import { jsPDF } from 'jspdf';

export default {
  name: 'StartOrthodonticRecords',
  components: {
    PhotoSlot,
    ImageCropperModal,
    AIFeaturesPanel
  },
  data() {
    return {
      currentStep: 1,
      smartCropEnabled: true,
      aiSettings: {
        colorCorrection: true,
        autoEnhance: true,
        intraoralCrop: true,
        smartFlip: false,
        faceDetection: false,
        backgroundRemoval: false,
        blurDetection: true,
        noiseReduction: false
      },
      patient: {
        name: 'John Doe',
        dob: '1990-01-01',
        caseId: 'CASE-123',
        gender: 'Male',
        race: 'Caucasian'
      },
      cephalometryImage: null,
      cropperModal: {
        isOpen: false,
        imageSrc: '',
        imageType: 'intraoral',
        slotId: ''
      },
      extraoralSlots: [
        { id: 'prev1', title: 'Frontal – Rest', filename: '', image: null, type: 'extraoral', aspectRatio: '5/7' },
        { id: 'prev2', title: 'Frontal – Smile', filename: '', image: null, type: 'extraoral', aspectRatio: '5/7' },
        { id: 'prev3', title: 'Profile – Right', filename: '', image: null, type: 'extraoral', aspectRatio: '5/7' },
        { id: 'prev4', title: '3/4 – Left', filename: '', image: null, type: 'extraoral', aspectRatio: '5/7' },
        { id: 'prev5', title: 'Submento-vertex', filename: '', image: null, type: 'extraoral', aspectRatio: '5/7' },
        { id: 'prev6', title: 'Profile Smiling', filename: '', image: null, type: 'extraoral', aspectRatio: '5/7' }
      ],
      intraoralSlots: [
        { id: 'prev7', title: 'Right Buccal', filename: '', image: null, type: 'intraoral' },
        { id: 'prev8', title: 'Frontal Occlusion', filename: '', image: null, type: 'intraoral' },
        { id: 'prev9', title: 'Left Buccal', filename: '', image: null, type: 'intraoral' },
        { id: 'prev10', title: 'Maxillary Occlusal', filename: '', image: null, type: 'occlusal', aspectRatio: '8/7' },
        { id: 'prev11', title: 'Smile – Close Up', filename: '', image: null, type: 'intraoral' },
        { id: 'prev12', title: 'Mandibular Occlusal', filename: '', image: null, type: 'occlusal', aspectRatio: '8/7' },
        { id: 'prev13', title: 'Right Buccal', filename: '', image: null, type: 'intraoral' },
        { id: 'prev14', title: 'Frontal Occlusion', filename: '', image: null, type: 'intraoral' },
        { id: 'prev15', title: 'Left Buccal', filename: '', image: null, type: 'intraoral' }
      ],
      radiographSlots: [
        { id: 'prevOPG', title: 'OPG (Orthopantomogram)', filename: '', image: null, type: 'radiograph', aspectRatio: '16/9' },
        { id: 'prevPA', title: 'Posteroanterior Cephalometry', filename: '', image: null, type: 'radiograph', aspectRatio: '3/4' },
        { id: 'prevHW', title: 'Hand Wrist', filename: '', image: null, type: 'radiograph', aspectRatio: '3/4' }
      ]
    };
  },
  methods: {
    handleAISettingsUpdate(settings) {
      this.aiSettings = settings;
    },
    handleMainUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      const reader = new FileReader();
      reader.onload = (e) => {
        this.cephalometryImage = e.target.result;
        // Auto-open editor for cephalometry
        this.editCephalometry();
      };
      reader.readAsDataURL(file);
      
      event.target.value = '';
    },
    editCephalometry() {
      if (!this.cephalometryImage) return;
      
      this.cropperModal = {
        isOpen: true,
        imageSrc: this.cephalometryImage,
        imageType: 'cephalometry',
        slotId: 'ceph'
      };
    },
    startAnalysis() {
      alert('Starting Cephalo.ai Analysis...');
    },
    handlePhotoUpload({ slotId, file }) {
      const reader = new FileReader();
      reader.onload = async (e) => {
        let imageSrc = e.target.result;
        
        // Process with AI if settings enabled
        imageSrc = await this.processImageWithAI(imageSrc, slotId);
        
        this.updateSlotImage(slotId, imageSrc, file.name);
      };
      reader.readAsDataURL(file);
    },
    async processImageWithAI(imageSrc, slotId) {
      const slot = this.findSlot(slotId);
      if (!slot) return imageSrc;
      
      const isIntraoral = slot.type === 'intraoral' || slot.type === 'occlusal';
      
      // Intraoral AI Features
      if (isIntraoral) {
        // Smart Crop (Remove black borders)
        if (this.aiSettings.intraoralCrop) {
          try {
            imageSrc = await this.smartIntraoralCrop(imageSrc);
          } catch (e) {
            console.error('Smart Crop failed:', e);
          }
        }
        
        // Smart Flip (Horizontal Mirror)
        if (this.aiSettings.smartFlip) {
          try {
            imageSrc = await this.smartIntraoralFlip(imageSrc);
          } catch (e) {
            console.error('Smart Flip failed:', e);
          }
        }
      }
      
      return imageSrc;
    },
    smartIntraoralCrop(imageSrc) {
      return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => {
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          canvas.width = img.width;
          canvas.height = img.height;
          ctx.drawImage(img, 0, 0);
          
          const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
          const data = imageData.data;
          
          let minX = canvas.width, minY = canvas.height, maxX = 0, maxY = 0;
          const threshold = 30; // Black threshold
          
          for (let y = 0; y < canvas.height; y++) {
            for (let x = 0; x < canvas.width; x++) {
              const i = (y * canvas.width + x) * 4;
              const r = data[i];
              const g = data[i+1];
              const b = data[i+2];
              
              if (r > threshold || g > threshold || b > threshold) {
                if (x < minX) minX = x;
                if (x > maxX) maxX = x;
                if (y < minY) minY = y;
                if (y > maxY) maxY = y;
              }
            }
          }
          
          // Add padding
          const padding = 20;
          minX = Math.max(0, minX - padding);
          minY = Math.max(0, minY - padding);
          maxX = Math.min(canvas.width, maxX + padding);
          maxY = Math.min(canvas.height, maxY + padding);
          
          const width = maxX - minX;
          const height = maxY - minY;
          
          if (width <= 0 || height <= 0) {
            resolve(imageSrc); // Return original if crop failed
            return;
          }
          
          const cropCanvas = document.createElement('canvas');
          cropCanvas.width = width;
          cropCanvas.height = height;
          const cropCtx = cropCanvas.getContext('2d');
          cropCtx.drawImage(canvas, minX, minY, width, height, 0, 0, width, height);
          
          resolve(cropCanvas.toDataURL('image/jpeg', 0.95));
        };
        img.src = imageSrc;
      });
    },
    smartIntraoralFlip(imageSrc) {
      return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => {
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          canvas.width = img.width;
          canvas.height = img.height;
          
          // Flip horizontally
          ctx.translate(canvas.width, 0);
          ctx.scale(-1, 1);
          ctx.drawImage(img, 0, 0);
          
          resolve(canvas.toDataURL('image/jpeg', 0.95));
        };
        img.src = imageSrc;
      });
    },
    handlePhotoEdit({ slotId }) {
      const slot = this.findSlot(slotId);
      if (!slot || !slot.image) return;
      
      this.cropperModal = {
        isOpen: true,
        imageSrc: slot.image,
        imageType: slot.type,
        slotId: slotId
      };
    },
    handleCropperSave({ slotId, image }) {
      if (slotId === 'ceph') {
        this.cephalometryImage = image;
      } else {
        this.updateSlotImage(slotId, image);
      }
    },
    closeCropperModal() {
      this.cropperModal.isOpen = false;
    },
    findSlot(slotId) {
      return [...this.extraoralSlots, ...this.intraoralSlots, ...this.radiographSlots].find(s => s.id === slotId);
    },
    updateSlotImage(slotId, image, filename = null) {
      const slot = this.findSlot(slotId);
      if (slot) {
        slot.image = image;
        if (filename) slot.filename = filename;
      }
    },
    resetForm() {
      if (confirm('Are you sure you want to reset the form? All images will be cleared.')) {
        window.location.reload();
      }
    },
    async exportPDF() {
      // PDF export logic placeholder
      alert('PDF Export functionality coming soon!');
    }
  }
};
</script>

<style lang="scss">
/* Global Variables matching the HTML :root */
$photon-primary: #EA5A43;
$photon-primary-soft: #FFE4DE;
$photon-dark: #222222;
$photon-muted: #777777;
$photon-border: #e0e0e0;
$photon-bg: #F5F6FA;
$shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
$shadow-md: 0 4px 12px rgba(0,0,0,0.08);
$shadow-lg: 0 8px 24px rgba(0,0,0,0.12);
$radius-sm: 8px;
$radius-md: 12px;
$radius-lg: 16px;

.ortho-records-page {
  background: linear-gradient(135deg, #f5f7fa 0%, #e9ecf1 100%);
  color: $photon-dark;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

/* Top Header */
.top-header {
  width: 100%;
  background: white;
  border-bottom: 1px solid #e8eaed;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 100px;
  display: flex;
  align-items: center;
}

.header-content {
  max-width: 1400px;
  width: 100%;
  margin: 0 auto;
  padding: 0 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}

.branding-section {
  display: flex;
  align-items: center;
  gap: 16px;
}

.dual-logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
  
  img {
    height: 45px;
    width: auto;
    object-fit: contain;
  }
}

.branding-text {
  border-left: 2px solid #e8eaed;
  padding-left: 16px;
  
  .branding-title {
    font-size: 16px;
    font-weight: 700;
    color: $photon-dark;
    line-height: 1.2;
    margin-bottom: 2px;
  }
  
  .branding-subtitle {
    font-size: 11px;
    color: $photon-muted;
    font-weight: 500;
  }
}

.patient-info-card {
  flex: 1;
  max-width: 700px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border: 1px solid #e8eaed;
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.info-icon {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  
  &.orange { background: linear-gradient(135deg, $photon-primary 0%, #d94d36 100%); box-shadow: 0 2px 4px rgba(234, 90, 67, 0.2); }
  &.indigo { background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); box-shadow: 0 2px 4px rgba(99, 102, 241, 0.2); }
  &.emerald { background: linear-gradient(135deg, #10b981 0%, #059669 100%); box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2); }
  &.violet { background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); box-shadow: 0 2px 4px rgba(139, 92, 246, 0.2); }
  &.amber { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); box-shadow: 0 2px 4px rgba(245, 158, 11, 0.2); }
}

.info-text {
  .info-label {
    font-size: 8px;
    font-weight: 600;
    color: $photon-muted;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }
  
  .info-value {
    font-size: 11px;
    font-weight: 600;
    color: $photon-dark;
  }
}

.divider {
  width: 1px;
  height: 20px;
  background: #dee2e6;
}

/* Main Container */
.main-container {
  display: flex;
  min-height: calc(100vh - 100px);
  padding-top: 100px;
}

/* Left Panel */
.left-panel {
  width: 520px;
  background: white;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: calc(100vh - 100px);
  left: 0;
  top: 100px;
  box-shadow: $shadow-md;
  z-index: 100;
  padding: 20px;
  overflow-y: auto;
}

.workflow-steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 12px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.step-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 8px;
  background: white;
  color: $photon-dark;
  border: 2px solid #dee2e6;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  
  &.active {
    background: linear-gradient(135deg, $photon-primary 0%, #d94d36 100%);
    color: white;
    border: none;
    box-shadow: 0 4px 12px rgba(234, 90, 67, 0.3);
    
    .step-label { opacity: 0.9; }
  }
  
  .step-label {
    font-size: 10px;
    font-weight: 600;
    opacity: 0.6;
    margin-bottom: 4px;
  }
  
  .step-title {
    font-size: 11px;
    font-weight: 700;
    line-height: 1.2;
    text-align: center;
  }
}

.step-arrow {
  flex-shrink: 0;
  color: #dee2e6;
  
  &.active {
    color: $photon-primary;
  }
}

/* Upload Section */
.upload-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  gap: 32px;
}

.cephalo-logo {
  width: 100%;
  max-width: 120px;
  margin-bottom: 20px;
  
  img {
    width: 100%;
    height: auto;
    object-fit: contain;
  }
}

.upload-button {
  background: linear-gradient(135deg, $photon-primary 0%, #d94d36 100%);
  color: white;
  border: none;
  border-radius: $radius-md;
  padding: 16px 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  box-shadow: 0 6px 20px rgba(234, 90, 67, 0.35);
  transition: all 0.3s;
  width: 100%;
  max-width: 320px;
  
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(234, 90, 67, 0.45);
  }
}

.upload-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  
  .upload-main-text {
    font-size: 16px;
    font-weight: 700;
  }
  
  .upload-sub-text {
    font-size: 12px;
    font-weight: 500;
    opacity: 0.95;
  }
}

.ceph-preview-container {
  width: 100%;
  margin-top: 20px;
}

.preview-title {
  font-size: 13px;
  font-weight: 600;
  color: $photon-dark;
  margin-bottom: 12px;
}

.ceph-preview {
  width: 100%;
  aspect-ratio: 4/3;
  background: #f8f9fa;
  border-radius: 12px;
  border: 2px dashed #dee2e6;
  overflow: hidden;
  margin-bottom: 12px;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }
}

.edit-ceph-btn {
  width: 100%;
  padding: 10px;
  background: linear-gradient(135deg, $photon-primary 0%, #d94d36 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 12px;
}

.start-analysis-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
}

.ceph-auto-crop-option {
  margin-top: 16px;
  padding: 12px 20px;
  background: rgba(234, 90, 67, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(234, 90, 67, 0.15);
  width: 100%;
}

.auto-crop-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  
  input {
    width: 18px;
    height: 18px;
    accent-color: $photon-primary;
  }
}

.auto-crop-text {
  flex: 1;
  
  .auto-crop-title {
    font-size: 13px;
    font-weight: 600;
    color: $photon-dark;
    margin-bottom: 2px;
  }
  
  .auto-crop-desc {
    font-size: 11px;
    color: $photon-muted;
    line-height: 1.4;
  }
}

/* Right Panel */
.right-panel {
  width: calc(100% - 520px);
  margin-left: 520px;
  background: transparent;
  padding: 32px;
  min-height: 100vh;
}

.section-header {
  margin-bottom: 24px;
  background: white;
  padding: 20px 24px;
  border-radius: $radius-lg;
  box-shadow: $shadow-sm;
  border-left: 4px solid $photon-primary;
  
  .section-title {
    font-size: 14px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: $photon-primary;
    margin-bottom: 6px;
  }
  
  .section-subtitle {
    font-size: 13px;
    color: $photon-muted;
    line-height: 1.5;
  }
}

.photo-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.bottom-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 32px;
  background: white;
  border-top: 1px solid #e5e7eb;
  position: sticky;
  bottom: 0;
  box-shadow: 0 -4px 12px rgba(0,0,0,0.05);
  z-index: 50;
  margin: 0 -32px -32px -32px;
}

.btn {
  border-radius: $radius-md;
  border: none;
  padding: 12px 24px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  transition: all 0.2s ease;
  
  &.btn-outline {
    background: white;
    color: $photon-primary;
    border: 2px solid $photon-primary-soft;
    
    &:hover {
      background: $photon-primary-soft;
      border-color: $photon-primary;
    }
  }
  
  &.btn-primary {
    background: linear-gradient(135deg, $photon-primary 0%, #d94d36 100%);
    color: white;
    box-shadow: 0 4px 12px rgba(234, 90, 67, 0.3);
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(234, 90, 67, 0.4);
    }
  }
}

@media (max-width: 1400px) {
  .left-panel { width: 480px; }
  .right-panel { width: calc(100% - 480px); margin-left: 480px; }
}

@media (max-width: 1200px) {
  .main-container { flex-direction: column; }
  .left-panel {
    width: 100%;
    position: relative;
    height: auto;
    border-right: none;
    border-bottom: 1px solid #e5e7eb;
    top: 0;
    left: 0;
  }
  .right-panel {
    width: 100%;
    margin-left: 0;
    padding-top: 32px;
  }
}
</style>
