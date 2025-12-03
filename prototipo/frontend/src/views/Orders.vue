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
    <OrderFilters
      :filters="filters"
      :users="users"
      @filters-changed="handleFiltersChanged"
    />
    
    <div v-if="loading" class="loading">
      <p>Carregando ordens de serviço...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>Erro ao carregar ordens: {{ error }}</p>
    </div>
    
    <div v-else>
      <OrdersList
        :orders="filteredOrders"
        @reassign="showReassignModal"
      />
    </div>
    
    <!-- Modal de Reassign Técnico -->
    <ReassignModal
      :show="showModal"
      :order="selectedOrder"
      :technicians="technicians"
      :loading="reassigning"
      @close="closeModal"
      @reassign="reassignTechnician"
    />
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import OrderFilters from '../components/OrdersComponents/OrderFilters.vue'
import OrdersList from '../components/OrdersComponents/OrdersList.vue'
import ReassignModal from '../components/OrdersComponents/ReassignModal.vue'

export default {
  name: 'Orders',
  components: {
    OrderFilters,
    OrdersList,
    ReassignModal
  },
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
    
    handleFiltersChanged(newFilters) {
      this.filters = { ...newFilters }
    },
    
    showReassignModal(order) {
      this.selectedOrder = order
      this.showModal = true
    },
    
    closeModal() {
      this.showModal = false
      this.selectedOrder = null
      this.reassigning = false
    },
    
    async reassignTechnician(technicianId) {
      if (!this.selectedOrder || !technicianId) return
      
      this.reassigning = true
      
      try {
        await axios.put(`http://localhost:8000/orders/${this.selectedOrder.id}/assign-technician?technician_id=${technicianId}`)
        
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

.loading, .error {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #e74c3c;
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

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>
