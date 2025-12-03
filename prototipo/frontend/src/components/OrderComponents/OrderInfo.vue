<template>
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
</template>

<script>
export default {
  name: 'OrderInfo',
  props: {
    order: {
      type: Object,
      required: true
    }
  },
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
.info-section {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.info-section h2 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item label {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
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

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
