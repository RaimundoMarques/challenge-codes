<template>
  <div class="add-order">
    <div class="header">
      <h1>📋 Nova Ordem de Serviço</h1>
      <router-link to="/orders" class="btn btn-secondary">Voltar</router-link>
    </div>
    
    <div class="form-container">
      <form @submit.prevent="handleSubmit" class="order-form">
        <!-- Informações Básicas -->
        <div class="form-section">
          <h3>Informações Básicas</h3>
          
          <div class="form-row">
            <div class="form-group">
              <label for="title">Título da OS *</label>
              <input
                id="title"
                v-model="form.title"
                type="text"
                required
                :disabled="loading"
                placeholder="Ex: Manutenção preventiva notebook"
              />
            </div>
            
            <div class="form-group">
              <label for="status">Status</label>
              <select
                id="status"
                v-model="form.status"
                :disabled="loading"
              >
                <option value="open">Aberta</option>
                <option value="in_progress">Em Andamento</option>
                <option value="closed">Fechada</option>
              </select>
            </div>
          </div>
          
          <div class="form-group">
            <label for="description">Descrição</label>
            <textarea
              id="description"
              v-model="form.description"
              :disabled="loading"
              placeholder="Descreva os detalhes da ordem de serviço..."
              rows="4"
            ></textarea>
          </div>
        </div>
        
        <!-- Cliente e Equipamento -->
        <div class="form-section">
          <h3>Cliente e Equipamento</h3>
          
          <div class="form-row">
            <div class="form-group">
              <label for="client_id">Cliente *</label>
              <select
                id="client_id"
                v-model="form.client_id"
                required
                :disabled="loading"
                @change="loadClientEquipments"
              >
                <option value="">Selecione um cliente</option>
                <option v-for="client in clients" :key="client.id" :value="client.id">
                  {{ client.name }}
                </option>
              </select>
              <button 
                type="button" 
                @click="showNewClientForm = !showNewClientForm"
                class="btn btn-sm btn-outline"
              >
                + Novo Cliente
              </button>
            </div>
            
            <div class="form-group">
              <label for="equipment_id">Equipamento *</label>
              <select
                id="equipment_id"
                v-model="form.equipment_id"
                required
                :disabled="loading || !form.client_id"
              >
                <option value="">Selecione um equipamento</option>
                <option v-for="equipment in equipments" :key="equipment.id" :value="equipment.id">
                  {{ getEquipmentDescription(equipment) }}
                </option>
              </select>
              <button 
                type="button" 
                @click="showNewEquipmentForm = !showNewEquipmentForm"
                class="btn btn-sm btn-outline"
                :disabled="!form.client_id"
              >
                + Novo Equipamento
              </button>
            </div>
          </div>
        </div>
        
        <!-- Atribuição de Técnico -->
        <div class="form-section">
          <h3>Atribuição de Técnico</h3>
          
          <div class="form-group">
            <label for="technician_id">Técnico Responsável *</label>
            <select
              id="technician_id"
              v-model="form.technician_id"
              required
              :disabled="loading"
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
        
        <!-- Formulário de Novo Cliente -->
        <div v-if="showNewClientForm" class="form-section new-client-form">
          <h3>Novo Cliente</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="new_client_name">Nome *</label>
              <input
                id="new_client_name"
                v-model="newClient.name"
                type="text"
                required
                placeholder="Nome do cliente"
              />
            </div>
            <div class="form-group">
              <label for="new_client_email">Email</label>
              <input
                id="new_client_email"
                v-model="newClient.email"
                type="email"
                placeholder="email@exemplo.com"
              />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="new_client_phone">Telefone</label>
              <input
                id="new_client_phone"
                v-model="newClient.phone"
                type="text"
                placeholder="(11) 99999-9999"
              />
            </div>
            <div class="form-group">
              <label for="new_client_address">Endereço</label>
              <input
                id="new_client_address"
                v-model="newClient.address"
                type="text"
                placeholder="Endereço completo"
              />
            </div>
          </div>
          <button type="button" @click="createClient" class="btn btn-primary">
            Criar Cliente
          </button>
        </div>
        
        <!-- Formulário de Novo Equipamento -->
        <div v-if="showNewEquipmentForm" class="form-section new-equipment-form">
          <h3>Novo Equipamento</h3>
          <div class="form-row">
            <div class="form-group">
              <label for="new_equipment_type">Tipo *</label>
              <input
                id="new_equipment_type"
                v-model="newEquipment.type"
                type="text"
                required
                placeholder="Ex: Notebook, Desktop, Servidor"
              />
            </div>
            <div class="form-group">
              <label for="new_equipment_brand">Marca</label>
              <input
                id="new_equipment_brand"
                v-model="newEquipment.brand"
                type="text"
                placeholder="Ex: Dell, HP, Lenovo"
              />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="new_equipment_model">Modelo</label>
              <input
                id="new_equipment_model"
                v-model="newEquipment.model"
                type="text"
                placeholder="Ex: Inspiron 15, ThinkPad X1"
              />
            </div>
            <div class="form-group">
              <label for="new_equipment_serial">Número de Série</label>
              <input
                id="new_equipment_serial"
                v-model="newEquipment.serial_number"
                type="text"
                placeholder="Número de série do equipamento"
              />
            </div>
          </div>
          <button type="button" @click="createEquipment" class="btn btn-primary">
            Criar Equipamento
          </button>
        </div>
        
        <div v-if="submitError" class="error-message">
          {{ submitError }}
        </div>
        
        <div class="form-actions">
          <button 
            type="button"
            @click="resetForm"
            class="btn btn-secondary"
            :disabled="loading"
          >
            Limpar
          </button>
          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="loading || !isFormValid"
          >
            <span v-if="loading">Criando...</span>
            <span v-else>Criar Ordem de Serviço</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import axios from 'axios'

export default {
  name: 'AddOrder',
  data() {
    return {
      loading: false,
      submitError: null,
      showNewClientForm: false,
      showNewEquipmentForm: false,
      clients: [],
      equipments: [],
      technicians: [],
      form: {
        title: '',
        description: '',
        status: 'open',
        client_id: '',
        equipment_id: '',
        technician_id: ''
      },
      newClient: {
        name: '',
        email: '',
        phone: '',
        address: ''
      },
      newEquipment: {
        type: '',
        brand: '',
        model: '',
        serial_number: ''
      }
    }
  },
  computed: {
    isFormValid() {
      return this.form.title && 
             this.form.client_id && 
             this.form.equipment_id &&
             this.form.technician_id
    }
  },
  mounted() {
    this.loadClients()
    this.loadTechnicians()
  },
  methods: {
    ...mapActions('auth', ['logout']),
    
    async loadClients() {
      try {
        const response = await axios.get('http://localhost:8000/orders/clients/')
        this.clients = response.data
      } catch (error) {
        console.error('Erro ao carregar clientes:', error)
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
    
    async loadClientEquipments() {
      if (!this.form.client_id) {
        this.equipments = []
        this.form.equipment_id = ''
        return
      }
      
      try {
        const response = await axios.get(`http://localhost:8000/orders/equipments/?client_id=${this.form.client_id}`)
        this.equipments = response.data
        this.form.equipment_id = '' // Reset equipment selection
      } catch (error) {
        console.error('Erro ao carregar equipamentos:', error)
        this.equipments = []
      }
    },
    
    async createClient() {
      if (!this.newClient.name) {
        alert('Nome do cliente é obrigatório')
        return
      }
      
      try {
        const response = await axios.post('http://localhost:8000/orders/clients/', this.newClient)
        this.clients.push(response.data)
        this.form.client_id = response.data.id
        this.showNewClientForm = false
        this.newClient = { name: '', email: '', phone: '', address: '' }
      } catch (error) {
        alert('Erro ao criar cliente: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    async createEquipment() {
      if (!this.newEquipment.type) {
        alert('Tipo do equipamento é obrigatório')
        return
      }
      
      if (!this.form.client_id) {
        alert('Selecione um cliente primeiro')
        return
      }
      
      try {
        const equipmentData = {
          ...this.newEquipment,
          client_id: this.form.client_id
        }
        
        const response = await axios.post('http://localhost:8000/orders/equipments/', equipmentData)
        this.equipments.push(response.data)
        this.form.equipment_id = response.data.id
        this.showNewEquipmentForm = false
        this.newEquipment = { type: '', brand: '', model: '', serial_number: '' }
      } catch (error) {
        alert('Erro ao criar equipamento: ' + (error.response?.data?.detail || error.message))
      }
    },
    
    getEquipmentDescription(equipment) {
      let description = equipment.type
      if (equipment.brand) description += ` ${equipment.brand}`
      if (equipment.model) description += ` ${equipment.model}`
      if (equipment.serial_number) description += ` (SN: ${equipment.serial_number})`
      return description
    },
    
    async handleSubmit() {
      this.loading = true
      this.submitError = null
      
      try {
        // Preparar dados para envio (remover technician_id do form principal)
        const orderData = {
          title: this.form.title,
          description: this.form.description,
          status: this.form.status,
          client_id: this.form.client_id,
          equipment_id: this.form.equipment_id
        }
        
        const response = await axios.post('http://localhost:8000/orders/', orderData)
        
        // Após criar a ordem, atribuir o técnico
        if (this.form.technician_id && response.data.id) {
          await axios.put(`http://localhost:8000/orders/${response.data.id}/assign-technician?technician_id=${this.form.technician_id}`)
        }
        
        // Sucesso - redirecionar para lista de ordens
        this.$router.push('/orders')
        
      } catch (error) {
        if (error.response?.status === 401) {
          await this.logout()
          this.$router.push('/login')
          return
        }
        
        this.submitError = error.response?.data?.detail || 'Erro ao criar ordem de serviço'
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
      this.submitError = null
      this.showNewClientForm = false
      this.showNewEquipmentForm = false
    }
  }
}
</script>

<style scoped>
.add-order {
  max-width: 800px;
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

.form-container {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.order-form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  border: 1px solid #e1e5e9;
  border-radius: 8px;
  padding: 1.5rem;
}

.form-section h3 {
  margin: 0 0 1.5rem 0;
  color: #333;
  border-bottom: 2px solid #667eea;
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
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
}

.form-group input:disabled,
.form-group select:disabled,
.form-group textarea:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-help {
  color: #666;
  font-size: 0.85rem;
  margin-top: 0.25rem;
  display: block;
}

.btn-sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

.btn-outline {
  background: transparent;
  border: 2px solid #667eea;
  color: #667eea;
}

.btn-outline:hover {
  background: #667eea;
  color: white;
}

.new-client-form,
.new-equipment-form {
  background-color: #f8f9fa;
  border: 2px solid #667eea;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #fcc;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 1rem;
  border-top: 1px solid #e1e5e9;
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
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
}
</style>
