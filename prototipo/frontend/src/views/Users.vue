<template>
  <div class="users">
    <div class="header">
      <h1>👥 Gestão de Usuários</h1>
      <div class="header-actions">
        <router-link to="/users/add" class="btn btn-success">+ Adicionar Usuário</router-link>
        <button @click="loadUsers" class="btn btn-primary">Atualizar</button>
      </div>
    </div>
    
    <div v-if="loading" class="loading">
      <p>Carregando usuários...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>Erro ao carregar usuários: {{ error }}</p>
    </div>
    
    <div v-else>
      <UsersList
        :users="users"
        :current-user-id="currentUser?.id"
        @edit="editUser"
        @delete="confirmDeleteUser"
      />
    </div>
    
    <!-- Modal de Edição de Usuário -->
    <UserEditModal
      :show="showEditModal"
      :user="selectedUser"
      :loading="updating"
      @close="closeEditModal"
      @update="updateUser"
    />
    
    <!-- Modal de Confirmação de Exclusão -->
    <UserDeleteModal
      :show="showDeleteModal"
      :user="userToDelete"
      :loading="deleting"
      @close="closeDeleteModal"
      @delete="deleteUser"
    />
  </div>
</template>

<script>
import api from '../api/axios'
import { mapState } from 'vuex'
import UsersList from '../components/UsersComponents/UsersList.vue'
import UserEditModal from '../components/UsersComponents/UserEditModal.vue'
import UserDeleteModal from '../components/UsersComponents/UserDeleteModal.vue'

export default {
  name: 'Users',
  components: {
    UsersList,
    UserEditModal,
    UserDeleteModal
  },
  data() {
    return {
      users: [],
      loading: false,
      error: null,
      showEditModal: false,
      showDeleteModal: false,
      selectedUser: null,
      userToDelete: null,
      updating: false,
      deleting: false
    }
  },
  computed: {
    ...mapState('auth', ['user']),
    currentUser() {
      return this.user
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
        const response = await api.get('/users/')
        this.users = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || error.message
        console.error('Erro ao carregar usuários:', error)
      } finally {
        this.loading = false
      }
    },
    
    editUser(user) {
      this.selectedUser = user
      this.showEditModal = true
    },
    
    closeEditModal() {
      this.showEditModal = false
      this.selectedUser = null
    },
    
    async updateUser(updateData) {
      if (!this.selectedUser) return
      
      this.updating = true
      
      try {
        await api.put(`/users/${this.selectedUser.id}`, updateData)
        
        // Recarregar lista de usuários
        await this.loadUsers()
        
        // Fechar modal
        this.closeEditModal()
        
        // Feedback de sucesso
        alert('Usuário atualizado com sucesso!')
        
      } catch (error) {
        alert('Erro ao atualizar usuário: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.updating = false
      }
    },
    
    confirmDeleteUser(user) {
      this.userToDelete = user
      this.showDeleteModal = true
    },
    
    closeDeleteModal() {
      this.showDeleteModal = false
      this.userToDelete = null
    },
    
    async deleteUser(user) {
      if (!user) return
      
      this.deleting = true
      
      try {
        await api.delete(`/users/${user.id}`)
        
        // Recarregar lista de usuários
        await this.loadUsers()
        
        // Fechar modal
        this.closeDeleteModal()
        
        // Feedback de sucesso
        alert('Usuário excluído com sucesso!')
        
      } catch (error) {
        alert('Erro ao excluir usuário: ' + (error.response?.data?.detail || error.message))
      } finally {
        this.deleting = false
      }
    }
  }
}
</script>

<style scoped>
.users {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h1 {
  color: #333;
  margin: 0;
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
