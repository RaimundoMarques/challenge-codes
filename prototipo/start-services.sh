#!/bin/bash

# Script para iniciar os serviços
echo "🚀 Iniciando serviços do protótipo..."

# Verificar se Docker está rodando
echo ""
echo "📦 Verificando Docker..."
if docker ps > /dev/null 2>&1; then
    echo "✅ Docker está rodando"
else
    echo "❌ Docker não está rodando!"
    echo "Por favor, inicie o Docker Desktop primeiro."
    exit 1
fi

# Iniciar containers
echo ""
echo "🔧 Iniciando containers..."
docker-compose up -d

# Aguardar alguns segundos
sleep 5

# Verificar status
echo ""
echo "📊 Status dos containers:"
docker-compose ps

# Verificar se frontend está acessível
echo ""
echo "🌐 Testando acesso ao frontend..."
sleep 3

if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend está acessível em http://localhost:3000"
else
    echo "⚠️  Frontend ainda não está respondendo. Aguarde alguns segundos..."
    echo "Verifique os logs com: docker-compose logs -f frontend"
fi

echo ""
echo "✨ Serviços iniciados!"
echo "Frontend: http://localhost:3000"
echo "API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"

