<template>
  <div class="order-detail">
    <div class="header">
      <h1>📋 Detalhes da Ordem de Serviço</h1>
      <router-link to="/orders" class="btn btn-secondary">Voltar</router-link>
    </div>
    
    <div v-if="loading" class="loading">
      <p>Carregando detalhes da ordem...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>Erro ao carregar ordem: {{ error }}</p>
    </div>
    
    <div v-else-if="order" class="order-content">
      <!-- Informações Básicas -->
      <div class="info-section">
        <h2>📋 Informações da Ordem</h2>
        <div class="info-grid">
          <div class="info-item">
            <label>Título:</label>
            <span>{{ order.title }}</span>
          </div>
          <div class="info-item">
            <label>Status:</label>
            <span :class="['status-badge', `status-${order.status}`]">
              {{ getStatusText(order.status) }}
            </span>
          </div>
          <div class="info-item">
            <label>Cliente:</label>
            <span>{{ order.client?.name || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <label>Equipamento:</label>
            <span>{{ getEquipmentDescription(order.equipment) }}</span>
          </div>
          <div class="info-item">
            <label>Técnico:</label>
            <span>{{ order.user?.name || order.user?.username || 'N/A' }}</span>
          </div>
          <div class="info-item">
            <label>Criada em:</label>
            <span>{{ formatDate(order.created_at) }}</span>
          </div>
        </div>
        
        <div v-if="order.description" class="description">
          <label>Descrição:</label>
          <p>{{ order.description }}</p>
        </div>
      </div>
      
      <!-- Campo de Descrição de Atividades -->
      <div class="activities-section">
        <h2>📝 Descrição das Atividades Realizadas</h2>
        <div class="form-group">
          <textarea
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
      
      <!-- Checklist -->
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
                <span class="checkmark"></span>
                {{ item.description }}
              </label>
            </div>
            
            <div class="checklist-actions">
              <button 
                @click="saveChecklistResponses"
                :disabled="saving"
                class="btn btn-primary"
              >
                <span v-if="saving">Salvando...</span>
                <span v-else>Salvar Checklist</span>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Upload de Fotos -->
      <div class="photos-section">
        <h2>📸 Fotos Comprovantes</h2>
        
        <div class="upload-area">
          <input
            type="file"
            ref="fileInput"
            @change="handleFileSelect"
            accept="image/*"
            multiple
            style="display: none"
          />
          <button 
            @click="$refs.fileInput.click()"
            :disabled="uploading"
            class="btn btn-secondary"
          >
            <span v-if="uploading">Enviando...</span>
            <span v-else>+ Adicionar Fotos</span>
          </button>
          <p class="upload-help">Selecione uma ou mais fotos para comprovar as atividades realizadas</p>
        </div>
        
        <div v-if="photos.length > 0" class="photos-grid">
          <div v-for="photo in photos" :key="photo.id" class="photo-item">
            <img :src="photo.photo_url" :alt="`Foto ${photo.id}`" />
            <div class="photo-info">
              <small>{{ formatDate(photo.uploaded_at) }}</small>
            </div>
          </div>
        </div>
        
        <div v-else class="empty">
          <p>Nenhuma foto enviada ainda</p>
        </div>
      </div>
      
      <!-- Ações -->
      <div class="actions-section">
        <h2>⚡ Ações</h2>
        <div class="action-buttons">
          <button 
            @click="updateOrderStatus('in_progress')"
            :disabled="order.status === 'in_progress' || saving"
            class="btn btn-warning"
          >
            Iniciar Trabalho
          </button>
          <button 
            @click="updateOrderStatus('closed')"
            :disabled="order.status === 'closed' || saving"
            class="btn btn-success"
          >
            Finalizar OS
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'OrderDetail',
  data() {
    return {
      order: null,
      loading: false,
      saving: false,
      uploading: false,
      error: null,
      checklists: [],
      checklistsLoading: false,
      selectedChecklistId: '',
      checklistResponses: {},
      activitiesDescription: '',
      photos: []
    }
  },
  computed: {
    selectedChecklist() {
      return this.checklists.find(c => c.id === parseInt(this.selectedChecklistId))
    }
  },
  mounted() {
    this.loadOrderDetails()
    this.loadChecklists()
  },
  methods: {
    async loadOrderDetails() {
      this.loading = true
      this.error = null
      
      try {
        const orderId = this.$route.params.id
        const response = await axios.get(`http://localhost:8000/orders/${orderId}`)
        this.order = response.data
        
        // Carregar descrição de atividades (se existir)
        this.activitiesDescription = this.order.activities_description || ''
        
        // Carregar fotos
        this.loadPhotos()
        
      } catch (error) {
        this.error = error.response?.data?.detail || error.message
      } finally {
        this.loading = false
      }
    },
    
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
      if (!this.selectedChecklistId) return
      
      try {
        const orderId = this.$route.params.id
        const response = await axios.get(`http://localhost:8000/orders/${orderId}/checklist-responses/`)
        
        // Converter respostas para objeto
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
      if (!this.selectedChecklist) return
      
      this.saving = true
      
      try {
        const orderId = this.$route.params.id
        const responses = this.selectedChecklist.items.map(item => ({
          checklist_item_id: item.id,
          is_checked: this.checklistResponses[item.id] || false
        }))
        
        await axios.post(`http://localhost:8000/orders/${orderId}/checklist-responses/`, responses)
        
        alert('Checklist salvo com sucesso!')
        
      } catch (error) {
        alert('Erro ao salvar checklist: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.saving = false
      }
    },
    
    async saveActivitiesDescription() {
      this.saving = true
      
      try {
        const orderId = this.$route.params.id
        await axios.put(`http://localhost:8000/orders/${orderId}`, {
          activities_description: this.activitiesDescription
        })
        
        alert('Descrição das atividades salva com sucesso!')
        
      } catch (error) {
        alert('Erro ao salvar descrição: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.saving = false
      }
    },
    
    async updateOrderStatus(newStatus) {
      this.saving = true
      
      try {
        const orderId = this.$route.params.id
        await axios.put(`http://localhost:8000/orders/${orderId}`, {
          status: newStatus
        })
        
        this.order.status = newStatus
        alert(`Status da ordem atualizado para: ${this.getStatusText(newStatus)}`)
        
      } catch (error) {
        alert('Erro ao atualizar status: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.saving = false
      }
    },
    
    handleFileSelect(event) {
      const files = event.target.files
      if (files.length === 0) return
      
      this.uploadFiles(files)
    },
    
    async uploadFiles(files) {
      this.uploading = true
      
      try {
        const orderId = this.$route.params.id
        
        for (let file of files) {
          const formData = new FormData()
          formData.append('file', file)
          formData.append('service_order_id', orderId)
          
          await axios.post(`http://localhost:8000/orders/${orderId}/photos/`, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
        }
        
        // Recarregar fotos
        this.loadPhotos()
        alert('Fotos enviadas com sucesso!')
        
      } catch (error) {
        alert('Erro ao enviar fotos: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.uploading = false
      }
    },
    
    async loadPhotos() {
      try {
        const orderId = this.$route.params.id
        const response = await axios.get(`http://localhost:8000/orders/${orderId}/photos/`)
        this.photos = response.data
      } catch (error) {
        console.error('Erro ao carregar fotos:', error)
      }
    },
    
    getStatusText(status) {
      const statusMap = {
        'open': 'Aberta',
        'in_progress': 'Em Andamento',
        'closed': 'Fechada'
      }
      return statusMap[status] || status
    },
    
    getEquipmentDescription(equipment) {
      if (!equipment) return 'N/A'
      
      let description = equipment.type
      if (equipment.brand) description += ` ${equipment.brand}`
      if (equipment.model) description += ` ${equipment.model}`
      if (equipment.serial_number) description += ` (SN: ${equipment.serial_number})`
      
      return description
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR')
    }
  }
}
</script>

<style scoped>
.order-detail {
  max-width: 1000px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h1 {
  color: #333;
}

.loading, .error, .empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #e74c3c;
}

.order-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.info-section,
.activities-section,
.checklist-section,
.photos-section,
.actions-section {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.info-section h2,
.activities-section h2,
.checklist-section h2,
.photos-section h2,
.actions-section h2 {
  margin: 0 0 1.5rem 0;
  color: #333;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-item label {
  font-weight: 600;
  color: #333;
}

.info-item span {
  color: #666;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  display: inline-block;
  width: fit-content;
}

.status-open {
  background-color: #ffeaa7;
  color: #d63031;
}

.status-in_progress {
  background-color: #74b9ff;
  color: white;
}

.status-closed {
  background-color: #00b894;
  color: white;
}

.description {
  margin-top: 1rem;
}

.description label {
  font-weight: 600;
  color: #333;
  display: block;
  margin-bottom: 0.5rem;
}

.description p {
  color: #666;
  line-height: 1.6;
  margin: 0;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  min-height: 120px;
}

.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
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
}

.checklist-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.checklist-item {
  padding: 1rem;
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  background-color: #f8f9fa;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  font-size: 1rem;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin: 0;
}

.upload-area {
  text-align: center;
  padding: 2rem;
  border: 2px dashed #e1e5e9;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.upload-help {
  margin-top: 0.5rem;
  color: #666;
  font-size: 0.9rem;
}

.photos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.photo-item {
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  overflow: hidden;
}

.photo-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.photo-info {
  padding: 0.5rem;
  background-color: #f8f9fa;
  text-align: center;
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

.btn-warning {
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
  color: white;
}

.btn-success {
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
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
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>
