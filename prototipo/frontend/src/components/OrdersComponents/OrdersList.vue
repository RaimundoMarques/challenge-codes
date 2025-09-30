<template>
  <div class="orders-list">
    <div v-if="orders.length === 0" class="empty">
      <p>Nenhuma ordem de serviço encontrada</p>
    </div>
    
    <div v-else>
      <OrderCard 
        v-for="order in orders" 
        :key="order.id"
        :order="order"
        @reassign="$emit('reassign', $event)"
      />
    </div>
  </div>
</template>

<script>
import OrderCard from './OrderCard.vue'

export default {
  name: 'OrdersList',
  components: {
    OrderCard
  },
  props: {
    orders: {
      type: Array,
      required: true
    }
  },
  emits: ['reassign']
}
</script>

<style scoped>
.orders-list {
  display: grid;
  gap: 1rem;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>
