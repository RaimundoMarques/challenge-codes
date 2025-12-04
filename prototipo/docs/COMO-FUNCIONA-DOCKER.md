# 🐳 Como Funcionam os Scripts com Docker

## ✅ Sim! Tudo continua rodando no Docker

Os scripts (`start.sh` e `stop.sh`) são apenas **atalhos simplificados** que executam comandos Docker Compose por trás. Tudo continua rodando em **containers Docker** como antes!

## 📋 O que acontece quando você roda os scripts?

### `./start.sh backend`
```bash
# O script executa internamente:
docker-compose -f docker-compose.backend.yml up -d --build

# Isso cria/sobe os containers:
# ✅ manufacturing-system-db-postgres (PostgreSQL)
# ✅ manufacturing-system-api (FastAPI)
```

### `./start.sh frontend`
```bash
# O script executa internamente:
docker-compose -f docker-compose.frontend.yml up -d --build

# Isso cria/sobe o container:
# ✅ manufacturing-system-frontend (Vue.js)
```

### `./stop.sh backend`
```bash
# O script executa internamente:
docker-compose -f docker-compose.backend.yml down

# Isso para e remove os containers:
# 🛑 manufacturing-system-db-postgres
# 🛑 manufacturing-system-api
```

## 🔍 Como verificar que está rodando no Docker?

### 1. Ver todos os containers
```bash
docker ps
```

Você verá algo assim:
```
CONTAINER ID   IMAGE                     STATUS          PORTS
abc123def456   manufacturing-system-frontend        Up 2 minutes    0.0.0.0:3000->3000/tcp
xyz789ghi012   manufacturing-system-api             Up 5 minutes    0.0.0.0:8000->8000/tcp
def456abc123   postgres:15.3-alpine                 Up 5 minutes    0.0.0.0:5441->5432/tcp
```

### 2. Ver containers específicos do backend
```bash
docker-compose -f docker-compose.backend.yml ps
```

### 3. Ver containers específicos do frontend
```bash
docker-compose -f docker-compose.frontend.yml ps
```

### 4. Ver logs dos containers
```bash
# Backend
docker-compose -f docker-compose.backend.yml logs -f

# Frontend
docker-compose -f docker-compose.frontend.yml logs -f

# Ou ver logs direto pelo Docker
docker logs manufacturing-system-api
docker logs manufacturing-system-frontend
docker logs manufacturing-system-db-postgres
```

## 🎯 Vantagens dos Scripts

### Antes (sem scripts):
```bash
# Para subir backend
docker-compose -f docker-compose.backend.yml up -d --build

# Para subir frontend
docker-compose -f docker-compose.frontend.yml up -d --build

# Para parar tudo
docker-compose -f docker-compose.frontend.yml down
docker-compose -f docker-compose.backend.yml down
```

### Agora (com scripts):
```bash
# Para subir backend
./start.sh backend

# Para subir frontend
./start.sh frontend

# Para parar tudo
./stop.sh
```

**✨ Mais simples, mas ainda usando Docker!**

## 🔧 Se preferir usar Docker diretamente

Você pode continuar usando os comandos Docker Compose manualmente se preferir:

```bash
# Backend
docker-compose -f docker-compose.backend.yml up -d --build
docker-compose -f docker-compose.backend.yml down

# Frontend
docker-compose -f docker-compose.frontend.yml up -d --build
docker-compose -f docker-compose.frontend.yml down
```

Os scripts são apenas uma camada de conveniência!

## 📦 Estrutura dos Containers

### Backend (`docker-compose.backend.yml`)
- **Container:** `manufacturing-system-db-postgres`
  - **Imagem:** `postgres:15.3-alpine`
  - **Porta:** `5441:5432`
  - **Volume:** `./data/postgres` (persistência de dados)

- **Container:** `manufacturing-system-api`
  - **Build:** `./backend/Dockerfile`
  - **Porta:** `8000:8000`
  - **Volume:** `./backend:/code` (hot reload)

### Frontend (`docker-compose.frontend.yml`)
- **Container:** `manufacturing-system-frontend`
  - **Build:** `./frontend/Dockerfile`
  - **Porta:** `3000:3000`
  - **Volume:** `./frontend:/app` (hot reload)

## 🎓 Resumo

✅ **Sim, tudo roda no Docker**  
✅ **Scripts são apenas atalhos**  
✅ **Você ainda pode usar Docker diretamente**  
✅ **Containers isolados e organizados**  
✅ **Volumes montados para desenvolvimento**  

**Os scripts tornam tudo mais simples, mas a tecnologia por trás continua sendo Docker!** 🐳

