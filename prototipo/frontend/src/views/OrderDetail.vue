<template>
  <div class="order-detail">
    <div class="header">
      <h1>📋 Detalhes da Ordem de Serviço</h1>
      <router-link to="/orders" class="btn btn-secondary">Voltar</router-link>
    </div>
    
    <div v-if="loading" class="loading">
      <p>Carregando detalhes da ordem...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>Erro ao carregar ordem: {{ error }}</p>
    </div>
    
    <div v-else-if="order" class="order-content">
      <!-- Informações Básicas -->
      <OrderInfo :order="order" />
      
      <!-- Descrição de Atividades -->
      <ActivitiesSection 
        :order="order" 
        @activities-saved="loadOrderDetails"
      />
      
      <!-- Fotos de Evidência -->
      <div class="photos-section">
        <h2>📸 Fotos de Evidência</h2>
        
        <!-- Upload de Fotos -->
        <PhotoUpload 
          :order-id="order.id"
          @upload-success="loadPhotos"
        />
        
        <!-- Galeria de Fotos -->
        <PhotoGallery 
          :order-id="order.id"
          :photos="photos"
          :loading="photosLoading"
          @open-photo-modal="openPhotoModal"
          @photo-deleted="loadPhotos"
        />
      </div>
      
      <!-- Checklist -->
      <ChecklistSection 
        :order-id="order.id"
        @checklist-saved="loadOrderDetails"
      />
      
      <!-- Ações -->
      <OrderActions 
        :order="order"
        @status-updated="loadOrderDetails"
      />
    </div>
    
    <!-- Modal de Visualização de Fotos -->
    <PhotoModal 
      :show="showPhotoModal"
      :photo="selectedPhoto"
      @close="closePhotoModal"
      @delete-photo="deletePhoto"
    />
  </div>
</template>

<script>
import axios from 'axios'
  import OrderInfo from '../components/OrderComponents/OrderInfo.vue'
import ActivitiesSection from '../components/OrderComponents/ActivitiesSection.vue'
import PhotoUpload from '../components/PhotoComponents/PhotoUpload.vue'
import PhotoGallery from '../components/PhotoComponents/PhotoGallery.vue'
import PhotoModal from '../components/PhotoComponents/PhotoModal.vue'
import ChecklistSection from '../components/OrderComponents/ChecklistSection.vue'
import OrderActions from '../components/OrderComponents/OrderActions.vue'

export default {
  name: 'OrderDetail',
  components: {
    OrderInfo,
    ActivitiesSection,
    PhotoUpload,
    PhotoGallery,
    PhotoModal,
    ChecklistSection,
    OrderActions
  },
  data() {
    return {
      order: null,
      loading: false,
      error: null,
      photos: [],
      photosLoading: false,
      showPhotoModal: false,
      selectedPhoto: null
    }
  },
  mounted() {
    this.loadOrderDetails()
  },
  methods: {
    async loadOrderDetails() {
      this.loading = true
      this.error = null
      
      try {
        const orderId = this.$route.params.id
        const response = await axios.get(`http://localhost:8000/orders/${orderId}`)
        this.order = response.data
        
        // Carregar fotos
        this.loadPhotos()
        
      } catch (error) {
        this.error = error.response?.data?.detail || error.message
      } finally {
        this.loading = false
      }
    },
    
    async loadPhotos() {
      this.photosLoading = true
      try {
        const orderId = this.$route.params.id
        const response = await axios.get(`http://localhost:8000/orders/${orderId}/photos`)
        this.photos = response.data
      } catch (error) {
        console.error('Erro ao carregar fotos:', error)
      } finally {
        this.photosLoading = false
      }
    },
    
    openPhotoModal(photo) {
      this.selectedPhoto = photo
      this.showPhotoModal = true
    },
    
    closePhotoModal() {
      this.showPhotoModal = false
      this.selectedPhoto = null
    },
    
    async deletePhoto(photoId) {
      if (!confirm('Tem certeza que deseja excluir esta foto?')) return
      
      try {
        await axios.delete(`http://localhost:8000/orders/photos/${photoId}`)
        
        // Recarregar fotos
        await this.loadPhotos()
        
        // Fechar modal se estiver aberto
        this.closePhotoModal()
        
        alert('Foto excluída com sucesso!')
        
      } catch (error) {
        alert('Erro ao excluir foto: ' + (error.response?.data?.detail || error.message))
      }
    }
  }
}
</script>

<style scoped>
.order-detail {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h1 {
  color: #333;
  margin: 0;
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #e74c3c;
}

.order-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.photos-section {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.photos-section h2 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn:hover {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>
