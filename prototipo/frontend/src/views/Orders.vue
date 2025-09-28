<template>
  <div class="orders">
    <div class="header">
      <h1>📋 Ordens de Serviço</h1>
      <div class="header-actions">
        <router-link to="/orders/add" class="btn btn-success">+ Nova Ordem</router-link>
        <button @click="loadOrders" class="btn btn-primary">Atualizar</button>
      </div>
    </div>
    
    <!-- Filtros -->
    <div class="filters">
      <div class="filter-group">
        <label for="status-filter">Status:</label>
        <select id="status-filter" v-model="filters.status" @change="applyFilters">
          <option value="">Todos</option>
          <option value="open">Abertas</option>
          <option value="in_progress">Em Andamento</option>
          <option value="closed">Fechadas</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="user-filter">Técnico:</label>
        <select id="user-filter" v-model="filters.user_id" @change="applyFilters">
          <option value="">Todos</option>
          <option v-for="user in users" :key="user.id" :value="user.id">
            {{ user.name || user.username }}
          </option>
        </select>
      </div>
    </div>
    
    <div v-if="loading" class="loading">
      <p>Carregando ordens de serviço...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>Erro ao carregar ordens: {{ error }}</p>
    </div>
    
    <div v-else class="orders-list">
      <div v-if="filteredOrders.length === 0" class="empty">
        <p>Nenhuma ordem de serviço encontrada</p>
      </div>
      
      <div v-else>
        <div class="order-card" v-for="order in filteredOrders" :key="order.id">
          <div class="order-header">
            <div class="order-title">
              <h3>{{ order.title }}</h3>
              <div class="order-meta">
                <span :class="['status-badge', `status-${order.status}`]">
                  {{ getStatusText(order.status) }}
                </span>
                <span class="technician-badge" v-if="order.user">
                  👨‍🔧 {{ order.user.name || order.user.username }}
                </span>
              </div>
            </div>
            <div class="order-actions">
              <button 
                @click="showReassignModal(order)"
                class="btn btn-sm btn-secondary"
                title="Reatribuir técnico"
              >
                🔄
              </button>
              <router-link :to="`/orders/${order.id}`" class="btn btn-sm btn-primary">
                Ver Detalhes
              </router-link>
            </div>
          </div>
          
          <div class="order-content">
            <div class="order-info">
              <div class="info-item">
                <strong>Cliente:</strong> {{ order.client?.name || 'N/A' }}
              </div>
              <div class="info-item">
                <strong>Equipamento:</strong> 
                {{ getEquipmentDescription(order.equipment) }}
              </div>
              <div class="info-item">
                <strong>Técnico:</strong> {{ order.user?.name || order.user?.username || 'N/A' }}
              </div>
              <div class="info-item">
                <strong>Criada em:</strong> {{ formatDate(order.created_at) }}
              </div>
            </div>
            
            <div v-if="order.description" class="order-description">
              <strong>Descrição:</strong>
              <p>{{ order.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal de Reassign Técnico -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Reatribuir Técnico</h3>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="current-assignment" v-if="selectedOrder">
            <p><strong>Ordem:</strong> {{ selectedOrder.title }}</p>
            <p><strong>Técnico Atual:</strong> {{ selectedOrder.user?.name || selectedOrder.user?.username || 'Não atribuído' }}</p>
          </div>
          
          <div class="form-group">
            <label for="new-technician">Novo Técnico:</label>
            <select id="new-technician" v-model="newTechnicianId">
              <option value="">Selecione um técnico</option>
              <option v-for="technician in technicians" :key="technician.id" :value="technician.id">
                {{ technician.name || technician.username }} ({{ technician.role }})
              </option>
            </select>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="closeModal" class="btn btn-secondary">Cancelar</button>
          <button @click="reassignTechnician" class="btn btn-primary" :disabled="!newTechnicianId || reassigning">
            <span v-if="reassigning">Reatribuindo...</span>
            <span v-else>Reatribuir</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  name: 'Orders',
  data() {
    return {
      orders: [],
      users: [],
      technicians: [],
      loading: false,
      error: null,
      filters: {
        status: '',
        user_id: ''
      },
      showModal: false,
      selectedOrder: null,
      newTechnicianId: '',
      reassigning: false
    }
  },
  computed: {
    ...mapState('auth', ['user']),
    
    filteredOrders() {
      let filtered = [...this.orders]
      
      if (this.filters.status) {
        filtered = filtered.filter(order => order.status === this.filters.status)
      }
      
      if (this.filters.user_id) {
        filtered = filtered.filter(order => order.user_id === parseInt(this.filters.user_id))
      }
      
      return filtered
    }
  },
  mounted() {
    this.loadOrders()
    this.loadUsers()
    this.loadTechnicians()
  },
  methods: {
    async loadOrders() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('http://localhost:8000/orders/')
        this.orders = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || error.message
        console.error('Erro ao carregar ordens:', error)
      } finally {
        this.loading = false
      }
    },
    
    async loadUsers() {
      try {
        const response = await axios.get('http://localhost:8000/users/')
        this.users = response.data
      } catch (error) {
        console.error('Erro ao carregar usuários:', error)
      }
    },
    
    async loadTechnicians() {
      try {
        const response = await axios.get('http://localhost:8000/orders/technicians/')
        this.technicians = response.data
      } catch (error) {
        console.error('Erro ao carregar técnicos:', error)
      }
    },
    
    showReassignModal(order) {
      this.selectedOrder = order
      this.newTechnicianId = ''
      this.showModal = true
    },
    
    closeModal() {
      this.showModal = false
      this.selectedOrder = null
      this.newTechnicianId = ''
      this.reassigning = false
    },
    
    async reassignTechnician() {
      if (!this.selectedOrder || !this.newTechnicianId) return
      
      this.reassigning = true
      
      try {
        await axios.put(`http://localhost:8000/orders/${this.selectedOrder.id}/assign-technician?technician_id=${this.newTechnicianId}`)
        
        // Recarregar lista de ordens
        await this.loadOrders()
        
        // Fechar modal
        this.closeModal()
        
        // Feedback de sucesso
        alert('Técnico reatribuído com sucesso!')
        
      } catch (error) {
        alert('Erro ao reatribuir técnico: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.reassigning = false
      }
    },
    
    applyFilters() {
      // Os filtros são aplicados automaticamente via computed
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
.orders {
  max-width: 1200px;
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

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.filters {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  display: flex;
  gap: 2rem;
  align-items: end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  min-width: 200px;
}

.filter-group label {
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

.filter-group select {
  padding: 0.5rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
}

.filter-group select:focus {
  outline: none;
  border-color: #667eea;
}

.loading, .error, .empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #e74c3c;
}

.orders-list {
  display: grid;
  gap: 1rem;
}

.order-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.order-card:hover {
  transform: translateY(-2px);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.order-title {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.order-meta {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.technician-badge {
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 0.25rem 0.5rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.order-title h3 {
  color: #333;
  margin: 0;
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

.order-actions {
  display: flex;
  gap: 0.5rem;
}

.order-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item {
  color: #666;
}

.info-item strong {
  color: #333;
}

.order-description {
  color: #666;
}

.order-description strong {
  color: #333;
}

.order-description p {
  margin: 0.5rem 0 0 0;
  line-height: 1.4;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: opacity 0.3s;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  font-size: 0.9rem;
}

.btn-sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.8rem;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-success {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
}

.btn:hover {
  opacity: 0.9;
}

/* Modal Styles */
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

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e1e5e9;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .filters {
    flex-direction: column;
    gap: 1rem;
  }
  
  .filter-group {
    min-width: auto;
  }
  
  .order-content {
    grid-template-columns: 1fr;
  }
  
  .order-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .order-meta {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
}
</style>