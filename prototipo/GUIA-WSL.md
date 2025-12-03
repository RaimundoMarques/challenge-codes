# 🐧 Guia para Rodar a Aplicação no WSL

## 📋 Configuração Inicial do WSL

### 1. Verificar se WSL está instalado
```bash
wsl --list --verbose
```

### 2. Acessar o WSL
```bash
wsl
# ou
wsl -d Ubuntu  # ou sua distribuição
```

---

## 🐳 Configuração do Docker no WSL

### Opção A: Docker Desktop com Integração WSL2 (Recomendado)

1. **Instalar Docker Desktop no Windows**
   - Baixe de: https://www.docker.com/products/docker-desktop
   - Durante a instalação, marque "Use WSL 2 based engine"

2. **Configurar integração WSL no Docker Desktop**
   - Abra Docker Desktop
   - Vá em Settings → Resources → WSL Integration
   - Ative a integração para sua distribuição WSL
   - Clique em "Apply & Restart"

3. **Verificar no WSL**
   ```bash
   # Dentro do WSL
   docker --version
   docker ps
   ```

### Opção B: Docker Engine direto no WSL

Se preferir instalar Docker diretamente no WSL:

```bash
# Atualizar pacotes
sudo apt update

# Instalar dependências
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Adicionar chave GPG do Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Adicionar repositório
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Reiniciar sessão WSL ou executar:
newgrp docker

# Verificar instalação
docker --version
docker compose version
```

---

## 🚀 Rodar a Aplicação no WSL

### 1. Navegar até o diretório do projeto
```bash
# Se o projeto está no Windows, acesse via /mnt
cd /mnt/c/Users/bc4g9993/Projects/challenge-codes/prototipo

# Ou se está dentro do WSL
cd ~/projetos/prototipo
```

### 2. Verificar Docker
```bash
# Verificar se Docker está funcionando
docker ps

# Se der erro, verificar se Docker Desktop está rodando no Windows
# ou se o serviço Docker está rodando no WSL
```

### 3. Iniciar os serviços
```bash
# Build e start
docker compose up -d --build

# Verificar status
docker compose ps

# Ver logs
docker compose logs -f
```

---

## 🔧 Configurações Específicas para WSL

### Ajustar permissões de arquivos
```bash
# Se houver problemas de permissão
sudo chown -R $USER:$USER .
```

### Configurar .env no WSL
```bash
# Verificar se .env existe
ls -la .env

# Se não existir, criar baseado no exemplo
cp .env.exemplo .env

# Editar com nano ou vim
nano .env
```

### Ajustar caminhos no docker-compose.yml
Se estiver usando caminhos do Windows via `/mnt`, pode haver problemas de performance. Considere:

1. **Mover projeto para dentro do WSL:**
   ```bash
   # Copiar projeto para ~/projetos
   cp -r /mnt/c/Users/bc4g9993/Projects/challenge-codes/prototipo ~/projetos/
   cd ~/projetos/prototipo
   ```

2. **Ou usar volumes nomeados:**
   ```yaml
   # Em vez de:
   volumes:
     - ./frontend:/app
   
   # Usar volume nomeado:
   volumes:
     - frontend_data:/app
   ```

---

## 🌐 Acessar a Aplicação

### Do Windows
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Do WSL
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Nota:** Se estiver usando WSL2, `localhost` funciona automaticamente.

---

## 🐛 Troubleshooting Específico para WSL

### Problema 1: Docker não encontrado no WSL
```bash
# Verificar se Docker Desktop está rodando no Windows
# Verificar integração WSL no Docker Desktop Settings

# Testar conexão
docker ps
```

### Problema 2: Erro de permissão
```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Verificar
groups
```

### Problema 3: Performance lenta com arquivos do Windows
```bash
# Mover projeto para dentro do WSL
# Ou usar WSL2 (mais rápido que WSL1)
wsl --set-version Ubuntu 2
```

### Problema 4: Porta já em uso
```bash
# Verificar processos
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :8000

# Finalizar processo
sudo kill -9 <PID>
```

### Problema 5: Frontend não acessível
```bash
# Verificar se container está rodando
docker compose ps

# Ver logs
docker compose logs frontend

# Verificar se porta está exposta
docker compose port frontend 3000
```

---

## 📝 Script de Inicialização para WSL

Crie um arquivo `start-wsl.sh`:

```bash
#!/bin/bash

echo "🚀 Iniciando aplicação no WSL..."

# Verificar Docker
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker não está rodando!"
    echo "Por favor, inicie o Docker Desktop ou o serviço Docker."
    exit 1
fi

# Navegar para o diretório
cd "$(dirname "$0")"

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker compose down

# Reconstruir e iniciar
echo "🔨 Reconstruindo e iniciando containers..."
docker compose up -d --build

# Aguardar inicialização
echo "⏳ Aguardando inicialização..."
sleep 10

# Verificar status
echo "📊 Status dos containers:"
docker compose ps

# Verificar acesso
echo ""
echo "🌐 Testando acesso..."
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend acessível em http://localhost:3000"
else
    echo "⚠️  Frontend ainda não está respondendo"
    echo "Verifique os logs: docker compose logs -f frontend"
fi

if curl -s http://localhost:8000/docs > /dev/null 2>&1; then
    echo "✅ API acessível em http://localhost:8000"
else
    echo "⚠️  API ainda não está respondendo"
    echo "Verifique os logs: docker compose logs -f api"
fi

echo ""
echo "✨ Pronto!"
echo "Frontend: http://localhost:3000"
echo "API: http://localhost:8000/docs"
```

Tornar executável:
```bash
chmod +x start-wsl.sh
./start-wsl.sh
```

---

## 🔍 Verificações Rápidas

```bash
# 1. Docker funcionando?
docker ps

# 2. Containers rodando?
docker compose ps

# 3. Logs do frontend
docker compose logs frontend --tail 20

# 4. Testar acesso
curl http://localhost:3000
curl http://localhost:8000/docs

# 5. Verificar portas
netstat -tulpn | grep -E ':(3000|8000)'
```

---

## 📚 Comandos Úteis no WSL

```bash
# Verificar versão do WSL
wsl --version

# Listar distribuições
wsl --list --verbose

# Parar WSL
wsl --shutdown

# Reiniciar Docker no WSL (se instalado localmente)
sudo service docker restart

# Ver logs em tempo real
docker compose logs -f

# Entrar no container
docker compose exec frontend sh
docker compose exec api bash
```

---

## ⚡ Dicas de Performance

1. **Use WSL2** (mais rápido que WSL1)
   ```bash
   wsl --set-version Ubuntu 2
   ```

2. **Mantenha projeto dentro do WSL** (não em /mnt/c)
   - Melhor performance de I/O
   - Menos problemas de permissão

3. **Use Docker Desktop com WSL2 backend**
   - Melhor integração
   - Mais fácil de gerenciar

4. **Aumente recursos do WSL** (se necessário)
   - Crie `~/.wslconfig` no Windows:
   ```ini
   [wsl2]
   memory=4GB
   processors=2
   ```

