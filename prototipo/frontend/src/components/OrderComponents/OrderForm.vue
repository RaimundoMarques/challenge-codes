<template>
  <div class="form-section">
    <h3>Informações Básicas</h3>
    
    <div class="form-row">
      <div class="form-group">
        <label for="title">Título da OS *</label>
        <input
          id="title"
          v-model="form.title"
          type="text"
          required
          :disabled="loading"
          placeholder="Ex: Manutenção preventiva notebook"
        />
      </div>
      
      <div class="form-group">
        <label for="status">Status</label>
        <select
          id="status"
          v-model="form.status"
          :disabled="loading"
        >
          <option value="open">Aberta</option>
          <option value="in_progress">Em Andamento</option>
          <option value="closed">Fechada</option>
        </select>
      </div>
    </div>
    
    <div class="form-group">
      <label for="description">Descrição</label>
      <textarea
        id="description"
        v-model="form.description"
        :disabled="loading"
        placeholder="Descreva os detalhes da ordem de serviço..."
        rows="4"
      ></textarea>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderForm',
  props: {
    form: {
      type: Object,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.form-section {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-section h3 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 600;
  font-size: 0.95rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
  width: 100%;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.form-group input:disabled,
.form-group select:disabled,
.form-group textarea:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style>
