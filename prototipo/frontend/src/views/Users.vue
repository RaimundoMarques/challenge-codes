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
    
    <div v-else class="users-list">
      <div v-if="users.length === 0" class="empty">
        <p>Nenhum usuário encontrado</p>
      </div>
      
      <div v-else>
        <div class="user-card" v-for="user in users" :key="user.id">
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
              @click="editUser(user)"
              class="btn btn-sm btn-primary"
              title="Editar usuário"
            >
              ✏️
            </button>
            <button 
              @click="confirmDeleteUser(user)"
              class="btn btn-sm btn-danger"
              title="Excluir usuário"
              :disabled="user.id === currentUser?.id"
            >
              🗑️
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal de Edição de Usuário -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Editar Usuário</h3>
          <button @click="closeEditModal" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="updateUser">
            <div class="form-row">
              <div class="form-group">
                <label for="edit_username">Username *</label>
                <input
                  id="edit_username"
                  v-model="editForm.username"
                  type="text"
                  required
                  :disabled="updating"
                />
              </div>
              
              <div class="form-group">
                <label for="edit_name">Nome Completo</label>
                <input
                  id="edit_name"
                  v-model="editForm.name"
                  type="text"
                  :disabled="updating"
                />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="edit_email">Email</label>
                <input
                  id="edit_email"
                  v-model="editForm.email"
                  type="email"
                  :disabled="updating"
                />
              </div>
              
              <div class="form-group">
                <label for="edit_role">Função *</label>
                <select
                  id="edit_role"
                  v-model="editForm.role"
                  required
                  :disabled="updating"
                >
                  <option value="tecnico">Técnico</option>
                  <option value="administrador">Administrador</option>
                </select>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="edit_password">Nova Senha (deixe em branco para manter)</label>
                <input
                  id="edit_password"
                  v-model="editForm.password"
                  type="password"
                  :disabled="updating"
                />
              </div>
              
              <div class="form-group">
                <label class="checkbox-label">
                  <input
                    type="checkbox"
                    v-model="editForm.is_active"
                    :disabled="updating"
                  />
                  Usuário ativo
                </label>
              </div>
            </div>
            
            <div v-if="updateError" class="error-message">
              {{ updateError }}
            </div>
            
            <div class="modal-footer">
              <button @click="closeEditModal" class="btn btn-secondary" :disabled="updating">
                Cancelar
              </button>
              <button type="submit" class="btn btn-primary" :disabled="updating">
                <span v-if="updating">Salvando...</span>
                <span v-else>Salvar</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- Modal de Confirmação de Exclusão -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Confirmar Exclusão</h3>
          <button @click="closeDeleteModal" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="warning-message">
            <p>⚠️ <strong>Atenção!</strong> Esta ação não pode ser desfeita.</p>
            <p>Tem certeza que deseja excluir o usuário:</p>
            <div class="user-to-delete" v-if="userToDelete">
              <strong>{{ userToDelete.name || userToDelete.username }}</strong>
              <span class="user-role">({{ userToDelete.role }})</span>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="closeDeleteModal" class="btn btn-secondary" :disabled="deleting">
            Cancelar
          </button>
          <button @click="deleteUser" class="btn btn-danger" :disabled="deleting">
            <span v-if="deleting">Excluindo...</span>
            <span v-else>Sim, Excluir</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  name: 'Users',
  data() {
    return {
      users: [],
      loading: false,
      error: null,
      showEditModal: false,
      showDeleteModal: false,
      updating: false,
      deleting: false,
      updateError: null,
      editForm: {
        username: '',
        name: '',
        email: '',
        role: '',
        password: '',
        is_active: true
      },
      userToDelete: null,
      currentEditingUser: null
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
        const response = await axios.get('http://localhost:8000/users/')
        this.users = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || error.message
        console.error('Erro ao carregar usuários:', error)
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'Não informado'
      const date = new Date(dateString)
      return date.toLocaleDateString('pt-BR')
    },
    
    editUser(user) {
      this.currentEditingUser = user
      this.editForm = {
        username: user.username,
        name: user.name || '',
        email: user.email || '',
        role: user.role,
        password: '',
        is_active: user.is_active
      }
      this.showEditModal = true
      this.updateError = null
    },
    
    closeEditModal() {
      this.showEditModal = false
      this.currentEditingUser = null
      this.editForm = {
        username: '',
        name: '',
        email: '',
        role: '',
        password: '',
        is_active: true
      }
      this.updateError = null
    },
    
    async updateUser() {
      if (!this.currentEditingUser) return
      
      this.updating = true
      this.updateError = null
      
      try {
        // Preparar dados para envio
        const updateData = {
          username: this.editForm.username,
          name: this.editForm.name,
          email: this.editForm.email,
          role: this.editForm.role,
          is_active: this.editForm.is_active
        }
        
        // Incluir senha apenas se foi preenchida
        if (this.editForm.password) {
          updateData.password = this.editForm.password
        }
        
        await axios.put(`http://localhost:8000/users/${this.currentEditingUser.id}`, updateData)
        
        // Recarregar lista de usuários
        await this.loadUsers()
        
        // Fechar modal
        this.closeEditModal()
        
        // Feedback de sucesso
        alert('Usuário atualizado com sucesso!')
        
      } catch (error) {
        this.updateError = error.response?.data?.detail || 'Erro ao atualizar usuário'
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
    
    async deleteUser() {
      if (!this.userToDelete) return
      
      this.deleting = true
      
      try {
        await axios.delete(`http://localhost:8000/users/${this.userToDelete.id}`)
        
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

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
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

.btn-success {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  text-decoration: none;
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
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
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
  align-items: flex-start;
  margin-bottom: 1rem;
}

.user-header h3 {
  color: #333;
  margin: 0;
}

.user-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: flex-end;
}

.role-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
}

.role-tecnico {
  background-color: #e3f2fd;
  color: #1976d2;
}

.role-administrador {
  background-color: #fff3e0;
  color: #f57c00;
}

.user-details p {
  margin-bottom: 0.5rem;
  color: #666;
}

.user-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-left: 1rem;
}

.btn-sm {
  padding: 0.5rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: opacity 0.3s;
  font-size: 1rem;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-danger {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
}

.btn-danger:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.status-active {
  color: #27ae60;
  font-weight: bold;
}

.status-inactive {
  color: #e74c3c;
  font-weight: bold;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 10px;
  padding: 0;
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e1e5e9;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
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
.form-group select {
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

.form-group input:disabled,
.form-group select:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.checkbox-label {
  display: flex !important;
  flex-direction: row !important;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin: 0;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid #fcc;
  margin-bottom: 1rem;
}

.warning-message {
  background-color: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 1.5rem;
  color: #856404;
}

.warning-message p {
  margin: 0.5rem 0;
}

.user-to-delete {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  text-align: center;
}

.user-role {
  color: #666;
  font-weight: normal;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e1e5e9;
}

@media (max-width: 768px) {
  .user-card {
    flex-direction: column;
  }
  
  .user-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .user-meta {
    flex-direction: row;
    align-items: center;
    margin-top: 0.5rem;
  }
  
  .user-actions {
    flex-direction: row;
    margin-left: 0;
    margin-top: 1rem;
    justify-content: flex-end;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
}
</style>
