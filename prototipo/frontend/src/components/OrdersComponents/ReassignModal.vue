<template>
  <div v-if="show" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>Reatribuir Técnico</h3>
        <button @click="closeModal" class="close-btn">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="current-assignment" v-if="order">
          <p><strong>Ordem:</strong> {{ order.title }}</p>
          <p><strong>Técnico Atual:</strong> {{ order.user?.name || order.user?.username || 'Não atribuído' }}</p>
        </div>
        
        <div class="form-group">
          <label for="new-technician">Novo Técnico:</label>
          <select 
            id="new-technician" 
            v-model="selectedTechnicianId"
          >
            <option value="">Selecione um técnico</option>
            <option v-for="technician in technicians" :key="technician.id" :value="technician.id">
              {{ technician.name || technician.username }} ({{ technician.role }})
            </option>
          </select>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="closeModal" class="btn btn-secondary">Cancelar</button>
        <button 
          @click="handleReassign" 
          class="btn btn-primary" 
          :disabled="!selectedTechnicianId || loading"
        >
          <span v-if="loading">Reatribuindo...</span>
          <span v-else>Reatribuir</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReassignModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    order: {
      type: Object,
      default: null
    },
    technicians: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      selectedTechnicianId: ''
    }
  },
  watch: {
    show(newValue) {
      if (newValue) {
        this.selectedTechnicianId = ''
      }
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    
    handleReassign() {
      if (!this.selectedTechnicianId) return
      this.$emit('reassign', this.selectedTechnicianId)
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

.current-assignment {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.current-assignment p {
  margin: 0.25rem 0;
  color: #666;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

.form-group select {
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
}

.form-group select:focus {
  outline: none;
  border-color: #667eea;
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

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-secondary {
  background: #6c757d;
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
}
</style>
