# 🚀 Rodando o Frontend com npm (Sem Docker)

## ✅ Sim! Você pode rodar o frontend com npm

O frontend pode ser executado de duas formas:
1. **Com npm** (desenvolvimento rápido, sem Docker)
2. **Com Docker** (ambiente isolado)

## 📋 Pré-requisitos

- **Node.js** 18+ instalado
- **npm** ou **yarn** instalado
- **Backend rodando** (Docker ou local)

## 🚀 Passo a Passo

### 1. Instalar Dependências

```bash
cd frontend
npm install
```

### 2. Iniciar o Servidor de Desenvolvimento

```bash
npm run serve
```

O frontend estará disponível em: **http://localhost:3000**

### 3. Verificar se o Backend está Rodando

O frontend precisa se conectar à API em `http://localhost:8000`. Certifique-se de que o backend está rodando:

```bash
# Opção 1: Backend no Docker
./start.sh backend

# Opção 2: Backend local (se configurado)
cd backend
uvicorn app.main:app --reload
```

## 📝 Scripts Disponíveis

### `npm run serve`
Inicia o servidor de desenvolvimento com hot reload na porta 3000.

```bash
npm run serve
```

### `npm run build`
Gera os arquivos otimizados para produção.

```bash
npm run build
```

### `npm run preview`
Visualiza a build de produção localmente.

```bash
npm run build
npm run preview
```

## ⚙️ Configuração

### URL da API

O frontend está configurado para se conectar à API em `http://localhost:8000` por padrão.

Se precisar alterar, edite o arquivo:
- `frontend/src/store/modules/auth.js` (linha 3)

```javascript
const API_BASE_URL = 'http://localhost:8000'  // Altere aqui se necessário
```

### Porta do Frontend

A porta padrão é **3000**. Para alterar:

1. Edite `frontend/package.json`:
```json
"serve": "vue-cli-service serve --host 0.0.0.0 --port 3000"
```

2. Ou edite `frontend/vue.config.js`:
```javascript
devServer: {
  port: 3000  // Altere aqui
}
```

## 💡 Vantagens de Usar npm

✅ **Hot reload mais rápido** - Mudanças aparecem instantaneamente  
✅ **Debug mais fácil** - Vue DevTools funciona melhor  
✅ **Sem Docker** - Não precisa reconstruir containers  
✅ **Ideal para desenvolvimento** - Ciclo de desenvolvimento mais ágil  

## 🐳 Quando Usar Docker?

Use Docker quando:
- ✅ Quer ambiente isolado e consistente
- ✅ Não tem Node.js instalado localmente
- ✅ Está testando em ambiente de produção
- ✅ Quer garantir que todos os desenvolvedores usam a mesma versão

## 🔄 Workflow Recomendado

### Desenvolvimento Ativo
```bash
# Terminal 1: Backend no Docker
./start.sh backend

# Terminal 2: Frontend com npm
cd frontend
npm run serve
```

### Teste Completo
```bash
# Tudo no Docker
./start.sh
```

## 🐛 Problemas Comuns

### Erro: "Cannot connect to API"
**Solução:** Verifique se o backend está rodando:
```bash
curl http://localhost:8000/docs
```

### Erro: "Port 3000 already in use"
**Solução:** Altere a porta ou pare o processo que está usando a porta:
```bash
# Windows
netstat -ano | findstr :3000

# Linux/WSL
lsof -i :3000
```

### Erro: "Module not found"
**Solução:** Reinstale as dependências:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Hot reload não funciona
**Solução:** 
1. Verifique se está usando `npm run serve` (não `npm start`)
2. Limpe o cache: `npm run serve -- --clear`

## 📚 Comandos Úteis

```bash
# Instalar dependências
npm install

# Desenvolvimento
npm run serve

# Build para produção
npm run build

# Verificar versão do Node
node --version

# Verificar versão do npm
npm --version

# Limpar cache
npm cache clean --force
```

## 🎯 Resumo

- ✅ **Pode rodar com npm** - Sim, totalmente suportado!
- ✅ **Mais rápido para desenvolvimento** - Hot reload instantâneo
- ✅ **Backend precisa estar rodando** - API em `http://localhost:8000`
- ✅ **Porta padrão: 3000** - Configurável se necessário

**Use npm para desenvolvimento ativo e Docker para testes completos!** 🚀

