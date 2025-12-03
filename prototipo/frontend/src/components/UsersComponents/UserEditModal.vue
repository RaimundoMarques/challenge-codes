<template>
  <div v-if="show" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>Editar Usuário</h3>
        <button @click="closeModal" class="close-btn">&times;</button>
      </div>
      
      <div class="modal-body">
        <form @submit.prevent="handleSubmit">
          <div class="form-row">
            <div class="form-group">
              <label for="edit_username">Username *</label>
              <input
                id="edit_username"
                v-model="form.username"
                type="text"
                required
                :disabled="loading"
              />
            </div>
            
            <div class="form-group">
              <label for="edit_name">Nome Completo</label>
              <input
                id="edit_name"
                v-model="form.name"
                type="text"
                :disabled="loading"
              />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="edit_email">Email</label>
              <input
                id="edit_email"
                v-model="form.email"
                type="email"
                :disabled="loading"
              />
            </div>
            
            <div class="form-group">
              <label for="edit_role">Função</label>
              <select
                id="edit_role"
                v-model="form.role"
                :disabled="loading"
              >
                <option value="tecnico">Técnico</option>
                <option value="administrador">Administrador</option>
              </select>
            </div>
          </div>
          
          <div class="form-group">
            <label for="edit_password">Nova Senha (deixe em branco para manter a atual)</label>
            <input
              id="edit_password"
              v-model="form.password"
              type="password"
              :disabled="loading"
              placeholder="Digite uma nova senha"
            />
          </div>
          
          <div class="form-group">
            <label class="checkbox-label">
              <input
                type="checkbox"
                v-model="form.is_active"
                :disabled="loading"
              />
              Usuário ativo
            </label>
          </div>
        </form>
      </div>
      
      <div class="modal-footer">
        <button @click="closeModal" class="btn btn-secondary" :disabled="loading">
          Cancelar
        </button>
        <button 
          type="submit" 
          @click="handleSubmit"
          class="btn btn-primary"
          :disabled="loading || !form.username.trim()"
        >
          <span v-if="loading">Salvando...</span>
          <span v-else>Salvar Alterações</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserEditModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    user: {
      type: Object,
      default: null
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      form: {
        username: '',
        name: '',
        email: '',
        role: 'tecnico',
        password: '',
        is_active: true
      }
    }
  },
  watch: {
    user: {
      handler(newUser) {
        if (newUser) {
          this.form = {
            username: newUser.username || '',
            name: newUser.name || '',
            email: newUser.email || '',
            role: newUser.role || 'tecnico',
            password: '',
            is_active: newUser.is_active !== false
          }
        }
      },
      immediate: true
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    
    handleSubmit() {
      if (!this.form.username.trim()) return
      
      const updateData = { ...this.form }
      if (!updateData.password.trim()) {
        delete updateData.password
      }
      
      this.$emit('update', updateData)
    }
  }
}
</script>

<style scoped>
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
  transition: border-color 0.3s, box-shadow 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.form-group input:disabled,
.form-group select:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin: 0;
  cursor: pointer;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
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
  
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
}
</style>
