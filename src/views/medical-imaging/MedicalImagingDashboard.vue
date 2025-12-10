<template>
  <div class="medical-imaging-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1>Medical Imaging</h1>
        <p>View and manage DICOM studies from the PACS server</p>
      </div>
      <div class="header-actions">
        <button @click="showUploadModal = true" class="btn-upload">
          <span class="icon">📤</span>
          Upload DICOM
        </button>
        <button @click="refreshStudies" class="btn-refresh" :disabled="loading">
          <span class="icon">🔄</span>
          Refresh
        </button>
      </div>
    </div>

    <!-- Search and Filters -->
    <div class="search-section">
      <div class="search-bar">
        <input
          v-model="searchQuery.PatientName"
          type="text"
          placeholder="Search by patient name..."
          @input="debouncedSearch"
          class="search-input"
        />
        <input
          v-model="searchQuery.PatientID"
          type="text"
          placeholder="Patient ID..."
          @input="debouncedSearch"
          class="search-input"
        />
        <input
          v-model="searchQuery.StudyDate"
          type="date"
          @change="searchStudies"
          class="search-input"
        />
      </div>
    </div>

    <!-- Studies List -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading studies...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <div class="error-icon">⚠️</div>
      <h3>Error Loading Studies</h3>
      <p>{{ error }}</p>
      <button @click="refreshStudies" class="retry-btn">Retry</button>
    </div>

    <div v-else-if="studies.length === 0" class="empty-state">
      <div class="empty-icon">📁</div>
      <h3>No Studies Found</h3>
      <p>Upload DICOM files to get started</p>
      <button @click="showUploadModal = true" class="btn-upload-large">
        Upload DICOM Files
      </button>
    </div>

    <div v-else class="studies-grid">
      <div
        v-for="study in studies"
        :key="study.studyUID"
        class="study-card"
        @click="openViewer(study.studyUID)"
      >
        <div class="study-thumbnail">
          <img v-if="study.thumbnail" :src="study.thumbnail" alt="Study thumbnail" />
          <div v-else class="thumbnail-placeholder">
            <span class="placeholder-icon">🏥</span>
          </div>
        </div>
        <div class="study-info">
          <h4 class="patient-name">{{ study.patientName || 'Unknown Patient' }}</h4>
          <p class="patient-id">ID: {{ study.patientID || 'N/A' }}</p>
          <p class="study-description">{{ study.studyDescription || 'No description' }}</p>
          <div class="study-meta">
            <span class="meta-item">
              <span class="meta-icon">📅</span>
              {{ formatDate(study.studyDate) }}
            </span>
            <span class="meta-item">
              <span class="meta-icon">📊</span>
              {{ study.numberOfSeries || 0 }} series
            </span>
            <span class="meta-item">
              <span class="meta-icon">🖼️</span>
              {{ study.numberOfInstances || 0 }} images
            </span>
          </div>
        </div>
        <div class="study-actions">
          <button @click.stop="openViewer(study.studyUID)" class="btn-view">
            <i class="fas fa-eye"></i> View
          </button>
          <button 
            @click.stop="triggerSegmentation(study)" 
            class="btn-slicer" 
            title="AI-powered dental segmentation: Maxilla, Mandible, Teeth, Mandibular Canal"
          >
            🧠 Segment
          </button>
          <button 
            @click.stop="generatePanoramic(study)" 
            class="btn-panoramic" 
            title="Generate panoramic CPR reconstruction"
          >
            📊 Panoramic
          </button>
          <button 
            @click.stop="generate3DModel(study)" 
            class="btn-model" 
            title="Generate 3D model (STL)"
          >
            🧊 3D Model
          </button>
          <button @click.stop="deleteStudy(study.studyUID)" class="btn-delete">
            <i class="fas fa-trash"></i> Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Upload Modal -->
    <div v-if="showUploadModal" class="modal-overlay" @click="closeUploadModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Upload DICOM Files</h3>
          <button @click="closeUploadModal" class="close-btn">×</button>
        </div>
        <div class="modal-body">
          <DicomUpload @upload-complete="onUploadComplete" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { queryStudies, deleteStudy as deleteStudyAPI } from '@/services/pacsService';
import DicomUpload from '@/components/medical-imaging/DicomUpload.vue';

export default {
  name: 'MedicalImagingDashboard',
  components: {
    DicomUpload
  },
  data() {
    return {
      studies: [],
      loading: false,
      error: null,
      showUploadModal: false,
      searchQuery: {
        PatientName: '',
        PatientID: '',
        StudyDate: ''
      },
      searchTimeout: null
    };
  },
  mounted() {
    this.loadStudies();
  },
  methods: {
    async loadStudies() {
      this.loading = true;
      this.error = null;

      try {
        const results = await queryStudies(this.searchQuery);
        this.studies = this.parseStudies(results);
      } catch (err) {
        console.error('Error loading studies:', err);
        this.error = err.message || 'Failed to load studies from PACS server';
      } finally {
        this.loading = false;
      }
    },
    parseStudies(dicomData) {
      console.log('Raw DICOM data from Orthanc:', dicomData);
      const studies = dicomData.map(study => {
        const studyUID = this.getDicomValue(study, '0020000D');
        console.log('Parsed studyUID:', studyUID, 'from study:', study);
        return {
          studyUID: studyUID,
          patientName: this.getDicomValue(study, '00100010'),
          patientID: this.getDicomValue(study, '00100020'),
          studyDate: this.getDicomValue(study, '00080020'),
          studyDescription: this.getDicomValue(study, '00081030'),
          accessionNumber: this.getDicomValue(study, '00080050'),
          numberOfSeries: this.getDicomValue(study, '00201206'),
          numberOfInstances: this.getDicomValue(study, '00201208'),
          thumbnail: null // Could be populated with WADO-RS thumbnail
        };
      });
      console.log('Final parsed studies:', studies);
      return studies;
    },
    getDicomValue(obj, tag) {
      const element = obj[tag];
      if (!element) return null;
      
      if (element.Value && element.Value.length > 0) {
        const value = element.Value[0];
        return typeof value === 'object' ? value.Alphabetic : value;
      }
      
      return null;
    },
    formatDate(dateStr) {
      if (!dateStr) return 'N/A';
      // DICOM date format: YYYYMMDD
      const year = dateStr.substring(0, 4);
      const month = dateStr.substring(4, 6);
      const day = dateStr.substring(6, 8);
      return `${year}-${month}-${day}`;
    },
    debouncedSearch() {
      clearTimeout(this.searchTimeout);
      this.searchTimeout = setTimeout(() => {
        this.searchStudies();
      }, 500);
    },
    searchStudies() {
      this.loadStudies();
    },
    
    async triggerSegmentation(study) {
      try {
        this.loading = true;
        
        const backendUrl = 'http://127.0.0.1:8001';
        const response = await fetch(`${backendUrl}/process/slicer/segment`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            studyInstanceUID: study.studyUID,
            seriesInstanceUID: study.studyUID
          })
        });
        
        if (!response.ok) {
          throw new Error(await response.text());
        }
        
        const result = await response.json();
        alert('Segmentation completed! Reload Voxel3di to see overlays.');
        console.log('Segmentation result:', result);
        
      } catch (error) {
        console.error('Segmentation error:', error);
        alert('Failed: ' + error.message);
      } finally {
        this.loading = false;
      }
    },
    refreshStudies() {
      this.loadStudies();
    },
    openViewer(studyUID) {
      // Open Voxel3di directly in a new window
      const voxel3diUrl = `http://127.0.0.1:8042/viewer?StudyInstanceUIDs=${studyUID}`;
      window.open(voxel3diUrl, '_blank');
    },
    
    async triggerSegmentation(study) {
      try {
        this.loading = true;
        
        this.$bvToast.toast('Sending CBCT to 3D Slicer for segmentation...', {
          title: '3D Slicer Processing',
          variant: 'info',
          solid: true,
          autoHideDelay: 3000
        });
        
        const backendUrl = process.env.VUE_APP_BACKEND_URL || 'http://127.0.0.1:8001';
        const response = await fetch(`${backendUrl}/process/slicer/segment`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            studyInstanceUID: study.studyUID,
            seriesInstanceUID: study.studyUID // Use first series
          })
        });
        
        if (!response.ok) {
          const error = await response.text();
          throw new Error(error);
        }
        
        const result = await response.json();
        
        this.$bvToast.toast('Segmentation completed! Reload Voxel3di to see overlays.', {
          title: 'Success',
          variant: 'success',
          solid: true,
          autoHideDelay: 5000
        });
        
        console.log('Segmentation result:', result);
        
      } catch (error) {
        console.error('Segmentation error:', error);
        this.$bvToast.toast(error.message || 'Failed to process segmentation', {
          title: 'Error',
          variant: 'danger',
          solid: true,
          autoHideDelay: 5000
        });
      } finally {
        this.loading = false;
      }
    },
    
    async generate3DModel(study) {
      try {
        this.loading = true;
        
        this.$bvToast.toast('Generating 3D model from CBCT...', {
          title: '3D Slicer Processing',
          variant: 'info',
          solid: true,
          autoHideDelay: 3000
        });
        
        const backendUrl = process.env.VUE_APP_BACKEND_URL || 'http://127.0.0.1:8001';
        const response = await fetch(`${backendUrl}/process/slicer/model`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            studyInstanceUID: study.studyUID,
            seriesInstanceUID: study.studyUID
          })
        });
        
        if (!response.ok) {
          const error = await response.text();
          throw new Error(error);
        }
        
        const result = await response.json();
        
        this.$bvToast.toast('3D model generated successfully!', {
          title: 'Success',
          variant: 'success',
          solid: true,
          autoHideDelay: 5000
        });
        
        console.log('3D model result:', result);
        
      } catch (error) {
        console.error('3D model error:', error);
        this.$bvToast.toast(error.message || 'Failed to generate 3D model', {
          title: 'Error',
          variant: 'danger',
          solid: true,
          autoHideDelay: 5000
        });
      } finally {
        this.loading = false;
      }
    },
    
    async generatePanoramic(study) {
      try {
        this.loading = true;
        
        this.$bvToast.toast('Generating panoramic reconstruction...', {
          title: '3D Slicer Processing',
          variant: 'info',
          solid: true,
          autoHideDelay: 3000
        });
        
        const backendUrl = process.env.VUE_APP_BACKEND_URL || 'http://127.0.0.1:8001';
        const response = await fetch(`${backendUrl}/process/slicer/panoramic`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            studyInstanceUID: study.studyUID,
            seriesInstanceUID: study.studyUID
          })
        });
        
        if (!response.ok) {
          const error = await response.text();
          throw new Error(error);
        }
        
        const result = await response.json();
        
        this.$bvToast.toast('Panoramic reconstruction completed! Reload studies to see new series.', {
          title: 'Success',
          variant: 'success',
          solid: true,
          autoHideDelay: 5000
        });
        
        console.log('Panoramic result:', result);
        
        // Refresh studies to show new panoramic series
        await this.loadStudies();
        
      } catch (error) {
        console.error('Panoramic error:', error);
        this.$bvToast.toast('Panoramic reconstruction failed. Please try again.', {
          title: 'Error',
          variant: 'danger',
          solid: true,
          autoHideDelay: 5000
        });
      } finally {
        this.loading = false;
      }
    },
    
    async generate3DModel(study) {
      try {
        this.loading = true;
        alert('Generating 3D model...\nThis may take 2-4 minutes.');
        
        const backendUrl = 'http://127.0.0.1:8001';
        const response = await fetch(`${backendUrl}/process/slicer/model`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            studyInstanceUID: study.studyUID,
            seriesInstanceUID: study.studyUID
          })
        });
        
        if (!response.ok) {
          throw new Error(await response.text());
        }
        
        const result = await response.json();
        alert(`3D model generated!\nModel: ${result.data.model_url}`);
        
      } catch (error) {
        console.error('3D model error:', error);
        alert('Failed: ' + error.message);
      } finally {
        this.loading = false;
      }
    },
    
    async deleteStudy(studyUID) {
      if (!confirm('Are you sure you want to delete this study?')) {
        return;
      }

      try {
        await deleteStudyAPI(studyUID);
        this.studies = this.studies.filter(s => s.studyUID !== studyUID);
      } catch (err) {
        alert('Failed to delete study: ' + err.message);
      }
    },
    closeUploadModal() {
      this.showUploadModal = false;
    },
    onUploadComplete() {
      this.showUploadModal = false;
      this.refreshStudies();
    }
  }
};
</script>

<style lang="scss" scoped>
.medical-imaging-dashboard {
  padding: 32px;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;

  .header-content {
    h1 {
      font-size: 32px;
      font-weight: 700;
      color: #222;
      margin-bottom: 8px;
    }

    p {
      font-size: 14px;
      color: #666;
    }
  }

  .header-actions {
    display: flex;
    gap: 12px;
  }
}

.btn-upload,
.btn-refresh {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;

  .icon {
    font-size: 18px;
  }
}

.btn-upload {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;

  &:hover {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
  }
}

.btn-slicer {
  padding: 10px 20px;
  background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(23, 162, 184, 0.3);

  &:hover {
    background: linear-gradient(135deg, #138496 0%, #117a8b 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(23, 162, 184, 0.4);
  }
}

.btn-refresh {
  background: white;
  color: #666;
  border: 1px solid #ddd;

  &:hover:not(:disabled) {
    background: #f5f5f5;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.search-section {
  margin-bottom: 24px;
}

.search-bar {
  display: flex;
  gap: 12px;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;

  &:focus {
    outline: none;
    border-color: #4CAF50;
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
  }
}

.loading-state,
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f0f0f0;
  border-top-color: #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-icon,
.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.studies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.study-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  }
}

.study-thumbnail {
  width: 100%;
  height: 200px;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .thumbnail-placeholder {
    .placeholder-icon {
      font-size: 64px;
      opacity: 0.3;
    }
  }
}

.study-info {
  padding: 16px;

  .patient-name {
    font-size: 18px;
    font-weight: 700;
    color: #222;
    margin-bottom: 4px;
  }

  .patient-id {
    font-size: 12px;
    color: #999;
    margin-bottom: 8px;
  }

  .study-description {
    font-size: 14px;
    color: #666;
    margin-bottom: 12px;
  }

  .study-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;

    .meta-item {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      color: #666;

      .meta-icon {
        font-size: 14px;
      }
    }
  }
}

.study-actions {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  border-top: 1px solid #f0f0f0;
}

.btn-view,
.btn-delete {
  flex: 1;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-view {
  background: #4CAF50;
  color: white;

  &:hover {
    background: #45a049;
  }
}

.btn-delete {
  background: white;
  color: #f44336;
  border: 1px solid #f44336;

  &:hover {
    background: #f44336;
    color: white;
  }
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 900px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;

  h3 {
    font-size: 20px;
    font-weight: 700;
    color: #222;
  }
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: #f5f5f5;
  color: #666;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #e0e0e0;
  }
}

.modal-body {
  padding: 24px;
}

.btn-upload-large {
  padding: 16px 32px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 24px;

  &:hover {
    background: #45a049;
  }
}
</style>
