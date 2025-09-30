<template>
  <div class="form-section">
    <h3>Atribuição de Técnico</h3>
    
    <div class="form-group">
      <label for="technician_id">Técnico Responsável *</label>
      <select
        id="technician_id"
        v-model="selectedTechnicianId"
        required
        :disabled="loading"
        @change="onTechnicianChange"
      >
        <option value="">Selecione um técnico</option>
        <option v-for="technician in technicians" :key="technician.id" :value="technician.id">
          {{ technician.name || technician.username }} ({{ technician.role }})
        </option>
      </select>
      <small class="form-help">
        O técnico selecionado será responsável por executar esta ordem de serviço
      </small>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TechnicianSelector',
  props: {
    technicians: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    value: {
      type: [String, Number],
      default: ''
    }
  },
  data() {
    return {
      selectedTechnicianId: this.value
    }
  },
  watch: {
    value(newValue) {
      this.selectedTechnicianId = newValue
    }
  },
  methods: {
    onTechnicianChange() {
      this.$emit('input', this.selectedTechnicianId)
      this.$emit('technician-selected', this.selectedTechnicianId)
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

.form-help {
  margin-top: 0.5rem;
  color: #666;
  font-size: 0.85rem;
  font-style: italic;
}
</style>
