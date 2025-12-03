# ⚡ Quick Start - WSL

## 🚀 Início Rápido

### 1. Verificar Docker no WSL
```bash
docker ps
```

Se der erro, você precisa:
- **Opção A:** Iniciar Docker Desktop no Windows e ativar integração WSL
- **Opção B:** Instalar Docker Engine diretamente no WSL

### 2. Iniciar a Aplicação
```bash
# Usando o script
./start-wsl.sh

# Ou manualmente
docker compose up -d --build
```

### 3. Verificar Status
```bash
docker compose ps
```

### 4. Ver Logs (se necessário)
```bash
docker compose logs -f frontend
docker compose logs -f api
```

### 5. Acessar
- Frontend: http://localhost:3000
- API: http://localhost:8000/docs

---

## 🔧 Se Docker não estiver funcionando

### Docker Desktop (Recomendado)
1. Abra Docker Desktop no Windows
2. Settings → Resources → WSL Integration
3. Ative para sua distribuição WSL
4. Apply & Restart

### Docker Engine no WSL
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker
```

---

## 📋 Comandos Essenciais

```bash
# Iniciar
docker compose up -d --build

# Parar
docker compose down

# Ver logs
docker compose logs -f [serviço]

# Reiniciar serviço
docker compose restart [serviço]

# Status
docker compose ps
```

---

## 🐛 Problemas Comuns

### "Cannot connect to Docker daemon"
→ Docker Desktop não está rodando ou integração WSL não está ativada

### "Port already in use"
→ Outro processo está usando a porta
```bash
sudo netstat -tulpn | grep :3000
sudo kill -9 <PID>
```

### Frontend não carrega
→ Verificar logs:
```bash
docker compose logs frontend
```

---

## 📚 Documentação Completa
Veja `GUIA-WSL.md` para guia detalhado.

