<template>
  <div class="activities-section">
    <h2>📝 Descrição das Atividades Realizadas</h2>
    <div class="form-group">
      <label for="activities-description">Descreva as atividades realizadas:</label>
      <textarea
        id="activities-description"
        v-model="activitiesDescription"
        :disabled="saving"
        placeholder="Descreva detalhadamente as atividades realizadas nesta ordem de serviço..."
        rows="6"
      ></textarea>
    </div>
    <button 
      @click="saveActivitiesDescription"
      :disabled="saving || !activitiesDescription.trim()"
      class="btn btn-primary"
    >
      <span v-if="saving">Salvando...</span>
      <span v-else>Salvar Descrição</span>
    </button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ActivitiesSection',
  props: {
    order: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      activitiesDescription: '',
      saving: false
    }
  },
  mounted() {
    this.activitiesDescription = this.order.activities_description || ''
  },
  methods: {
    async saveActivitiesDescription() {
      this.saving = true
      
      try {
        await axios.put(`http://localhost:8000/orders/${this.order.id}`, {
          activities_description: this.activitiesDescription
        })
        
        // Emitir evento de sucesso
        this.$emit('activities-saved')
        
        alert('Descrição das atividades salva com sucesso!')
        
      } catch (error) {
        alert('Erro ao salvar descrição: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style scoped>
.activities-section {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.activities-section h2 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.3s;
}

.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
}

.form-group textarea:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
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

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn:hover:not(:disabled) {
  opacity: 0.9;
}
</style>
