<template>
  <div class="medical-imaging-viewer-page">
    <!-- Viewer Header -->
    <div class="viewer-header">
      <button @click="goBack" class="back-btn">
        <span class="icon">←</span>
        Back to Studies
      </button>
      <div class="study-info" v-if="studyMetadata">
        <h3>{{ studyMetadata.patientName || 'Unknown Patient' }}</h3>
        <p>Study: {{ studyMetadata.studyDescription || 'No description' }}</p>
      </div>
    </div>

    <!-- Voxel3di Viewer -->
    <div class="viewer-container">
      <Voxel3diViewer
        v-if="studyUID"
        :key="studyUID"
        @loaded="onViewerLoaded"
        @error="onViewerError"
      />
    </div>
  </div>
</template>

<script>
import Voxel3diViewer from '@/components/medical-imaging/Voxel3diViewer.vue';
import { getStudyMetadata } from '@/services/pacsService';

export default {
  name: 'MedicalImagingViewer',
  components: {
    Voxel3diViewer
  },
  data() {
    return {
      studyUID: this.$route.params.studyUID || null,
      studyMetadata: null
    };
  },
  created() {
    console.log('MedicalImagingViewer created, studyUID:', this.studyUID);
    console.log('Route params:', this.$route.params);
  },
  mounted() {
    if (this.studyUID) {
      this.loadStudyMetadata();
    } else {
      console.error('No studyUID in route params!');
    }
  },
  methods: {
    async loadStudyMetadata() {
      try {
        const metadata = await getStudyMetadata(this.studyUID);
        if (metadata && metadata.length > 0) {
          const firstInstance = metadata[0];
          this.studyMetadata = {
            patientName: this.getDicomValue(firstInstance, '00100010'),
            studyDescription: this.getDicomValue(firstInstance, '00081030')
          };
        }
      } catch (error) {
        console.error('Error loading study metadata:', error);
      }
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
    goBack() {
      this.$router.push({ name: 'MedicalImagingDashboard' });
    },
    onViewerLoaded() {
      console.log('Voxel3di Viewer loaded successfully');
    },
    onViewerError(error) {
      console.error('Voxel3di Viewer error:', error);
    }
  }
};
</script>

<style lang="scss" scoped>
.medical-imaging-viewer-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #000;
}

.viewer-header {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 16px 24px;
  background: #1a1a1a;
  border-bottom: 1px solid #333;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #333;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;

  .icon {
    font-size: 18px;
  }

  &:hover {
    background: #444;
  }
}

.study-info {
  flex: 1;
  color: white;

  h3 {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 4px;
  }

  p {
    font-size: 13px;
    color: #999;
  }
}

.viewer-container {
  flex: 1;
  overflow: hidden;
}
</style>
