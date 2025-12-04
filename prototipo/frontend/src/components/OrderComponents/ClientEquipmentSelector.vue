<template>
  <div class="form-section">
    <h3>Cliente e Equipamento</h3>
    
    <div class="form-row">
      <div class="form-group">
        <label for="client_id">Cliente *</label>
        <select
          id="client_id"
          v-model="selectedClientId"
          required
          :disabled="loading"
          @change="onClientChange"
        >
          <option value="">Selecione um cliente</option>
          <option v-for="client in clients" :key="client.id" :value="client.id">
            {{ client.name }}
          </option>
        </select>
        <button 
          type="button" 
          @click="toggleNewClientForm"
          class="btn btn-sm btn-outline"
        >
          + Novo Cliente
        </button>
      </div>
      
      <div class="form-group">
        <label for="equipment_id">Equipamento *</label>
        <select
          id="equipment_id"
          v-model="selectedEquipmentId"
          required
          :disabled="loading || !selectedClientId"
          @change="onEquipmentChange"
        >
          <option value="">Selecione um equipamento</option>
          <option v-for="equipment in equipments" :key="equipment.id" :value="equipment.id">
            {{ getEquipmentDescription(equipment) }}
          </option>
        </select>
        <button 
          type="button" 
          @click="toggleNewEquipmentForm"
          class="btn btn-sm btn-outline"
          :disabled="!selectedClientId"
        >
          + Novo Equipamento
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClientEquipmentSelector',
  props: {
    clients: {
      type: Array,
      default: () => []
    },
    equipments: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    clientId: {
      type: [String, Number],
      default: ''
    },
    equipmentId: {
      type: [String, Number],
      default: ''
    }
  },
  data() {
    return {
      selectedClientId: this.clientId,
      selectedEquipmentId: this.equipmentId
    }
  },
  watch: {
    clientId(newValue) {
      this.selectedClientId = newValue
    },
    equipmentId(newValue) {
      this.selectedEquipmentId = newValue
    }
  },
  methods: {
    onClientChange() {
      this.$emit('client-selected', this.selectedClientId)
      this.selectedEquipmentId = '' // Reset equipment when client changes
    },
    
    onEquipmentChange() {
      this.$emit('equipment-selected', this.selectedEquipmentId)
    },
    
    getEquipmentDescription(equipment) {
      if (!equipment) return 'N/A'
      let description = equipment.type || ''
      if (equipment.brand) description += ` ${equipment.brand}`
      if (equipment.model) description += ` ${equipment.model}`
      if (equipment.serial_number) description += ` (SN: ${equipment.serial_number})`
      return description
    },
    
    toggleNewClientForm() {
      this.$emit('show-new-client-form')
    },
    
    toggleNewEquipmentForm() {
      if (this.selectedClientId) {
        this.$emit('show-new-equipment-form')
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

.form-section h3 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
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

.form-group select {
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
  width: 100%;
  box-sizing: border-box;
  background-color: white;
  margin-bottom: 0.5rem;
}

.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.form-group select:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.btn {
  padding: 0.5rem 1rem;
  border: 2px solid #e1e5e9;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  background-color: white;
  color: #667eea;
}

.btn:hover {
  background-color: #f0f2ff;
  border-color: #667eea;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: #f8f9fa;
  color: #999;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>
