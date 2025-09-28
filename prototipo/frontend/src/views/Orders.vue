<template>
  <div class="orders">
    <div class="header">
      <h1>📋 Ordens de Serviço</h1>
      <button class="btn btn-primary" disabled>Nova Ordem (Em breve)</button>
    </div>
    
    <div class="info">
      <p>Funcionalidade de ordens de serviço será implementada em breve.</p>
      <p>Por enquanto, você pode gerenciar os usuários do sistema.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Orders'
}
</script>

<style scoped>
.orders {
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

.btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.info {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  color: #666;
}

.info p {
  margin-bottom: 1rem;
}
</style>
