# 🎨 Sistema de Ordens de Serviço - Frontend

## 📋 Visão Geral

Este é o frontend da aplicação de gerenciamento de ordens de serviço, construído com **Vue.js 3** e **Composition API**. O sistema oferece uma interface moderna e responsiva para gerenciar usuários, ordens de serviço, clientes, equipamentos e fotos de evidência.

## 🏗️ Arquitetura

### Tecnologias Utilizadas
- **Vue.js 3** - Framework JavaScript reativo
- **Vue Router** - Roteamento SPA
- **Vuex** - Gerenciamento de estado
- **Axios** - Cliente HTTP
- **CSS3** - Estilização moderna
- **Docker** - Containerização

### Estrutura do Projeto
```
frontend/
├── src/
│   ├── components/       # Componentes reutilizáveis
│   │   ├── LoginComponents/    # Componentes de autenticação
│   │   ├── OrderComponents/    # Componentes de ordens
│   │   ├── OrdersComponents/   # Componentes de lista de ordens
│   │   ├── PhotoComponents/    # Componentes de fotos
│   │   └── UserComponents/     # Componentes de usuários
│   ├── views/            # Páginas principais
│   ├── router/           # Configuração de rotas
│   ├── store/            # Gerenciamento de estado
│   └── App.vue           # Componente raiz
├── package.json          # Dependências Node.js
└── Dockerfile           # Configuração Docker
```

## 🔐 Sistema de Autenticação

### Fluxo de Login
1. **Formulário**: Username e senha
2. **Validação**: Dados obrigatórios
3. **Request**: POST para `/auth/login`
4. **Token**: Armazenamento no localStorage
5. **Redirecionamento**: Dashboard principal

### Gerenciamento de Estado
```javascript
// store/auth.js
state: {
  user: null,
  token: localStorage.getItem('token')
}

mutations: {
  SET_USER(state, user) {
    state.user = user
  },
  SET_TOKEN(state, token) {
    state.token = token
    localStorage.setItem('token', token)
  }
}
```

### Proteção de Rotas
```javascript
// router/index.js
router.beforeEach((to, from, next) => {
  const token = store.state.auth.token
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})
```

## 📱 Páginas Principais

### 🏠 Home (`/`)
- **Dashboard** com estatísticas
- **Resumo** de ordens recentes
- **Acesso rápido** às funcionalidades

### 👥 Usuários (`/users`)
- **Listagem** de todos os usuários
- **Filtros** por função e status
- **Ações**: Editar, excluir, criar
- **Modal** de edição inline

### 📋 Ordens de Serviço (`/orders`)
- **Listagem** de ordens com filtros
- **Cards** informativos por ordem
- **Reatribuição** de técnicos
- **Status** visual (aberta/em andamento/fechada)

### 📝 Detalhes da Ordem (`/orders/:id`)
- **Informações** completas da ordem
- **Atividades** descritivas
- **Checklist** interativo
- **Fotos** de evidência
- **Ações** de status

### ➕ Nova Ordem (`/orders/add`)
- **Formulário** completo
- **Seleção** de cliente/equipamento
- **Criação** inline de novos registros
- **Validação** em tempo real

## 🧩 Arquitetura de Componentes

### Organização Modular
```
components/
├── LoginComponents/      # 1 componente
│   └── Login.vue
├── OrderComponents/      # 11 componentes
│   ├── AddOrder.vue
│   ├── OrderForm.vue
│   ├── OrderInfo.vue
│   ├── OrderActions.vue
│   ├── ActivitiesSection.vue
│   ├── ChecklistSection.vue
│   ├── ClientForm.vue
│   ├── EquipmentForm.vue
│   ├── ClientEquipmentSelector.vue
│   └── TechnicianSelector.vue
├── OrdersComponents/     # 4 componentes
│   ├── OrderCard.vue
│   ├── OrderFilters.vue
│   ├── OrdersList.vue
│   └── ReassignModal.vue
├── PhotoComponents/      # 3 componentes
│   ├── PhotoUpload.vue
│   ├── PhotoGallery.vue
│   └── PhotoModal.vue
└── UserComponents/       # 4 componentes
    ├── UserCard.vue
    ├── UserEditModal.vue
    ├── UserDeleteModal.vue
    └── UsersList.vue
```

### Princípios de Design
- **Single Responsibility**: Cada componente tem uma função
- **Reusabilidade**: Componentes modulares
- **Props/Events**: Comunicação clara
- **Styling**: CSS scoped por componente

## 🎨 Sistema de Design

### Cores Principais
```css
:root {
  --primary: #667eea;
  --secondary: #764ba2;
  --success: #28a745;
  --warning: #ffc107;
  --danger: #e74c3c;
  --info: #17a2b8;
}
```

### Componentes Base
- **Botões**: Gradientes e estados
- **Cards**: Sombras e bordas
- **Modais**: Overlay e animações
- **Formulários**: Validação visual
- **Tabelas**: Responsivas

### Responsividade
```css
/* Mobile First */
@media (max-width: 768px) {
  .grid { grid-template-columns: 1fr; }
  .header { flex-direction: column; }
}
```

## 🔄 Gerenciamento de Estado

### Vuex Store
```javascript
// store/index.js
modules: {
  auth: {
    state: { user: null, token: null },
    mutations: { SET_USER, SET_TOKEN },
    actions: { login, logout, checkAuth }
  }
}
```

### Persistência
- **localStorage**: Token de autenticação
- **sessionStorage**: Dados temporários
- **Vuex**: Estado da aplicação

## 📡 Integração com API

### Cliente HTTP
```javascript
// Axios configuration
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para token
api.interceptors.request.use(config => {
  const token = store.state.auth.token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

### Tratamento de Erros
```javascript
// Error handling
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      store.dispatch('auth/logout')
      router.push('/login')
    }
    return Promise.reject(error)
  }
)
```

## 🖼️ Sistema de Upload de Fotos

### Funcionalidades
- **Drag & Drop**: Interface intuitiva
- **Preview**: Visualização antes do upload
- **Validação**: Tipos e tamanhos permitidos
- **Progress**: Barra de progresso
- **Gallery**: Galeria de fotos existentes

### Implementação
```javascript
// PhotoUpload.vue
methods: {
  async uploadPhotos(files) {
    const formData = new FormData()
    files.forEach(file => formData.append('file', file))
    
    await axios.post(`/orders/${orderId}/photos`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}
```

## 📋 Sistema de Checklist

### Funcionalidades
- **Seleção**: Checklist por ordem
- **Respostas**: Checkbox interativo
- **Persistência**: Salvar no backend
- **Validação**: Campos obrigatórios

### Implementação
```javascript
// ChecklistSection.vue
methods: {
  async saveChecklistResponses() {
    const responses = this.selectedChecklist.items.map(item => ({
      service_order_id: this.orderId,
      checklist_item_id: item.id,
      is_checked: this.getChecklistResponse(item.id)
    }))
    
    await axios.post(`/orders/${this.orderId}/checklist-responses/`, responses)
  }
}
```

## 🔧 Configuração e Instalação

### Variáveis de Ambiente
```env
# API Configuration
VUE_APP_API_URL=http://localhost:8000
VUE_APP_API_TIMEOUT=10000
```

### Instalação Local
```bash
# Instalar dependências
npm install

# Desenvolvimento
npm run serve

# Build para produção
npm run build
```

### Docker
```bash
# Build e execução
docker-compose up -d --build

# Logs
docker-compose logs -f frontend
```

## 📁 Estrutura de Arquivos

### Views (`src/views/`)
- `Home.vue` - Dashboard principal
- `Users.vue` - Gestão de usuários
- `Orders.vue` - Lista de ordens
- `OrderDetail.vue` - Detalhes da ordem

### Components (`src/components/`)
- **Organizados por funcionalidade**
- **Reutilizáveis e modulares**
- **Props e events bem definidos**

### Router (`src/router/`)
- **Rotas protegidas** com middleware
- **Lazy loading** de componentes
- **Navegação programática**

### Store (`src/store/`)
- **Módulos** por funcionalidade
- **Actions** assíncronas
- **Mutations** síncronas

## 🎯 Funcionalidades Principais

### Gestão de Usuários
- ✅ **CRUD completo** de usuários
- ✅ **Roles** (admin/tecnico)
- ✅ **Status** ativo/inativo
- ✅ **Validação** de dados

### Gestão de Ordens
- ✅ **Criação** de novas ordens
- ✅ **Atribuição** de técnicos
- ✅ **Status** (aberta/em andamento/fechada)
- ✅ **Filtros** avançados

### Sistema de Fotos
- ✅ **Upload** drag & drop
- ✅ **Galeria** de fotos
- ✅ **Modal** de visualização
- ✅ **Exclusão** de fotos

### Checklist
- ✅ **Seleção** de checklist
- ✅ **Respostas** interativas
- ✅ **Persistência** de dados
- ✅ **Validação** de campos

## 🚀 Deploy

### Produção
1. **Build**: `npm run build`
2. **Servidor**: Nginx/Apache
3. **SSL**: Certificados HTTPS
4. **CDN**: Assets estáticos

### Docker Production
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "serve"]
```

## 📚 Documentação

### Componentes
- **Props**: Tipos e validação
- **Events**: Emissão de eventos
- **Slots**: Conteúdo customizável
- **Styling**: CSS scoped

### API Integration
- **Endpoints**: Documentação completa
- **Authentication**: JWT tokens
- **Error Handling**: Tratamento global
- **Loading States**: UX otimizada

## 🐛 Troubleshooting

### Problemas Comuns
1. **CORS Error**: Verificar configuração backend
2. **Token Expired**: Refresh automático
3. **Network Error**: Verificar conectividade
4. **Build Error**: Limpar node_modules

### Debug
```bash
# Vue DevTools
npm install -g @vue/devtools

# Console logs
console.log('Debug info:', data)

# Network tab
F12 → Network → XHR
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar console do navegador
2. Consultar Vue DevTools
3. Verificar rede (Network tab)
4. Testar endpoints da API

---

**Desenvolvido usando Vue.js 3 + Composition API**
