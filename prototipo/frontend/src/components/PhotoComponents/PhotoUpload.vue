<template>
  <div class="photo-upload">
    <div class="upload-area" 
         @click="triggerFileUpload"
         @dragover.prevent="handleDragOver"
         @dragleave.prevent="handleDragLeave"
         @drop.prevent="handleFileDrop"
         :class="{ 'dragover': isDragOver }"
    >
      <input 
        ref="fileInput"
        type="file" 
        multiple 
        accept="image/*"
        @change="handleFileSelect"
        style="display: none;"
      />
      <div class="upload-content">
        <div class="upload-icon">📁</div>
        <p>Clique para selecionar fotos ou arraste aqui</p>
        <small>Formatos aceitos: JPG, PNG, GIF, BMP, WEBP (máx. 10MB cada)</small>
      </div>
    </div>
    
    <div v-if="uploading" class="upload-progress">
      <p>Enviando {{ uploadingFiles.length }} foto(s)...</p>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
      </div>
    </div>
    
    <div v-if="uploadError" class="error-message">
      {{ uploadError }}
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PhotoUpload',
  props: {
    orderId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      uploading: false,
      uploadingFiles: [],
      uploadProgress: 0,
      uploadError: null,
      isDragOver: false
    }
  },
  methods: {
    triggerFileUpload() {
      this.$refs.fileInput.click()
    },
    
    handleDragOver(event) {
      event.preventDefault()
      this.isDragOver = true
    },
    
    handleDragLeave(event) {
      event.preventDefault()
      this.isDragOver = false
    },
    
    handleFileSelect(event) {
      const files = Array.from(event.target.files)
      this.uploadPhotos(files)
    },
    
    handleFileDrop(event) {
      this.isDragOver = false
      const files = Array.from(event.dataTransfer.files)
      this.uploadPhotos(files)
    },
    
    async uploadPhotos(files) {
      if (files.length === 0) return
      
      this.uploading = true
      this.uploadingFiles = files
      this.uploadError = null
      this.uploadProgress = 0
      
      try {
        for (let i = 0; i < files.length; i++) {
          const file = files[i]
          const formData = new FormData()
          formData.append('file', file)
          
          await axios.post(`http://localhost:8000/orders/${this.orderId}/photos`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          
          this.uploadProgress = Math.round(((i + 1) / files.length) * 100)
        }
        
        // Emitir evento de sucesso
        this.$emit('upload-success')
        
        // Limpar input
        this.$refs.fileInput.value = ''
        
      } catch (error) {
        this.uploadError = error.response?.data?.detail || 'Erro ao fazer upload de fotos'
      } finally {
        this.uploading = false
        this.uploadingFiles = []
        this.uploadProgress = 0
      }
    }
  }
}
</script>

<style scoped>
.photo-upload {
  margin-bottom: 2rem;
}

.upload-area {
  border: 2px dashed #e1e5e9;
  border-radius: 10px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #f8f9fa;
}

.upload-area:hover, .upload-area.dragover {
  border-color: #667eea;
  background-color: #f0f2ff;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-icon {
  font-size: 3rem;
}

.upload-area p {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
  font-weight: 600;
}

.upload-area small {
  color: #666;
}

.upload-progress {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.progress-bar {
  width: 100%;
  height: 20px;
  background-color: #e1e5e9;
  border-radius: 10px;
  overflow: hidden;
  margin-top: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #fcc;
  margin-top: 1rem;
}
</style>
