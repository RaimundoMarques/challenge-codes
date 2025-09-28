<template>
  <div class="users">
    <div class="header">
      <h1>👥 Gestão de Usuários</h1>
      <button @click="loadUsers" class="btn btn-primary">Atualizar</button>
    </div>
    
    <div v-if="loading" class="loading">
      <p>Carregando usuários...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>Erro ao carregar usuários: {{ error }}</p>
    </div>
    
    <div v-else class="users-list">
      <div v-if="users.length === 0" class="empty">
        <p>Nenhum usuário encontrado</p>
      </div>
      
      <div v-else>
        <div class="user-card" v-for="user in users" :key="user.id">
          <div class="user-info">
            <h3>{{ user.name || user.username }}</h3>
            <p><strong>Username:</strong> {{ user.username }}</p>
            <p><strong>Email:</strong> {{ user.email || 'Não informado' }}</p>
            <p><strong>Status:</strong> 
              <span :class="user.is_active ? 'status-active' : 'status-inactive'">
                {{ user.is_active ? 'Ativo' : 'Inativo' }}
              </span>
            </p>
            <p><strong>Criado em:</strong> {{ formatDate(user.created_at) }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Users',
  data() {
    return {
      users: [],
      loading: false,
      error: null
    }
  },
  mounted() {
    this.loadUsers()
  },
  methods: {
    async loadUsers() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('http://localhost:8000/users/')
        this.users = response.data
      } catch (error) {
        this.error = error.message
        console.error('Erro ao carregar usuários:', error)
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'Não informado'
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR')
    }
  }
}
</script>

<style scoped>
.users {
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

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn:hover {
  opacity: 0.9;
}

.loading, .error, .empty {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.error {
  color: #e74c3c;
}

.users-list {
  display: grid;
  gap: 1rem;
}

.user-card {
  background: white;
  padding: 1.5rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.user-card:hover {
  transform: translateY(-2px);
}

.user-info h3 {
  color: #333;
  margin-bottom: 0.5rem;
}

.user-info p {
  margin-bottom: 0.5rem;
  color: #666;
}

.status-active {
  color: #27ae60;
  font-weight: bold;
}

.status-inactive {
  color: #e74c3c;
  font-weight: bold;
}
</style>
