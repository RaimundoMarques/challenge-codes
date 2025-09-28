import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Users from '../views/Users.vue'
import Orders from '../views/Orders.vue'
import Login from '../components/Login.vue'
import AddUser from '../components/AddUser.vue'
import AddOrder from '../components/AddOrder.vue'
import store from '../store'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    name: 'Users',
    component: Users,
    meta: { requiresAuth: true }
  },
  {
    path: '/users/add',
    name: 'AddUser',
    component: AddUser,
    meta: { requiresAuth: true }
  },
  {
    path: '/orders',
    name: 'Orders',
    component: Orders,
    meta: { requiresAuth: true }
  },
  {
    path: '/orders/add',
    name: 'AddOrder',
    component: AddOrder,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de navegação para autenticação
router.beforeEach(async (to, from, next) => {
  // Verificar se o usuário está autenticado
  const isAuthenticated = await store.dispatch('auth/checkAuth')
  
  // Se a rota requer autenticação e o usuário não está autenticado
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }
  
  // Se a rota é apenas para visitantes (como login) e o usuário está autenticado
  if (to.meta.requiresGuest && isAuthenticated) {
    next('/')
    return
  }
  
  next()
})

export default router
