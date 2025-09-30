<template>
  <div class="photo-gallery">
    <div v-if="photos.length === 0 && !loading" class="empty-photos">
      <p>Nenhuma foto adicionada ainda</p>
    </div>
    
    <div v-else-if="loading" class="loading">
      <p>Carregando fotos...</p>
    </div>
    
    <div v-else class="photos-grid">
      <div v-for="photo in photos" :key="photo.id" class="photo-item">
        <div class="photo-container">
          <img 
            :src="getPhotoUrl(photo.photo_url)" 
            :alt="`Foto ${photo.id}`"
            @click="openPhotoModal(photo)"
            class="photo-thumbnail"
          />
          <div class="photo-overlay">
            <button @click="openPhotoModal(photo)" class="btn btn-sm btn-primary" title="Ver foto">
              👁️
            </button>
            <button @click="deletePhoto(photo.id)" class="btn btn-sm btn-danger" title="Excluir foto">
              🗑️
            </button>
          </div>
        </div>
        <div class="photo-info">
          <small>{{ formatDate(photo.uploaded_at) }}</small>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PhotoGallery',
  props: {
    orderId: {
      type: [String, Number],
      required: true
    },
    photos: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    getPhotoUrl(photoUrl) {
      return `http://localhost:8000/orders${photoUrl}`
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR')
    },
    
    openPhotoModal(photo) {
      this.$emit('open-photo-modal', photo)
    },
    
    async deletePhoto(photoId) {
      if (!confirm('Tem certeza que deseja excluir esta foto?')) return
      
      try {
        await axios.delete(`http://localhost:8000/orders/photos/${photoId}`)
        
        // Emitir evento de sucesso para recarregar fotos
        this.$emit('photo-deleted')
        
        alert('Foto excluída com sucesso!')
        
      } catch (error) {
        alert('Erro ao excluir foto: ' + (error.response?.data?.detail || error.message))
      }
    }
  }
}
</script>

<style scoped>
.empty-photos {
  text-align: center;
  padding: 2rem;
  color: #666;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.photos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
}

.photo-item {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.photo-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.photo-container {
  position: relative;
  overflow: hidden;
}

.photo-thumbnail {
  width: 100%;
  height: 200px;
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.photo-thumbnail:hover {
  transform: scale(1.1);
}

.photo-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.photo-container:hover .photo-overlay {
  opacity: 1;
}

.photo-info {
  padding: 0.75rem;
  background-color: #f8f9fa;
  text-align: center;
}

.photo-info small {
  color: #666;
  font-size: 0.85rem;
}

.btn {
  padding: 0.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: opacity 0.3s;
  font-size: 1rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-danger {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
}

.btn:hover {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .photos-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
</style>
