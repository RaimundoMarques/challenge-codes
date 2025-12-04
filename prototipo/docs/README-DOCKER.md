# 🐳 Guia de Docker - Estrutura Separada

## 📋 Estrutura do Projeto

O projeto foi reorganizado para separar as responsabilidades:

```
manufacturing-system/
├── docker-compose.backend.yml    # Backend (DB + API)
├── docker-compose.frontend.yml   # Frontend (Vue.js)
├── backend/
│   ├── Dockerfile                # Dockerfile da API
│   └── ...
├── frontend/
│   ├── Dockerfile                # Dockerfile do Frontend
│   └── ...
└── ...
```

---

## 🏗️ Arquitetura

### Backend (Banco + API)
- **PostgreSQL**: Banco de dados
- **FastAPI**: API REST
- **Rede**: `manufacturing-system-backend-network`

### Frontend
- **Vue.js**: Aplicação frontend
- **Rede**: `manufacturing-system-frontend-network`
- **Comunicação**: Via HTTP com a API (http://localhost:8000)

---

## 🚀 Como Usar

### Opção 1: Usando Scripts Simplificados (Recomendado)

```bash
# Iniciar tudo
./start.sh

# Iniciar apenas backend
./start.sh backend

# Iniciar apenas frontend
./start.sh frontend

# Parar tudo
./stop.sh
```

### Opção 2: Iniciar Backend e Frontend Separadamente

#### 1. Iniciar Backend (Banco + API)
```bash
# Iniciar apenas o backend
docker-compose -f docker-compose.backend.yml up -d

# Ver logs
docker-compose -f docker-compose.backend.yml logs -f

# Ver status
docker-compose -f docker-compose.backend.yml ps
```

#### 2. Iniciar Frontend
```bash
# Iniciar apenas o frontend
docker-compose -f docker-compose.frontend.yml up -d

# Ver logs
docker-compose -f docker-compose.frontend.yml logs -f

# Ver status
docker-compose -f docker-compose.frontend.yml ps
```

### Opção 3: Iniciar Tudo de Uma Vez

```bash
# Iniciar backend e frontend juntos
docker-compose -f docker-compose.backend.yml -f docker-compose.frontend.yml up -d

# Ver logs de todos
docker-compose -f docker-compose.backend.yml -f docker-compose.frontend.yml logs -f

# Parar tudo
docker-compose -f docker-compose.backend.yml -f docker-compose.frontend.yml down
```

---

## 📦 Comandos Úteis

### Backend

```bash
# Parar backend
docker-compose -f docker-compose.backend.yml down

# Parar e remover volumes (CUIDADO: apaga dados do banco)
docker-compose -f docker-compose.backend.yml down -v

# Reconstruir e iniciar
docker-compose -f docker-compose.backend.yml up -d --build

# Reiniciar apenas a API
docker-compose -f docker-compose.backend.yml restart api

# Ver logs apenas da API
docker-compose -f docker-compose.backend.yml logs -f api

# Entrar no container da API
docker-compose -f docker-compose.backend.yml exec api bash

# Acessar o banco de dados
docker-compose -f docker-compose.backend.yml exec db-postgres psql -U postgres
```

### Frontend

```bash
# Parar frontend
docker-compose -f docker-compose.frontend.yml down

# Reconstruir e iniciar
docker-compose -f docker-compose.frontend.yml up -d --build

# Reiniciar frontend
docker-compose -f docker-compose.frontend.yml restart frontend

# Ver logs
docker-compose -f docker-compose.frontend.yml logs -f frontend

# Entrar no container
docker-compose -f docker-compose.frontend.yml exec frontend sh
```

---

## 🔧 Variáveis de Ambiente

### Backend
O backend usa o arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Database
DB_HOST=db-postgres
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=postgres
DB_PORT=5432

# Security
SECRET_KEY=your-secret-key-change-in-production
```

### Frontend
O frontend está configurado para se conectar à API em `http://localhost:8000`.

---

## 🌐 Acessos

Após iniciar os serviços:

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Banco de Dados**: localhost:5441

---

## 📝 Scripts de Inicialização

### Script para Backend (bash)
```bash
#!/bin/bash
docker-compose -f docker-compose.backend.yml up -d --build
docker-compose -f docker-compose.backend.yml logs -f
```

### Script para Frontend (bash)
```bash
#!/bin/bash
docker-compose -f docker-compose.frontend.yml up -d --build
docker-compose -f docker-compose.frontend.yml logs -f
```

---

## 🐛 Troubleshooting

### Problema: Frontend não consegue conectar à API

**Solução:**
1. Verificar se o backend está rodando:
   ```bash
   docker-compose -f docker-compose.backend.yml ps
   ```

2. Testar se a API está acessível:
   ```bash
   curl http://localhost:8000/docs
   ```

3. Verificar logs do backend:
   ```bash
   docker-compose -f docker-compose.backend.yml logs api
   ```

### Problema: Porta já em uso

**Solução:**
- Backend (porta 8000 ou 5441): Verificar processos usando as portas
- Frontend (porta 3000): Alterar no `docker-compose.frontend.yml`

### Problema: Banco de dados não inicia

**Solução:**
```bash
# Ver logs do banco
docker-compose -f docker-compose.backend.yml logs db-postgres

# Verificar se o diretório data/postgres existe e tem permissões corretas
ls -la data/postgres
```

---

## 🔄 Migração da Estrutura Antiga

Se você estava usando o `docker-compose.yml` antigo:

1. **Parar containers antigos:**
   ```bash
   docker-compose down
   ```

2. **Iniciar nova estrutura:**
   ```bash
   docker-compose -f docker-compose.backend.yml up -d
   docker-compose -f docker-compose.frontend.yml up -d
   ```

O arquivo `docker-compose.yml.backup` contém a configuração antiga para referência.

---

## 🎯 Vantagens da Nova Estrutura

1. **Separação de Responsabilidades**: Backend e frontend podem ser desenvolvidos e deployados independentemente
2. **Escalabilidade**: Cada serviço pode ser escalado separadamente
3. **Isolamento**: Problemas em um serviço não afetam o outro
4. **Flexibilidade**: Backend pode rodar em um servidor, frontend em outro
5. **Manutenção**: Mais fácil de manter e atualizar

---

## 📚 Referências

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vue.js Documentation](https://vuejs.org/)

