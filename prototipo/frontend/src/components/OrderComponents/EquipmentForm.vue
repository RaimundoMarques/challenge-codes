<template>
  <div v-if="show" class="form-section new-equipment-form">
    <h3>Novo Equipamento</h3>
    <div class="form-row">
      <div class="form-group">
        <label for="new_equipment_type">Tipo *</label>
        <input
          id="new_equipment_type"
          v-model="equipment.type"
          type="text"
          required
          placeholder="Ex: Notebook, Desktop, Servidor"
          :disabled="loading"
        />
      </div>
      <div class="form-group">
        <label for="new_equipment_brand">Marca</label>
        <input
          id="new_equipment_brand"
          v-model="equipment.brand"
          type="text"
          placeholder="Ex: Dell, HP, Lenovo"
          :disabled="loading"
        />
      </div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label for="new_equipment_model">Modelo</label>
        <input
          id="new_equipment_model"
          v-model="equipment.model"
          type="text"
          placeholder="Ex: Inspiron 15, ThinkPad X1"
          :disabled="loading"
        />
      </div>
      <div class="form-group">
        <label for="new_equipment_serial">Número de Série</label>
        <input
          id="new_equipment_serial"
          v-model="equipment.serial_number"
          type="text"
          placeholder="Ex: SN123456789"
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
        @click="saveEquipment"
        class="btn btn-primary"
        :disabled="loading || !equipment.type.trim()"
      >
        <span v-if="loading">Salvando...</span>
        <span v-else>Salvar Equipamento</span>
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EquipmentForm',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    clientId: {
      type: [String, Number],
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      equipment: {
        type: '',
        brand: '',
        model: '',
        serial_number: ''
      }
    }
  },
  methods: {
    async saveEquipment() {
      if (!this.equipment.type.trim()) return
      
      try {
        const equipmentData = {
          ...this.equipment,
          client_id: parseInt(this.clientId)
        }
        
        const response = await axios.post('http://localhost:8000/orders/equipments/', equipmentData)
        
        // Emitir evento de sucesso com o equipamento criado
        this.$emit('equipment-created', response.data)
        
        // Limpar formulário
        this.resetForm()
        
        alert('Equipamento criado com sucesso!')
        
      } catch (error) {
        alert('Erro ao criar equipamento: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    cancel() {
      this.resetForm()
      this.$emit('cancel')
    },
    
    resetForm() {
      this.equipment = {
        type: '',
        brand: '',
        model: '',
        serial_number: ''
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

.new-equipment-form {
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
