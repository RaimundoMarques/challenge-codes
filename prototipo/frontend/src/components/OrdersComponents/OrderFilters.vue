<template>
  <div class="filters">
    <div class="filter-group">
      <label for="status-filter">Status:</label>
      <select 
        id="status-filter" 
        v-model="localFilters.status" 
        @change="applyFilters"
      >
        <option value="">Todos</option>
        <option value="open">Abertas</option>
        <option value="in_progress">Em Andamento</option>
        <option value="closed">Fechadas</option>
      </select>
    </div>
    
    <div class="filter-group">
      <label for="user-filter">Técnico:</label>
      <select 
        id="user-filter" 
        v-model="localFilters.user_id" 
        @change="applyFilters"
      >
        <option value="">Todos</option>
        <option v-for="user in users" :key="user.id" :value="user.id">
          {{ user.name || user.username }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderFilters',
  props: {
    filters: {
      type: Object,
      required: true
    },
    users: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      localFilters: { ...this.filters }
    }
  },
  watch: {
    filters: {
      handler(newFilters) {
        this.localFilters = { ...newFilters }
      },
      deep: true
    }
  },
  methods: {
    applyFilters() {
      this.$emit('filters-changed', this.localFilters)
    }
  }
}
</script>

<style scoped>
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

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
    gap: 1rem;
  }
  
  .filter-group {
    min-width: auto;
  }
}
</style>
