<template>
  <div class="checklist-section">
    <h2>✅ Checklist de Atividades</h2>
    
    <div v-if="checklistsLoading" class="loading">
      <p>Carregando checklist...</p>
    </div>
    
    <div v-else-if="checklists.length === 0" class="empty">
      <p>Nenhum checklist disponível</p>
    </div>
    
    <div v-else>
      <div class="checklist-selector">
        <label for="checklist-select">Selecione o Checklist:</label>
        <select 
          id="checklist-select"
          v-model="selectedChecklistId"
          @change="loadChecklistResponses"
        >
          <option value="">Selecione um checklist</option>
          <option v-for="checklist in checklists" :key="checklist.id" :value="checklist.id">
            {{ checklist.name }}
          </option>
        </select>
      </div>
      
      <div v-if="selectedChecklist && selectedChecklist.items.length > 0" class="checklist-items">
        <div v-for="item in selectedChecklist.items" :key="item.id" class="checklist-item">
          <label class="checkbox-label">
            <input
              type="checkbox"
              :checked="getChecklistResponse(item.id)"
              @change="updateChecklistResponse(item.id, $event.target.checked)"
              :disabled="saving"
            />
            {{ item.description }}
          </label>
        </div>
        
        <div class="checklist-actions">
          <button 
            @click="saveChecklistResponses"
            :disabled="saving || !selectedChecklistId"
            class="btn btn-primary"
          >
            <span v-if="saving">Salvando...</span>
            <span v-else>Salvar Checklist</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ChecklistSection',
  props: {
    orderId: {
      type: [String, Number],
      required: true
    }
  },
  data() {
    return {
      checklists: [],
      checklistsLoading: false,
      selectedChecklistId: '',
      checklistResponses: {},
      saving: false
    }
  },
  computed: {
    selectedChecklist() {
      return this.checklists.find(c => c.id === parseInt(this.selectedChecklistId))
    }
  },
  mounted() {
    this.loadChecklists()
  },
  methods: {
    async loadChecklists() {
      this.checklistsLoading = true
      try {
        const response = await axios.get('http://localhost:8000/orders/checklists/')
        this.checklists = response.data
      } catch (error) {
        console.error('Erro ao carregar checklists:', error)
      } finally {
        this.checklistsLoading = false
      }
    },
    
    async loadChecklistResponses() {
      if (!this.selectedChecklistId) {
        this.checklistResponses = {}
        return
      }
      
      try {
        const response = await axios.get(`http://localhost:8000/orders/${this.orderId}/checklist-responses/`)
        this.checklistResponses = {}
        response.data.forEach(response => {
          this.checklistResponses[response.checklist_item_id] = response.is_checked
        })
      } catch (error) {
        console.error('Erro ao carregar respostas do checklist:', error)
        this.checklistResponses = {}
      }
    },
    
    getChecklistResponse(itemId) {
      return this.checklistResponses[itemId] || false
    },
    
    updateChecklistResponse(itemId, checked) {
      this.checklistResponses[itemId] = checked
    },
    
    async saveChecklistResponses() {
      if (!this.selectedChecklistId) return
      
      this.saving = true
      
      try {
        const responses = Object.entries(this.checklistResponses).map(([itemId, isChecked]) => ({
          service_order_id: parseInt(this.orderId),
          checklist_item_id: parseInt(itemId),
          is_checked: isChecked
        }))
        
        console.log('Enviando respostas:', responses) // Debug
        
        await axios.post(`http://localhost:8000/orders/${this.orderId}/checklist-responses/`, responses, {
          headers: {
            'Content-Type': 'application/json'
          }
        })
        
        // Emitir evento de sucesso
        this.$emit('checklist-saved')
        
        alert('Checklist salvo com sucesso!')
        
      } catch (error) {
        console.error('Erro detalhado:', error.response?.data)
        alert('Erro ao salvar checklist: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style scoped>
.checklist-section {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.checklist-section h2 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.loading, .empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.checklist-selector {
  margin-bottom: 2rem;
}

.checklist-selector label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.checklist-selector select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  background-color: white;
}

.checklist-selector select:focus {
  outline: none;
  border-color: #667eea;
}

.checklist-items {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.checklist-item {
  margin-bottom: 1rem;
}

.checklist-item:last-child {
  margin-bottom: 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1.5;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin: 0;
  cursor: pointer;
}

.checklist-actions {
  margin-top: 1.5rem;
  text-align: center;
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
