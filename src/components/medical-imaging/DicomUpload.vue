<template>
  <div class="dicom-upload">
    <div class="upload-header">
      <h3>Upload DICOM Files</h3>
      <p>Select one or more DICOM files to upload to the PACS server</p>
    </div>

    <!-- File Drop Zone -->
    <div
      class="drop-zone"
      :class="{ 'drag-over': isDragging, 'has-files': files.length > 0 }"
      @drop.prevent="onDrop"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @click="triggerFileInput"
    >
      <input
        ref="fileInput"
        type="file"
        multiple
        accept=".dcm,.dicom"
        @change="onFileSelect"
        style="display: none"
      />

      <div v-if="files.length === 0" class="drop-zone-content">
        <div class="upload-icon">📁</div>
        <p class="drop-text">Drag & drop DICOM files here</p>
        <p class="or-text">or</p>
        <button class="browse-btn">Browse Files</button>
      </div>

      <div v-else class="files-list">
        <div v-for="(file, index) in files" :key="index" class="file-item">
          <div class="file-info">
            <span class="file-icon">📄</span>
            <div class="file-details">
              <span class="file-name">{{ file.name }}</span>
              <span class="file-size">{{ formatFileSize(file.size) }}</span>
            </div>
          </div>
          <div class="file-status">
            <span v-if="file.status === 'pending'" class="status-badge pending">Pending</span>
            <span v-else-if="file.status === 'uploading'" class="status-badge uploading">
              Uploading... {{ file.progress }}%
            </span>
            <span v-else-if="file.status === 'success'" class="status-badge success">✓ Uploaded</span>
            <span v-else-if="file.status === 'error'" class="status-badge error">✗ Failed</span>
          </div>
          <button
            v-if="file.status === 'pending' || file.status === 'error'"
            @click.stop="removeFile(index)"
            class="remove-btn"
          >
            ×
          </button>
        </div>
      </div>
    </div>

    <!-- Upload Actions -->
    <div v-if="files.length > 0" class="upload-actions">
      <button @click="clearFiles" class="btn-secondary" :disabled="uploading">
        Clear All
      </button>
      <button @click="uploadFiles" class="btn-primary" :disabled="uploading || allUploaded">
        {{ uploading ? 'Uploading...' : 'Upload to PACS' }}
      </button>
    </div>

    <!-- Upload Progress -->
    <div v-if="uploading" class="upload-progress">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: overallProgress + '%' }"></div>
      </div>
      <p class="progress-text">{{ uploadedCount }} / {{ files.length }} files uploaded</p>
    </div>

    <!-- Success Message -->
    <div v-if="uploadComplete && !uploading" class="success-message">
      <span class="success-icon">✓</span>
      <span>All files uploaded successfully!</span>
      <button @click="viewStudies" class="view-studies-btn">View Studies</button>
    </div>
  </div>
</template>

<script>
import { storeDicomFiles } from '@/services/pacsService';

export default {
  name: 'DicomUpload',
  data() {
    return {
      files: [],
      isDragging: false,
      uploading: false,
      uploadComplete: false
    };
  },
  computed: {
    uploadedCount() {
      return this.files.filter(f => f.status === 'success').length;
    },
    allUploaded() {
      return this.files.length > 0 && this.files.every(f => f.status === 'success');
    },
    overallProgress() {
      if (this.files.length === 0) return 0;
      const totalProgress = this.files.reduce((sum, file) => sum + (file.progress || 0), 0);
      return Math.round(totalProgress / this.files.length);
    }
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    onFileSelect(event) {
      const selectedFiles = Array.from(event.target.files);
      this.addFiles(selectedFiles);
      event.target.value = ''; // Reset input
    },
    onDrop(event) {
      this.isDragging = false;
      const droppedFiles = Array.from(event.dataTransfer.files);
      this.addFiles(droppedFiles);
    },
    onDragOver() {
      this.isDragging = true;
    },
    onDragLeave() {
      this.isDragging = false;
    },
    addFiles(newFiles) {
      const dicomFiles = newFiles.filter(file => {
        const ext = file.name.toLowerCase();
        return ext.endsWith('.dcm') || ext.endsWith('.dicom') || !ext.includes('.');
      });

      dicomFiles.forEach(file => {
        this.files.push({
          file,
          name: file.name,
          size: file.size,
          status: 'pending',
          progress: 0
        });
      });

      if (dicomFiles.length < newFiles.length) {
        alert('Some files were skipped (only DICOM files are accepted)');
      }
    },
    removeFile(index) {
      this.files.splice(index, 1);
    },
    clearFiles() {
      this.files = [];
      this.uploadComplete = false;
    },
    async uploadFiles() {
      this.uploading = true;
      this.uploadComplete = false;

      // Collect files to upload
      const filesToUpload = this.files
        .filter(f => f.status !== 'success')
        .map(f => f.file);

      if (filesToUpload.length === 0) {
        this.uploading = false;
        return;
      }

      try {
        // Upload all files
        const results = await storeDicomFiles(filesToUpload, (index, percent, total) => {
          // Find the file object and update progress
          const fileIndex = this.files.findIndex(f => f.file === filesToUpload[index]);
          if (fileIndex !== -1) {
            this.files[fileIndex].status = 'uploading';
            this.files[fileIndex].progress = percent;
          }
        });

        // Update file statuses based on results
        results.forEach((result, index) => {
          const fileIndex = this.files.findIndex(f => f.file === filesToUpload[index]);
          if (fileIndex !== -1) {
            if (result.success) {
              this.files[fileIndex].status = 'success';
              this.files[fileIndex].progress = 100;
            } else {
              this.files[fileIndex].status = 'error';
              this.files[fileIndex].error = result.error;
            }
          }
        });
      } catch (error) {
        console.error('Upload error:', error);
        // Mark all pending files as error
        this.files.forEach(f => {
          if (f.status === 'uploading' || f.status === 'pending') {
            f.status = 'error';
            f.error = error.message;
          }
        });
      }

      this.uploading = false;
      
      if (this.allUploaded) {
        this.uploadComplete = true;
        this.$emit('upload-complete', this.files);
      }
    },
    viewStudies() {
      this.$router.push('/medical-imaging');
    },
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }
  }
};
</script>

<style lang="scss" scoped>
.dicom-upload {
  max-width: 800px;
  margin: 0 auto;
}

.upload-header {
  margin-bottom: 24px;
  text-align: center;

  h3 {
    font-size: 24px;
    font-weight: 700;
    color: #222;
    margin-bottom: 8px;
  }

  p {
    font-size: 14px;
    color: #666;
  }
}

.drop-zone {
  border: 2px dashed #ddd;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #fafafa;

  &.drag-over {
    border-color: #4CAF50;
    background: #f0f8f0;
  }

  &.has-files {
    padding: 20px;
    text-align: left;
  }
}

.drop-zone-content {
  .upload-icon {
    font-size: 64px;
    margin-bottom: 16px;
  }

  .drop-text {
    font-size: 16px;
    font-weight: 600;
    color: #333;
    margin-bottom: 8px;
  }

  .or-text {
    font-size: 14px;
    color: #999;
    margin: 16px 0;
  }
}

.browse-btn {
  padding: 12px 32px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover {
    background: #45a049;
    transform: translateY(-2px);
  }
}

.files-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.file-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  transition: all 0.2s ease;

  &:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
}

.file-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;

  .file-icon {
    font-size: 24px;
  }

  .file-details {
    display: flex;
    flex-direction: column;
    gap: 4px;

    .file-name {
      font-size: 14px;
      font-weight: 600;
      color: #333;
    }

    .file-size {
      font-size: 12px;
      color: #999;
    }
  }
}

.file-status {
  margin-right: 12px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;

  &.pending {
    background: #e3f2fd;
    color: #1976d2;
  }

  &.uploading {
    background: #fff3e0;
    color: #f57c00;
  }

  &.success {
    background: #e8f5e9;
    color: #4CAF50;
  }

  &.error {
    background: #ffebee;
    color: #f44336;
  }
}

.remove-btn {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: #f5f5f5;
  color: #666;
  font-size: 20px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #ff5252;
    color: white;
  }
}

.upload-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn-primary,
.btn-secondary {
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.btn-primary {
  background: #4CAF50;
  color: white;

  &:hover:not(:disabled) {
    background: #45a049;
    transform: translateY(-2px);
  }
}

.btn-secondary {
  background: white;
  color: #666;
  border: 1px solid #ddd;

  &:hover:not(:disabled) {
    background: #f5f5f5;
  }
}

.upload-progress {
  margin-top: 24px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #45a049);
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  font-size: 14px;
  color: #666;
}

.success-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px;
  background: #e8f5e9;
  border: 1px solid #4CAF50;
  border-radius: 8px;
  margin-top: 24px;
  color: #2e7d32;
  font-weight: 600;

  .success-icon {
    font-size: 24px;
  }
}

.view-studies-btn {
  padding: 8px 16px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  margin-left: 12px;

  &:hover {
    background: #45a049;
  }
}
</style>
