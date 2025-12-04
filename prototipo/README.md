# 🏭 Manufacturing System

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
manufacturing-system/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── models/         # Modelos de dados
│   │   ├── routers/        # Endpoints da API
│   │   ├── middleware/     # Middleware de auth
│   │   └── utils/         # Utilitários
│   ├── docs/              # Documentação do backend
│   │   └── README.md
│   ├── initdb/            # Scripts de inicialização do banco
│   │   ├── schema.sql     # Schema do banco
│   │   └── add_activities_description.sql
│   ├── requirements.txt    # Dependências Python
│   └── Dockerfile         # Dockerfile do backend
├── frontend/               # Interface Vue.js
│   ├── src/
│   │   ├── components/    # Componentes modulares
│   │   ├── views/         # Páginas principais
│   │   ├── router/        # Configuração de rotas
│   │   └── store/         # Gerenciamento de estado
│   ├── docs/              # Documentação do frontend
│   │   └── README.md
│   ├── package.json       # Dependências Node.js
│   └── Dockerfile         # Dockerfile do frontend
├── docs/                   # Documentação geral
│   ├── README-DOCKER.md
│   ├── RELATORIO_TESTES.md
│   └── HISTORICO_MUDANCAS.md
├── docker-compose.backend.yml    # Compose do backend (Banco + API)
├── docker-compose.frontend.yml   # Compose do frontend
├── start.sh               # Script para iniciar serviços
├── stop.sh                # Script para parar serviços
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
cd manufacturing-system
```

### 2. Configuração do Ambiente
```bash
# Copiar arquivo de ambiente
cp .env.example .env

# Editar variáveis se necessário
nano .env
```

### 3. Executar com Docker

#### ⚡ Opção 1: Usando Scripts (Recomendado - Mais Simples!)

Os scripts automatizam o Docker Compose e permitem subir os serviços de forma independente. **Tudo continua rodando em containers Docker!**

```bash
# 🚀 Iniciar TUDO (Backend + Frontend)
./start.sh
# ou
./start.sh all

# 🔧 Iniciar apenas BACKEND (Banco + API) - em containers Docker
./start.sh backend

# 🎨 Iniciar apenas FRONTEND - em container Docker
./start.sh frontend

# 🛑 Parar tudo
./stop.sh

# 🛑 Parar apenas backend
./stop.sh backend

# 🛑 Parar apenas frontend
./stop.sh frontend
```

**💡 Dica:** Use `./start.sh backend` para trabalhar apenas na API, ou `./start.sh frontend` quando precisar testar apenas a interface!

**🐳 Nota:** Os scripts executam comandos Docker Compose por trás. Você pode verificar os containers com:
```bash
docker ps
# ou
docker-compose -f docker-compose.backend.yml ps
docker-compose -f docker-compose.frontend.yml ps
```

#### Opção 2: Docker Compose Manual
```bash
# Backend (DB + API)
docker-compose -f docker-compose.backend.yml up -d --build

# Frontend
docker-compose -f docker-compose.frontend.yml up -d --build

# Verificar status
docker-compose -f docker-compose.backend.yml ps
docker-compose -f docker-compose.frontend.yml ps
```

**📚 Para mais detalhes sobre Docker, consulte: [docs/README-DOCKER.md](docs/README-DOCKER.md)**

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

#### ✅ Opção 1: Com npm (Recomendado para desenvolvimento rápido)

Você pode rodar o frontend diretamente com npm, sem Docker:

```bash
cd frontend
npm install
npm run serve
```

O frontend estará disponível em: **http://localhost:3000**

**💡 Vantagens:**
- ✅ Hot reload mais rápido
- ✅ Debug mais fácil
- ✅ Sem precisar reconstruir containers
- ✅ Ideal para desenvolvimento

**⚠️ Importante:** Certifique-se de que o backend está rodando (via Docker com `./start.sh backend` ou localmente) para que o frontend possa se conectar à API em `http://localhost:8000`.

#### 🐳 Opção 2: Com Docker (Ambiente isolado)

```bash
# Usando o script
./start.sh frontend

# Ou manualmente
docker-compose -f docker-compose.frontend.yml up -d --build
```

**💡 Quando usar Docker:**
- ✅ Ambiente de produção/teste
- ✅ Garantir consistência entre desenvolvedores
- ✅ Quando não tem Node.js instalado localmente

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

### Documentação Geral
- **[README-DOCKER.md](docs/README-DOCKER.md)** - Guia completo do Docker
- **[RELATORIO_TESTES.md](docs/RELATORIO_TESTES.md)** - Relatório de testes dos endpoints
- **[HISTORICO_MUDANCAS.md](docs/HISTORICO_MUDANCAS.md)** - Histórico de mudanças e ajustes

### Documentação por Módulo
- **[Backend](backend/docs/README.md)** - Documentação completa da API
- **[Frontend](frontend/docs/README.md)** - Documentação completa do frontend

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

#### ❌ Docker não está rodando
**Erro:** `error during connect: Get "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine...": open //./pipe/dockerDesktopLinuxEngine: O sistema não pode encontrar o arquivo especificado.`

**Solução:**
1. Abra o **Docker Desktop** no Windows
2. Aguarde o Docker inicializar completamente (ícone do Docker na bandeja deve ficar verde)
3. Execute o script novamente: `./start.sh backend` ou `./start.sh frontend`

Os scripts agora verificam automaticamente se o Docker está rodando e exibem uma mensagem clara caso não esteja!

#### Backend
1. **Database Connection**: Verificar variáveis de ambiente no arquivo `.env`
2. **JWT Invalid**: Verificar SECRET_KEY no arquivo `.env`
3. **CORS Error**: Verificar configuração de origins no backend
4. **Permission Denied**: Verificar roles de usuário

#### Frontend
1. **CORS Error**: Verificar configuração backend e se a API está rodando
2. **Token Expired**: Refresh automático ou fazer logout/login novamente
3. **Network Error**: Verificar se o backend está rodando (`./start.sh backend`)
4. **Build Error**: Limpar node_modules e reinstalar dependências

### Logs
```bash
# Backend logs
docker-compose -f docker-compose.backend.yml logs -f api
docker-compose -f docker-compose.backend.yml logs -f db-postgres

# Frontend logs
docker-compose -f docker-compose.frontend.yml logs -f frontend
```

**📚 Para mais informações, consulte a [documentação completa](docs/README-DOCKER.md)**

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

**Manufacturing System - Desenvolvido usando FastAPI + Vue.js 3 + PostgreSQL**