# 🚀 Sistema de Ordens de Serviço

## 📋 Visão Geral

Sistema completo de gerenciamento de ordens de serviço desenvolvido com **FastAPI** (backend) e **Vue.js 3** (frontend), utilizando **PostgreSQL** como banco de dados e **Docker** para containerização.

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   Vue.js 3      │◄──►│   FastAPI       │◄──►│   PostgreSQL    │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Tecnologias Utilizadas

### Backend
- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para Python
- **JWT** - Autenticação via tokens
- **Bcrypt** - Hash de senhas
- **Pydantic** - Validação de dados

### Frontend
- **Vue.js 3** - Framework JavaScript reativo
- **Vue Router** - Roteamento SPA
- **Vuex** - Gerenciamento de estado
- **Axios** - Cliente HTTP
- **CSS3** - Estilização moderna

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração
- **Nginx** - Proxy reverso (produção)

## 🔐 Sistema de Autenticação

### Fluxo Completo
1. **Login**: Usuário insere credenciais
2. **Validação**: Backend verifica no banco
3. **JWT**: Token gerado e retornado
4. **Storage**: Token armazenado no frontend
5. **Requests**: Token enviado em cada requisição
6. **Middleware**: Validação automática no backend

### Níveis de Acesso
- **Administrador**: Acesso total ao sistema
- **Técnico**: Acesso limitado às suas ordens

## 📊 Funcionalidades Principais

### 👥 Gestão de Usuários
- ✅ **CRUD completo** de usuários
- ✅ **Roles** (administrador/técnico)
- ✅ **Status** ativo/inativo
- ✅ **Validação** de dados

### 📋 Gestão de Ordens de Serviço
- ✅ **Criação** de novas ordens
- ✅ **Atribuição** de técnicos
- ✅ **Status** (aberta/em andamento/fechada)
- ✅ **Filtros** avançados
- ✅ **Reatribuição** de técnicos

### 🏢 Gestão de Clientes e Equipamentos
- ✅ **CRUD** de clientes
- ✅ **CRUD** de equipamentos
- ✅ **Relacionamento** cliente-equipamento
- ✅ **Criação inline** durante nova ordem

### 📸 Sistema de Fotos
- ✅ **Upload** drag & drop
- ✅ **Galeria** de fotos
- ✅ **Modal** de visualização
- ✅ **Exclusão** de fotos
- ✅ **Validação** de tipos e tamanhos

### ✅ Sistema de Checklist
- ✅ **Seleção** de checklist
- ✅ **Respostas** interativas
- ✅ **Persistência** de dados
- ✅ **Validação** de campos

## 🏗️ Estrutura do Projeto

```
prototipo/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── models/         # Modelos de dados
│   │   ├── routers/        # Endpoints da API
│   │   ├── middleware/     # Middleware de auth
│   │   └── utils/         # Utilitários
│   ├── requirements.txt    # Dependências Python
│   └── README.md          # Documentação backend
├── frontend/               # Interface Vue.js
│   ├── src/
│   │   ├── components/    # Componentes modulares
│   │   ├── views/         # Páginas principais
│   │   ├── router/        # Configuração de rotas
│   │   └── store/         # Gerenciamento de estado
│   ├── package.json       # Dependências Node.js
│   └── README.md          # Documentação frontend
├── initdb/                # Scripts de inicialização
│   └── schema.sql         # Schema do banco
├── docker-compose.yml     # Orquestração Docker
├── .env                   # Variáveis de ambiente
└── README.md              # Este arquivo
```

## 🚀 Instalação e Execução

### Pré-requisitos
- Docker e Docker Compose
- Git

### 1. Clone o Repositório
```bash
git clone <repository-url>
cd prototipo
```

### 2. Configuração do Ambiente
```bash
# Copiar arquivo de ambiente
cp .env.example .env

# Editar variáveis se necessário
nano .env
```

### 3. Executar com Docker
```bash
# Build e execução
docker-compose up -d --build

# Verificar status
docker-compose ps

# Logs
docker-compose logs -f
```

### 4. Acessar a Aplicação
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

## 🔧 Configuração de Desenvolvimento

### Backend (Local)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Local)
```bash
cd frontend
npm install
npm run serve
```

## 📊 Banco de Dados

### Schema Principal
```sql
-- Usuários do sistema
users (id, username, password_hash, name, email, role, is_active, created_at)

-- Clientes
clients (id, name, email, phone, address, created_at)

-- Equipamentos
equipments (id, client_id, type, brand, model, serial_number, created_at)

-- Ordens de Serviço
service_orders (id, title, description, status, client_id, equipment_id, user_id, activities_description, created_at, updated_at)

-- Fotos
os_photos (id, service_order_id, photo_url, uploaded_at)

-- Checklists
checklists (id, name, created_at)
checklist_items (id, checklist_id, description)
os_checklist_responses (id, service_order_id, checklist_item_id, is_checked)
```

### Dados Iniciais
- **Usuário Admin**: username: `admin`, password: `123456`
- **Checklists**: Manutenção, Reparo, Instalação
- **Clientes**: Dados de exemplo
- **Equipamentos**: Dados de exemplo

## 🔐 Segurança

### Autenticação
- **JWT Tokens** com expiração de 30 minutos
- **Bcrypt** para hash de senhas
- **Middleware** de validação automática
- **Revogação** de tokens no logout

### Validação
- **Pydantic** para validação de dados
- **SQLAlchemy** para proteção SQL injection
- **CORS** configurado para frontend
- **Sanitização** de inputs

## 📈 Performance

### Otimizações
- **Connection Pooling** no banco
- **Lazy Loading** de relacionamentos
- **Componentes modulares** no frontend
- **Lazy loading** de rotas
- **Caching** de tokens

### Monitoramento
- **Logs estruturados** no backend
- **Health checks** automáticos
- **Métricas** do FastAPI
- **Vue DevTools** no frontend

## 🧪 Testes

### Backend
```bash
# Testes unitários
pytest

# Testes de integração
pytest tests/integration/
```

### Frontend
```bash
# Testes unitários
npm run test:unit

# Testes e2e
npm run test:e2e
```

## 🚀 Deploy em Produção

### 1. Configuração do Servidor
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Configuração de Produção
```bash
# Variáveis de ambiente
export DB_PASSWORD=your_secure_password
export SECRET_KEY=your_secure_secret_key

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### 3. SSL e Domínio
- **Certificado SSL** (Let's Encrypt)
- **Domínio** configurado
- **Nginx** como proxy reverso
- **Backup** automático do banco

## 📚 Documentação

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI**: http://localhost:8000/openapi.json

### Componentes Frontend
- **Vue DevTools** para debug
- **Props/Events** documentados
- **Styling** com CSS scoped
- **Responsividade** mobile-first

## 🐛 Troubleshooting

### Problemas Comuns

#### Backend
1. **Database Connection**: Verificar variáveis de ambiente
2. **JWT Invalid**: Verificar SECRET_KEY
3. **CORS Error**: Verificar configuração de origins
4. **Permission Denied**: Verificar roles de usuário

#### Frontend
1. **CORS Error**: Verificar configuração backend
2. **Token Expired**: Refresh automático
3. **Network Error**: Verificar conectividade
4. **Build Error**: Limpar node_modules

### Logs
```bash
# Backend logs
docker-compose logs -f api

# Frontend logs
docker-compose logs -f frontend

# Database logs
docker-compose logs -f db-postgres
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar logs da aplicação
2. Consultar documentação Swagger
3. Verificar configuração de ambiente
4. Testar endpoints individualmente

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido usando FastAPI + Vue.js 3 + PostgreSQL**