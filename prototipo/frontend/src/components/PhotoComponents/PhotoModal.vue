<template>
  <div v-if="show" class="modal-overlay" @click="closeModal">
    <div class="photo-modal" @click.stop>
      <div class="photo-modal-header">
        <h3>Visualizar Foto</h3>
        <button @click="closeModal" class="close-btn">&times;</button>
      </div>
      <div class="photo-modal-body">
        <img 
          :src="getPhotoUrl(photo?.photo_url)" 
          :alt="`Foto ${photo?.id}`"
          class="photo-full"
        />
        <div class="photo-modal-info">
          <p><strong>ID:</strong> {{ photo?.id }}</p>
          <p><strong>Enviada em:</strong> {{ formatDate(photo?.uploaded_at) }}</p>
        </div>
      </div>
      <div class="photo-modal-footer">
        <button @click="deletePhoto" class="btn btn-danger">
          🗑️ Excluir Foto
        </button>
        <button @click="closeModal" class="btn btn-secondary">
          Fechar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PhotoModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    photo: {
      type: Object,
      default: null
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
    
    closeModal() {
      this.$emit('close')
    },
    
    deletePhoto() {
      if (!confirm('Tem certeza que deseja excluir esta foto?')) return
      this.$emit('delete-photo', this.photo?.id)
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.photo-modal {
  background: white;
  border-radius: 10px;
  max-width: 90%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.photo-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e1e5e9;
  background-color: #f8f9fa;
}

.photo-modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  color: #666;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.close-btn:hover {
  background-color: #e1e5e9;
}

.photo-modal-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  overflow: auto;
}

.photo-full {
  max-width: 100%;
  max-height: 70vh;
  object-fit: contain;
  border-radius: 8px;
}

.photo-modal-info {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  width: 100%;
}

.photo-modal-info p {
  margin: 0.5rem 0;
  color: #666;
}

.photo-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e1e5e9;
  background-color: #f8f9fa;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-danger {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn:hover {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .photo-modal {
    max-width: 95%;
  }
}
</style>
