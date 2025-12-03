# 🔍 Diagnóstico e Solução - Frontend Não Acessível

## ✅ Comando que você está usando
```bash
docker compose up -d --build
```

## 🔴 Problema Atual
O Docker Desktop não está acessível ou não está rodando.

## 📋 Checklist de Diagnóstico

### 1. Verificar se Docker Desktop está rodando
```bash
# Verificar status do Docker
docker ps

# Se retornar erro, o Docker Desktop não está rodando
```

**Solução:** Abra o Docker Desktop e aguarde até que o ícone fique verde na bandeja do sistema.

---

### 2. Verificar se os containers estão rodando
```bash
# Ver status de todos os containers
docker compose ps

# Ou
docker ps
```

**Resultado esperado:**
```
NAME           IMAGE                STATUS         PORTS
frontend       prototipo-frontend   Up X minutes   0.0.0.0:3000->3000/tcp
api            prototipo-api         Up X minutes   0.0.0.0:8000->8000/tcp
db-postgres    postgres:15.3-alpine  Up X minutes   0.0.0.0:5441->5432/tcp
```

---

### 3. Verificar logs do frontend
```bash
# Ver últimas 50 linhas
docker compose logs frontend --tail 50

# Acompanhar logs em tempo real
docker compose logs -f frontend
```

**O que procurar:**
- ✅ `App running at: http://0.0.0.0:3000/` - Frontend iniciado com sucesso
- ❌ Erros de compilação
- ❌ Erros de dependências (npm install)
- ❌ Porta já em uso

---

### 4. Verificar se a porta 3000 está livre
```bash
# Windows PowerShell
netstat -ano | findstr :3000

# Se houver processo, anote o PID e finalize:
# taskkill /PID <numero_pid> /F
```

---

### 5. Testar acesso ao frontend
```bash
# Via curl
curl http://localhost:3000

# Ou abra no navegador
# http://localhost:3000
```

---

## 🛠️ Soluções Comuns

### Problema 1: Container não inicia
```bash
# Parar todos os containers
docker compose down

# Reconstruir e iniciar
docker compose up -d --build

# Ver logs detalhados
docker compose logs frontend
```

### Problema 2: Erro de build do frontend
```bash
# Limpar cache do Docker
docker system prune -a

# Reconstruir apenas o frontend
docker compose build --no-cache frontend
docker compose up -d frontend
```

### Problema 3: Porta 3000 ocupada
**Opção A:** Finalizar processo na porta
```bash
# Encontrar processo
netstat -ano | findstr :3000

# Finalizar (substitua <PID> pelo número)
taskkill /PID <PID> /F
```

**Opção B:** Alterar porta no docker-compose.yml
```yaml
frontend:
  ports:
    - "3001:3000"  # Mude 3000 para 3001
```

### Problema 4: Frontend inicia mas não carrega
```bash
# Verificar se node_modules está montado corretamente
docker compose exec frontend ls -la /app/node_modules

# Se estiver vazio, reinstalar
docker compose exec frontend npm install
```

### Problema 5: Erro de conexão com API
O frontend está configurado para acessar a API em `http://localhost:8000`.

**Verificar se API está rodando:**
```bash
curl http://localhost:8000/docs
```

**Se API não estiver acessível:**
```bash
# Ver logs da API
docker compose logs api

# Reiniciar API
docker compose restart api
```

---

## 🚀 Passo a Passo Completo

### 1. Iniciar Docker Desktop
- Abra o Docker Desktop
- Aguarde até o ícone ficar verde
- Verifique: `docker ps` deve funcionar

### 2. Limpar e Reconstruir
```bash
# Parar tudo
docker compose down

# Remover volumes antigos (opcional, cuidado!)
docker compose down -v

# Reconstruir tudo
docker compose up -d --build
```

### 3. Aguardar Inicialização
```bash
# Aguardar 30-60 segundos para tudo inicializar
# Verificar status
docker compose ps
```

### 4. Verificar Logs
```bash
# Frontend
docker compose logs frontend

# API
docker compose logs api

# Banco
docker compose logs db-postgres
```

### 5. Testar Acesso
- Frontend: http://localhost:3000
- API: http://localhost:8000/docs
- Banco: localhost:5441

---

## 📊 Comandos Úteis

```bash
# Status geral
docker compose ps

# Logs de todos os serviços
docker compose logs

# Reiniciar um serviço específico
docker compose restart frontend

# Parar tudo
docker compose down

# Parar e remover volumes
docker compose down -v

# Ver uso de recursos
docker stats

# Entrar no container do frontend
docker compose exec frontend sh
```

---

## 🔧 Verificações Avançadas

### Verificar configuração do Vue
```bash
# Entrar no container
docker compose exec frontend sh

# Verificar vue.config.js
cat vue.config.js

# Verificar package.json
cat package.json
```

### Verificar variáveis de ambiente
```bash
# Ver variáveis do frontend
docker compose exec frontend env
```

### Verificar rede Docker
```bash
# Ver redes
docker network ls

# Inspecionar rede
docker network inspect prototipo_default
```

---

## ⚠️ Problemas Conhecidos

### 1. Windows: Docker Desktop não inicia
- Verificar se WSL2 está instalado
- Verificar se virtualização está habilitada no BIOS
- Reiniciar Docker Desktop como administrador

### 2. Porta já em uso
- Verificar outros serviços na porta 3000
- Usar outra porta ou finalizar processo

### 3. node_modules não sincroniza
- O volume `/app/node_modules` deve estar como volume anônimo
- Se houver problemas, reconstruir o container

---

## 📞 Próximos Passos

Se após seguir este guia o problema persistir:

1. **Cole aqui os logs completos:**
   ```bash
   docker compose logs frontend > frontend-logs.txt
   ```

2. **Verifique a saída de:**
   ```bash
   docker compose ps
   docker compose logs api
   ```

3. **Teste acesso direto:**
   ```bash
   curl -v http://localhost:3000
   curl -v http://localhost:8000/docs
   ```

