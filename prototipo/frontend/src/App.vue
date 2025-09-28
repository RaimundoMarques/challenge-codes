<template>
  <div id="app">
    <!-- Navbar apenas para usuários autenticados -->
    <nav v-if="isAuthenticated" class="navbar">
      <div class="navbar-brand">
        <h1>🛠️ Sistema de Ordens de Serviço</h1>
      </div>
      <div class="navbar-menu">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/users" class="nav-link">Usuários</router-link>
        <router-link to="/orders" class="nav-link">Ordens de Serviço</router-link>
      </div>
      <div class="navbar-user">
        <div class="user-info">
          <span class="user-name">{{ user?.name || user?.username }}</span>
          <span class="user-role">{{ user?.role }}</span>
        </div>
        <button @click="handleLogout" class="logout-button">
          Sair
        </button>
      </div>
    </nav>
    
    <main class="main-content" :class="{ 'no-navbar': !isAuthenticated }">
      <router-view />
    </main>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'App',
  computed: {
    ...mapState('auth', ['isAuthenticated', 'user'])
  },
  methods: {
    ...mapActions('auth', ['logout']),
    
    async handleLogout() {
      await this.logout()
      this.$router.push('/login')
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
}

.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.navbar-brand h1 {
  font-size: 1.5rem;
  font-weight: 600;
}

.navbar-menu {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.navbar-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.user-name {
  font-weight: 600;
  font-size: 0.9rem;
}

.user-role {
  font-size: 0.8rem;
  opacity: 0.8;
  text-transform: capitalize;
}

.logout-button {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.main-content.no-navbar {
  padding-top: 2rem;
}
</style>
