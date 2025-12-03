<template>
  <div class="order-card">
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
          @click="$emit('reassign', order)"
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
</template>

<script>
export default {
  name: 'OrderCard',
  props: {
    order: {
      type: Object,
      required: true
    }
  },
  emits: ['reassign'],
  methods: {
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

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn:hover {
  opacity: 0.9;
}

@media (max-width: 768px) {
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
}
</style>
