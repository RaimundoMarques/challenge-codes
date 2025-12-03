<template>
  <div v-if="show" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>Confirmar Exclusão</h3>
        <button @click="closeModal" class="close-btn">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="warning-message">
          <div class="warning-icon">⚠️</div>
          <div class="warning-text">
            <h4>Tem certeza que deseja excluir este usuário?</h4>
            <p>Esta ação não pode ser desfeita.</p>
          </div>
        </div>
        
        <div class="user-info" v-if="user">
          <div class="info-item">
            <strong>Nome:</strong> {{ user.name || user.username }}
          </div>
          <div class="info-item">
            <strong>Username:</strong> {{ user.username }}
          </div>
          <div class="info-item">
            <strong>Email:</strong> {{ user.email || 'Não informado' }}
          </div>
          <div class="info-item">
            <strong>Função:</strong> {{ user.role }}
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="closeModal" class="btn btn-secondary" :disabled="loading">
          Cancelar
        </button>
        <button 
          @click="handleDelete"
          class="btn btn-danger"
          :disabled="loading"
        >
          <span v-if="loading">Excluindo...</span>
          <span v-else>Excluir Usuário</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserDeleteModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    user: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    
    handleDelete() {
      this.$emit('delete', this.user)
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
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 10px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e1e5e9;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.warning-message {
  display: flex;
  align-items: center;
  gap: 1rem;
  background-color: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.warning-icon {
  font-size: 2rem;
}

.warning-text h4 {
  margin: 0 0 0.5rem 0;
  color: #856404;
}

.warning-text p {
  margin: 0;
  color: #856404;
  font-size: 0.9rem;
}

.user-info {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #e1e5e9;
}

.info-item {
  margin: 0.5rem 0;
  color: #666;
}

.info-item strong {
  color: #333;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e1e5e9;
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

.btn-danger {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
}

.btn:hover:not(:disabled) {
  opacity: 0.9;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
  
  .warning-message {
    flex-direction: column;
    text-align: center;
  }
}
</style>
