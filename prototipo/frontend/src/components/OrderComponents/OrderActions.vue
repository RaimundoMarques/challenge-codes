<template>
  <div class="actions-section">
    <h2>⚡ Ações</h2>
    <div class="action-buttons">
      <button 
        @click="updateOrderStatus('in_progress')"
        :disabled="order.status === 'in_progress' || saving"
        class="btn btn-warning"
      >
        <span v-if="saving">Atualizando...</span>
        <span v-else>Iniciar OS</span>
      </button>
      
      <button 
        @click="updateOrderStatus('closed')"
        :disabled="order.status === 'closed' || saving"
        class="btn btn-success"
      >
        <span v-if="saving">Finalizando...</span>
        <span v-else>Finalizar OS</span>
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'OrderActions',
  props: {
    order: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      saving: false
    }
  },
  methods: {
    async updateOrderStatus(newStatus) {
      this.saving = true
      
      try {
        await axios.put(`http://localhost:8000/orders/${this.order.id}`, {
          status: newStatus
        })
        
        // Emitir evento de sucesso
        this.$emit('status-updated', newStatus)
        
        const statusText = newStatus === 'in_progress' ? 'iniciada' : 'finalizada'
        alert(`Ordem de serviço ${statusText} com sucesso!`)
        
      } catch (error) {
        alert('Erro ao atualizar status: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style scoped>
.actions-section {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.actions-section h2 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
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

.btn-warning {
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
  color: white;
}

.btn-success {
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
  color: white;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn:hover:not(:disabled) {
  opacity: 0.9;
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
  }
}
</style>
