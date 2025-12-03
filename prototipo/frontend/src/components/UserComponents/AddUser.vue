<template>
  <div class="add-user">
    <div class="header">
      <h1>👥 Adicionar Novo Usuário</h1>
      <router-link to="/users" class="btn btn-secondary">Voltar</router-link>
    </div>
    
    <div class="form-container">
      <form @submit.prevent="handleSubmit" class="user-form">
        <div class="form-row">
          <div class="form-group">
            <label for="username">Username *</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              :disabled="loading"
              placeholder="Digite o username"
              @blur="validateUsername"
            />
            <span v-if="errors.username" class="error-text">{{ errors.username }}</span>
          </div>
          
          <div class="form-group">
            <label for="password">Senha *</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              :disabled="loading"
              placeholder="Digite a senha"
              @blur="validatePassword"
            />
            <span v-if="errors.password" class="error-text">{{ errors.password }}</span>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="name">Nome Completo</label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              :disabled="loading"
              placeholder="Digite o nome completo"
            />
          </div>
          
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              :disabled="loading"
              placeholder="Digite o email"
              @blur="validateEmail"
            />
            <span v-if="errors.email" class="error-text">{{ errors.email }}</span>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="role">Função *</label>
            <select
              id="role"
              v-model="form.role"
              required
              :disabled="loading"
            >
              <option value="">Selecione uma função</option>
              <option value="tecnico">Técnico</option>
              <option value="administrador">Administrador</option>
            </select>
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
            <span v-else>Criar Usuário</span>
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
  name: 'AddUser',
  data() {
    return {
      loading: false,
      submitError: null,
      form: {
        username: '',
        password: '',
        name: '',
        email: '',
        role: '',
        is_active: true
      },
      errors: {}
    }
  },
  computed: {
    isFormValid() {
      return this.form.username && 
             this.form.password && 
             this.form.role && 
             Object.keys(this.errors).length === 0
    }
  },
  methods: {
    ...mapActions('auth', ['logout']),
    
    validateUsername() {
      if (!this.form.username) {
        this.errors.username = 'Username é obrigatório'
        return
      }
      
      if (this.form.username.length < 3) {
        this.errors.username = 'Username deve ter pelo menos 3 caracteres'
        return
      }
      
      // Verificar caracteres válidos
      if (!/^[a-zA-Z0-9_]+$/.test(this.form.username)) {
        this.errors.username = 'Username deve conter apenas letras, números e _'
        return
      }
      
      delete this.errors.username
    },
    
    validatePassword() {
      if (!this.form.password) {
        this.errors.password = 'Senha é obrigatória'
        return
      }
      
      if (this.form.password.length < 6) {
        this.errors.password = 'Senha deve ter pelo menos 6 caracteres'
        return
      }
      
      delete this.errors.password
    },
    
    validateEmail() {
      if (this.form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.form.email)) {
        this.errors.email = 'Email inválido'
        return
      }
      
      delete this.errors.email
    },
    
    async handleSubmit() {
      // Validar formulário antes de enviar
      this.validateUsername()
      this.validatePassword()
      this.validateEmail()
      
      if (!this.isFormValid) {
        this.submitError = 'Por favor, corrija os erros no formulário'
        return
      }
      
      this.loading = true
      this.submitError = null
      
      try {
        const response = await axios.post('http://localhost:8000/users/', this.form)
        
        // Sucesso - redirecionar para lista de usuários
        this.$router.push('/users')
        
        // Mostrar mensagem de sucesso (opcional)
        this.$emit('user-created', response.data)
        
      } catch (error) {
        if (error.response?.status === 401) {
          // Token expirado - fazer logout
          await this.logout()
          this.$router.push('/login')
          return
        }
        
        if (error.response?.status === 403) {
          this.submitError = 'Você não tem permissão para criar usuários'
          return
        }
        
        this.submitError = error.response?.data?.detail || 'Erro ao criar usuário'
      } finally {
        this.loading = false
      }
    },
    
    resetForm() {
      this.form = {
        username: '',
        password: '',
        name: '',
        email: '',
        role: '',
        is_active: true
      }
      this.errors = {}
      this.submitError = null
    }
  }
}
</script>

<style scoped>
.add-user {
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

.user-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
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

.error-text {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 0.25rem;
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
