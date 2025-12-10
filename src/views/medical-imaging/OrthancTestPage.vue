<template>
  <div class="orthanc-test-page">
    <h1>Orthanc PACS Connection Test</h1>
    
    <div class="test-section">
      <h2>Connection Settings</h2>
      <div class="settings">
        <p><strong>Orthanc URL:</strong> {{ pacsUrl }}</p>
        <p><strong>DICOMweb Root:</strong> {{ dicomWebRoot }}</p>
        <p><strong>Username:</strong> orthanc</p>
        <p><strong>Password:</strong> orthanc</p>
      </div>
    </div>

    <div class="test-section">
      <h2>Connection Test</h2>
      <button @click="testConnection" :disabled="testing" class="test-btn">
        {{ testing ? 'Testing...' : 'Test Connection' }}
      </button>
      
      <div v-if="testResult" class="result" :class="testResult.success ? 'success' : 'error'">
        <h3>{{ testResult.success ? '✅ Success' : '❌ Failed' }}</h3>
        <pre>{{ JSON.stringify(testResult, null, 2) }}</pre>
      </div>
    </div>

    <div class="test-section">
      <h2>Upload DICOM File</h2>
      <input type="file" @change="onFileSelect" accept=".dcm" />
      <button @click="uploadFile" :disabled="!selectedFile || uploading" class="upload-btn">
        {{ uploading ? 'Uploading...' : 'Upload to Orthanc' }}
      </button>
      
      <div v-if="uploadResult" class="result" :class="uploadResult.success ? 'success' : 'error'">
        <h3>{{ uploadResult.success ? '✅ Upload Success' : '❌ Upload Failed' }}</h3>
        <pre>{{ JSON.stringify(uploadResult, null, 2) }}</pre>
      </div>
    </div>

    <div class="test-section">
      <h2>Debug Log</h2>
      <div class="debug-log">
        <div v-for="(log, index) in debugLogs" :key="index" class="log-entry">
          {{ log }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'OrthancTestPage',
  data() {
    return {
      pacsUrl: process.env.VUE_APP_PACS_URL || 'http://127.0.0.1:8043',
      dicomWebRoot: process.env.VUE_APP_DICOM_WEB_ROOT || 'http://127.0.0.1:8043/dicom-web',
      testing: false,
      testResult: null,
      selectedFile: null,
      uploading: false,
      uploadResult: null,
      debugLogs: []
    };
  },
  methods: {
    addLog(message) {
      const timestamp = new Date().toLocaleTimeString();
      this.debugLogs.unshift(`[${timestamp}] ${message}`);
    },
    
    async testConnection() {
      this.testing = true;
      this.testResult = null;
      this.addLog('Testing connection to Orthanc...');
      
      try {
        const url = `${this.dicomWebRoot}/studies`;
        this.addLog(`URL: ${url}`);
        
        const response = await axios.get(url, {
          headers: {
            'Authorization': 'Basic ' + btoa('orthanc:orthanc'),
            'Accept': 'application/json'
          }
        });
        
        this.testResult = {
          success: true,
          status: response.status,
          data: response.data,
          headers: response.headers
        };
        this.addLog('✅ Connection successful!');
      } catch (error) {
        this.testResult = {
          success: false,
          error: error.message,
          status: error.response?.status,
          data: error.response?.data,
          details: error.toString()
        };
        this.addLog(`❌ Connection failed: ${error.message}`);
      } finally {
        this.testing = false;
      }
    },
    
    onFileSelect(event) {
      this.selectedFile = event.target.files[0];
      this.addLog(`File selected: ${this.selectedFile?.name}`);
    },
    
    async uploadFile() {
      if (!this.selectedFile) return;
      
      this.uploading = true;
      this.uploadResult = null;
      this.addLog(`Uploading ${this.selectedFile.name}...`);
      
      try {
        const url = `${this.pacsUrl}/instances`;
        this.addLog(`Upload URL: ${url}`);
        
        const response = await axios.post(url, this.selectedFile, {
          headers: {
            'Content-Type': 'application/dicom',
            'Authorization': 'Basic ' + btoa('orthanc:orthanc')
          }
        });
        
        this.uploadResult = {
          success: true,
          status: response.status,
          data: response.data
        };
        this.addLog('✅ Upload successful!');
      } catch (error) {
        this.uploadResult = {
          success: false,
          error: error.message,
          status: error.response?.status,
          data: error.response?.data,
          details: error.toString()
        };
        this.addLog(`❌ Upload failed: ${error.message}`);
      } finally {
        this.uploading = false;
      }
    }
  },
  mounted() {
    this.addLog('Orthanc Test Page loaded');
    this.addLog(`PACS URL: ${this.pacsUrl}`);
    this.addLog(`DICOMweb Root: ${this.dicomWebRoot}`);
  }
};
</script>

<style scoped>
.orthanc-test-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

h1 {
  color: #333;
  border-bottom: 2px solid #4CAF50;
  padding-bottom: 10px;
}

.test-section {
  margin: 30px 0;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}

.test-section h2 {
  margin-top: 0;
  color: #555;
}

.settings p {
  margin: 10px 0;
  font-family: monospace;
}

.test-btn, .upload-btn {
  padding: 12px 24px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin: 10px 10px 10px 0;
}

.test-btn:hover, .upload-btn:hover {
  background: #45a049;
}

.test-btn:disabled, .upload-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.result {
  margin-top: 20px;
  padding: 15px;
  border-radius: 4px;
}

.result.success {
  background: #d4edda;
  border: 1px solid #c3e6cb;
}

.result.error {
  background: #f8d7da;
  border: 1px solid #f5c6cb;
}

.result h3 {
  margin-top: 0;
}

.result pre {
  background: white;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
}

.debug-log {
  background: #1e1e1e;
  color: #00ff00;
  padding: 15px;
  border-radius: 4px;
  max-height: 300px;
  overflow-y: auto;
  font-family: 'Courier New', monospace;
  font-size: 12px;
}

.log-entry {
  margin: 5px 0;
}

input[type="file"] {
  margin: 10px 0;
  padding: 8px;
}
</style>
