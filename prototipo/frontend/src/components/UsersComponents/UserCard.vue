<template>
  <div class="user-card">
    <div class="user-info">
      <div class="user-header">
        <h3>{{ user.name || user.username }}</h3>
        <div class="user-meta">
          <span :class="['role-badge', `role-${user.role}`]">
            {{ user.role }}
          </span>
          <span :class="user.is_active ? 'status-active' : 'status-inactive'">
            {{ user.is_active ? 'Ativo' : 'Inativo' }}
          </span>
        </div>
      </div>
      <div class="user-details">
        <p><strong>Username:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email || 'Não informado' }}</p>
        <p><strong>Criado em:</strong> {{ formatDate(user.created_at) }}</p>
      </div>
    </div>
    <div class="user-actions">
      <button 
        @click="$emit('edit', user)"
        class="btn btn-sm btn-primary"
        title="Editar usuário"
      >
        ✏️
      </button>
      <button 
        @click="$emit('delete', user)"
        class="btn btn-sm btn-danger"
        title="Excluir usuário"
        :disabled="user.id === currentUserId"
      >
        🗑️
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserCard',
  props: {
    user: {
      type: Object,
      required: true
    },
    currentUserId: {
      type: [String, Number],
      default: null
    }
  },
  emits: ['edit', 'delete'],
  methods: {
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR') + ' ' + date.toLocaleTimeString('pt-BR')
    }
  }
}
</script>

<style scoped>
.user-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.3s;
}

.user-card:hover {
  transform: translateY(-2px);
}

.user-info {
  flex: 1;
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.user-header h3 {
  color: #333;
  margin: 0;
  font-size: 1.2rem;
}

.user-meta {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  display: inline-block;
}

.role-administrador {
  background-color: #ff6b6b;
  color: white;
}

.role-tecnico {
  background-color: #4ecdc4;
  color: white;
}

.status-active {
  color: #28a745;
  font-weight: 600;
  font-size: 0.9rem;
}

.status-inactive {
  color: #dc3545;
  font-weight: 600;
  font-size: 0.9rem;
}

.user-details {
  color: #666;
}

.user-details p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}

.user-details strong {
  color: #333;
}

.user-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: 1rem;
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

.btn-danger {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
}

.btn:hover:not(:disabled) {
  opacity: 0.9;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .user-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .user-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .user-actions {
    margin-left: 0;
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
