<template>
  <div class="slot">
    <div class="slot-preview" :style="previewStyle">
      <img v-if="slotData.image" :src="slotData.image" :alt="slotData.title" />
      <span v-else>Preview – {{ slotData.title }}</span>
    </div>
    <div class="slot-meta">
      <div class="slot-text">
        <div class="slot-title">{{ slotData.title }}</div>
        <div class="slot-filename">{{ slotData.filename || 'No file selected' }}</div>
      </div>
      <div class="slot-actions">
        <label class="upload-btn">
          Upload
          <input 
            type="file" 
            accept="image/*" 
            @change="handleUpload"
            style="position: absolute; inset: 0; opacity: 0; cursor: pointer;"
          />
        </label>
        <button 
          type="button" 
          class="edit-btn" 
          @click="handleEdit"
          :disabled="!slotData.image"
        >
          Edit
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PhotoSlot',
  props: {
    slotData: {
      type: Object,
      required: true
    }
  },
  computed: {
    previewStyle() {
      if (this.slotData.aspectRatio) {
        return {
          aspectRatio: this.slotData.aspectRatio
        };
      }
      return {
        aspectRatio: '4/3'
      };
    }
  },
  methods: {
    handleUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      this.$emit('upload', {
        slotId: this.slotData.id,
        file: file
      });
      
      // Reset input
      event.target.value = '';
    },
    handleEdit() {
      if (!this.slotData.image) return;
      
      this.$emit('edit', {
        slotId: this.slotData.id
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.slot {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    border-color: #EA5A43;
  }
}

.slot-preview {
  flex: 1;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #777777;
  position: relative;
  overflow: hidden;
  padding: 16px;
  min-height: 200px;
  
  span {
    text-align: center;
    line-height: 1.4;
    max-width: 90%;
    font-weight: 500;
  }
  
  img {
    max-width: 100%;
    max-height: 100%;
    width: auto;
    height: auto;
    object-fit: contain;
    object-position: center;
    display: block;
    border-radius: 4px;
  }
}

.slot-meta {
  padding: 16px;
  background: white;
  border-top: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.slot-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 0;
}

.slot-title {
  font-size: 13px;
  font-weight: 700;
  color: #222222;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.slot-filename {
  font-size: 11px;
  color: #777777;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.slot-actions {
  display: flex;
  gap: 6px;
}

.upload-btn {
  position: relative;
  overflow: hidden;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 14px;
  border-radius: 8px;
  background: #FFE4DE;
  color: #EA5A43;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  
  &:hover {
    background: #EA5A43;
    color: white;
    transform: translateY(-1px);
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  }
}

.edit-btn {
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  padding: 8px 14px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: white;
  color: #777777;
  transition: all 0.2s ease;
  font-family: inherit;
  
  &:hover:not(:disabled) {
    background: #f8f9fa;
    border-color: #EA5A43;
    color: #EA5A43;
    transform: translateY(-1px);
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
</style>
