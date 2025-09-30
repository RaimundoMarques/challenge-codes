<template>
  <div v-if="show" class="form-section new-client-form">
    <h3>Novo Cliente</h3>
    <div class="form-row">
      <div class="form-group">
        <label for="new_client_name">Nome *</label>
        <input
          id="new_client_name"
          v-model="client.name"
          type="text"
          required
          placeholder="Nome do cliente"
          :disabled="loading"
        />
      </div>
      <div class="form-group">
        <label for="new_client_email">Email</label>
        <input
          id="new_client_email"
          v-model="client.email"
          type="email"
          placeholder="email@exemplo.com"
          :disabled="loading"
        />
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label for="new_client_phone">Telefone</label>
        <input
          id="new_client_phone"
          v-model="client.phone"
          type="text"
          placeholder="(11) 99999-9999"
          :disabled="loading"
        />
      </div>
      <div class="form-group">
        <label for="new_client_address">Endereço</label>
        <input
          id="new_client_address"
          v-model="client.address"
          type="text"
          placeholder="Rua, número, bairro, cidade"
          :disabled="loading"
        />
      </div>
    </div>
    <div class="form-actions">
      <button 
        type="button" 
        @click="cancel"
        class="btn btn-secondary"
        :disabled="loading"
      >
        Cancelar
      </button>
      <button 
        type="button" 
        @click="saveClient"
        class="btn btn-primary"
        :disabled="loading || !client.name.trim()"
      >
        <span v-if="loading">Salvando...</span>
        <span v-else>Salvar Cliente</span>
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ClientForm',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      client: {
        name: '',
        email: '',
        phone: '',
        address: ''
      }
    }
  },
  methods: {
    async saveClient() {
      if (!this.client.name.trim()) return
      
      try {
        const response = await axios.post('http://localhost:8000/orders/clients/', this.client)
        
        // Emitir evento de sucesso com o cliente criado
        this.$emit('client-created', response.data)
        
        // Limpar formulário
        this.resetForm()
        
        alert('Cliente criado com sucesso!')
        
      } catch (error) {
        alert('Erro ao criar cliente: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    cancel() {
      this.resetForm()
      this.$emit('cancel')
    },
    
    resetForm() {
      this.client = {
        name: '',
        email: '',
        phone: '',
        address: ''
      }
    }
  }
}
</script>

<style scoped>
.form-section {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.new-client-form {
  background-color: #f8f9fa;
  border: 2px dashed #e1e5e9;
}

.form-section h3 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
  border-bottom: 2px solid #e1e5e9;
  padding-bottom: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 600;
  font-size: 0.95rem;
}

.form-group input {
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
  width: 100%;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.form-group input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
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

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-secondary {
  background: #6c757d;
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
  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>
