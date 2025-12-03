<template>
  <div class="add-order">
    <div class="header">
      <h1>📋 Nova Ordem de Serviço</h1>
      <router-link to="/orders" class="btn btn-secondary">Voltar</router-link>
    </div>
    
    <div class="form-container">
      <form @submit.prevent="handleSubmit" class="order-form">
        <!-- Informações Básicas -->
        <OrderForm 
          :form="form" 
          :loading="loading" 
        />
        
        <!-- Cliente e Equipamento -->
        <ClientEquipmentSelector
          :clients="clients"
          :equipments="equipments"
          :loading="loading"
          :client-id="form.client_id"
          :equipment-id="form.equipment_id"
          @client-selected="handleClientSelected"
          @equipment-selected="handleEquipmentSelected"
          @client-created="handleClientCreated"
          @equipment-created="handleEquipmentCreated"
        />
        
        <!-- Formulário de Novo Cliente -->
        <ClientForm
          :show="showNewClientForm"
          :loading="loading"
          @client-created="handleClientCreated"
          @cancel="showNewClientForm = false"
        />
        
        <!-- Formulário de Novo Equipamento -->
        <EquipmentForm
          :show="showNewEquipmentForm"
          :client-id="form.client_id"
          :loading="loading"
          @equipment-created="handleEquipmentCreated"
          @cancel="showNewEquipmentForm = false"
        />
        
        <!-- Atribuição de Técnico -->
        <TechnicianSelector
          :technicians="technicians"
          :loading="loading"
          v-model="form.technician_id"
          @technician-selected="handleTechnicianSelected"
        />
        
        <!-- Botões de Ação -->
        <div class="form-actions">
          <button 
            type="button" 
            @click="resetForm"
            class="btn btn-secondary"
            :disabled="loading"
          >
            Limpar Formulário
          </button>
          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="loading || !isFormValid"
          >
            <span v-if="loading">Criando OS...</span>
            <span v-else>Criar Ordem de Serviço</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import OrderForm from './OrderForm.vue'
import ClientEquipmentSelector from './ClientEquipmentSelector.vue'
import ClientForm from './ClientForm.vue'
import EquipmentForm from './EquipmentForm.vue'
import TechnicianSelector from './TechnicianSelector.vue'

export default {
  name: 'AddOrder',
  components: {
    OrderForm,
    ClientEquipmentSelector,
    ClientForm,
    EquipmentForm,
    TechnicianSelector
  },
  data() {
    return {
      form: {
        title: '',
        description: '',
        status: 'open',
        client_id: '',
        equipment_id: '',
        technician_id: ''
      },
      clients: [],
      equipments: [],
      technicians: [],
      loading: false,
      showNewClientForm: false,
      showNewEquipmentForm: false
    }
  },
  computed: {
    isFormValid() {
      return this.form.title.trim() && 
             this.form.client_id && 
             this.form.equipment_id && 
             this.form.technician_id
    }
  },
  created() {
    this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        await Promise.all([
          this.loadClients(),
          this.loadTechnicians()
        ])
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
        alert('Erro ao carregar dados iniciais')
      } finally {
        this.loading = false
      }
    },
    
    async loadClients() {
      try {
        const response = await axios.get('http://localhost:8000/orders/clients/')
        this.clients = response.data
      } catch (error) {
        console.error('Erro ao carregar clientes:', error)
        this.clients = []
      }
    },
    
    async loadEquipments(clientId) {
      if (!clientId) {
        this.equipments = []
        return
      }
      
      try {
        const response = await axios.get(`http://localhost:8000/orders/equipments/?client_id=${clientId}`)
        this.equipments = response.data
      } catch (error) {
        console.error('Erro ao carregar equipamentos:', error)
        this.equipments = []
      }
    },
    
    async loadTechnicians() {
      try {
        const response = await axios.get('http://localhost:8000/users/')
        this.technicians = response.data.filter(user => 
          user.role === 'tecnico' || user.role === 'administrador'
        )
      } catch (error) {
        console.error('Erro ao carregar técnicos:', error)
        this.technicians = []
      }
    },
    
    handleClientSelected(clientId) {
      this.form.client_id = clientId
      this.form.equipment_id = '' // Reset equipment
      this.loadEquipments(clientId)
    },
    
    handleEquipmentSelected(equipmentId) {
      this.form.equipment_id = equipmentId
    },
    
    handleTechnicianSelected(technicianId) {
      this.form.technician_id = technicianId
    },
    
    handleClientCreated(client) {
      this.clients.push(client)
      this.form.client_id = client.id
      this.loadEquipments(client.id)
      this.showNewClientForm = false
    },
    
    handleEquipmentCreated(equipment) {
      this.equipments.push(equipment)
      this.form.equipment_id = equipment.id
      this.showNewEquipmentForm = false
    },
    
    async handleSubmit() {
      if (!this.isFormValid) {
        alert('Por favor, preencha todos os campos obrigatórios')
        return
      }
      
      this.loading = true
      
      try {
        const orderData = {
          title: this.form.title,
          description: this.form.description,
          status: this.form.status,
          client_id: parseInt(this.form.client_id),
          equipment_id: parseInt(this.form.equipment_id),
          technician_id: parseInt(this.form.technician_id)
        }
        
        const response = await axios.post('http://localhost:8000/orders/', orderData)
        
        alert('Ordem de serviço criada com sucesso!')
        this.$router.push('/orders')
        
      } catch (error) {
        console.error('Erro ao criar ordem:', error)
        alert('Erro ao criar ordem de serviço: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.loading = false
      }
    },
    
    resetForm() {
      this.form = {
        title: '',
        description: '',
        status: 'open',
        client_id: '',
        equipment_id: '',
        technician_id: ''
      }
      this.equipments = []
      this.showNewClientForm = false
      this.showNewEquipmentForm = false
    }
  }
}
</script>

<style scoped>
.add-order {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header h1 {
  color: #333;
  margin: 0;
  font-size: 2rem;
}

.form-container {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.order-form {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #e1e5e9;
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

.btn:hover:not(:disabled) {
  opacity: 0.9;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>
