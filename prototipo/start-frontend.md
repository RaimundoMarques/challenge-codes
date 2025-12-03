# 🚀 Guia para Iniciar o Frontend

## Problema Identificado
O Docker Desktop não está rodando, por isso o frontend não está acessível.

## Solução 1: Iniciar via Docker (Recomendado)

### Passo 1: Iniciar Docker Desktop
1. Abra o **Docker Desktop** no Windows
2. Aguarde até que o Docker esteja totalmente iniciado (ícone verde na bandeja)

### Passo 2: Iniciar os Containers
Execute no terminal:
```bash
docker-compose up -d
```

### Passo 3: Verificar Status
```bash
docker-compose ps
```

### Passo 4: Verificar Logs do Frontend
```bash
docker-compose logs -f frontend
```

### Passo 5: Acessar o Frontend
Abra no navegador: **http://localhost:3000**

---

## Solução 2: Rodar Frontend Localmente (Sem Docker)

Se preferir rodar o frontend diretamente no seu sistema:

### Passo 1: Instalar Node.js
Certifique-se de ter Node.js 18+ instalado.

### Passo 2: Instalar Dependências
```bash
cd frontend
npm install
```

### Passo 3: Iniciar Servidor de Desenvolvimento
```bash
npm run serve
```

### Passo 4: Acessar
O frontend estará disponível em: **http://localhost:3000**

**Nota:** A API ainda precisa estar rodando no Docker ou separadamente.

---

## Troubleshooting

### Porta 3000 já em uso
Se a porta 3000 estiver ocupada:
```bash
# Windows - Verificar processo na porta
netstat -ano | findstr :3000

# Ou alterar a porta no vue.config.js
```

### Erro de conexão com API
Verifique se a API está rodando:
```bash
curl http://localhost:8000/docs
```

### Limpar e Reconstruir
```bash
docker-compose down
docker-compose up -d --build
```

