<template>
  <div class="home">
    <div class="hero">
      <h1>Bem-vindo ao Sistema de Ordens de Serviço</h1>
      <p>Gerencie suas ordens de serviço de forma eficiente e organizada</p>
    </div>
    
    <div class="features">
      <div class="feature-card">
        <div class="feature-icon">👥</div>
        <h3>Gestão de Usuários</h3>
        <p>Gerencie usuários do sistema com facilidade</p>
        <router-link to="/users" class="btn">Ver Usuários</router-link>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">📋</div>
        <h3>Ordens de Serviço</h3>
        <p>Crie e acompanhe ordens de serviço</p>
        <router-link to="/orders" class="btn">Ver Ordens</router-link>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Relatórios</h3>
        <p>Acompanhe métricas e relatórios</p>
        <button class="btn" disabled>Em breve</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
/* .home {
  text-align: center;
} */

.hero {
  margin-bottom: 3rem;
}

.hero h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1.2rem;
  color: #666;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #333;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  margin-bottom: 1.5rem;
}

.btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: opacity 0.3s;
}

.btn:hover {
  opacity: 0.9;
}

.btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
