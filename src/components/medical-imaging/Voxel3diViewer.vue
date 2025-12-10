<template>
  <div class="voxel3di-viewer-wrapper">
    <!-- Loading State -->
    <div v-if="loading" class="viewer-loading">
      <div class="loading-spinner"></div>
      <p>Loading Voxel3di Viewer...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="viewer-error">
      <div class="error-icon">⚠️</div>
      <h3>Failed to Load Viewer</h3>
      <p>{{ error }}</p>
      <button @click="retryLoad" class="retry-btn">Retry</button>
    </div>

    <!-- Voxel3di Viewer Iframe -->
    <iframe
      v-else
      ref="voxel3diFrame"
      :src="viewerUrl"
      class="voxel3di-iframe"
      frameborder="0"
      allowfullscreen
      @load="onFrameLoad"
      @error="onFrameError"
    ></iframe>
  </div>
</template>

<script>
export default {
  name: 'Voxel3diViewer',
  props: {
    seriesInstanceUID: {
      type: String,
      default: null
    },
    sopInstanceUID: {
      type: String,
      default: null
    },
    dicomWebRoot: {
      type: String,
      default: () => process.env.VUE_APP_DICOM_WEB_ROOT || 'http://localhost:8080/dcm4chee-arc/aets/DCM4CHEE/rs'
    }
  },
  data() {
    return {
      loading: true,
      error: null,
      viewerUrl: '',
      studyInstanceUID: this.$route.params.studyUID || null
    };
  },
  computed: {
    voxel3diBaseUrl() {
      return process.env.VUE_APP_VOXEL3DI_URL || 'http://localhost:3000';
    }
  },
  watch: {
    studyInstanceUID: {
      immediate: true,
      handler(newVal, oldVal) {
        console.log('studyInstanceUID watcher triggered:', { newVal, oldVal });
        this.buildViewerUrl();
      }
    }
  },
  methods: {
    buildViewerUrl() {
      try {
        this.loading = true;
        this.error = null;

        console.log('buildViewerUrl called with studyInstanceUID:', this.studyInstanceUID);

        if (!this.studyInstanceUID) {
          console.warn('studyInstanceUID is empty, waiting...');
          this.loading = false;
          return;
        }

        // Build Voxel3di viewer URL for Orthanc
        // Format: http://127.0.0.1:8042/viewer?StudyInstanceUIDs=<uid>
        const params = new URLSearchParams();
        params.append('StudyInstanceUIDs', this.studyInstanceUID);
        
        this.viewerUrl = `${this.voxel3diBaseUrl}/viewer?${params.toString()}`;
        
        console.log('Voxel3di Viewer URL:', this.viewerUrl);
        console.log('voxel3diBaseUrl:', this.voxel3diBaseUrl);
      } catch (err) {
        console.error('Error building viewer URL:', err);
        this.error = err.message;
        this.loading = false;
      }
    },
    onFrameLoad() {
      this.loading = false;
      this.$emit('loaded');
    },
    onFrameError(event) {
      this.error = 'Failed to load Voxel3di Viewer. Please check if Voxel3di is running.';
      this.loading = false;
      this.$emit('error', event);
    },
    retryLoad() {
      this.buildViewerUrl();
    }
  }
};
</script>

<style lang="scss" scoped>
.voxel3di-viewer-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.voxel3di-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.viewer-loading,
.viewer-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
  text-align: center;
  padding: 40px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.viewer-error {
  .error-icon {
    font-size: 48px;
    margin-bottom: 16px;
  }

  h3 {
    font-size: 24px;
    margin-bottom: 12px;
    color: #ff6b6b;
  }

  p {
    font-size: 14px;
    color: #ccc;
    margin-bottom: 24px;
  }
}

.retry-btn {
  padding: 10px 24px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: #45a049;
    transform: translateY(-2px);
  }

  &:active {
    transform: translateY(0);
  }
}
</style>
