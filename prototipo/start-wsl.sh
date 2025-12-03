#!/bin/bash

echo "🚀 Iniciando aplicação no WSL..."

# Verificar Docker
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker não está rodando!"
    echo "Por favor, inicie o Docker Desktop ou o serviço Docker."
    echo ""
    echo "Se estiver usando Docker Desktop:"
    echo "  1. Abra o Docker Desktop no Windows"
    echo "  2. Vá em Settings → Resources → WSL Integration"
    echo "  3. Ative a integração para esta distribuição WSL"
    echo ""
    echo "Se estiver usando Docker Engine no WSL:"
    echo "  sudo service docker start"
    exit 1
fi

echo "✅ Docker está rodando"

# Navegar para o diretório do script
cd "$(dirname "$0")"

# Verificar se docker-compose.yml existe
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Arquivo docker-compose.yml não encontrado!"
    echo "Certifique-se de estar no diretório correto do projeto."
    exit 1
fi

# Parar containers existentes
echo ""
echo "🛑 Parando containers existentes..."
docker compose down 2>/dev/null || docker-compose down 2>/dev/null

# Reconstruir e iniciar
echo ""
echo "🔨 Reconstruindo e iniciando containers..."
docker compose up -d --build 2>&1 | grep -v "deprecated" || docker-compose up -d --build 2>&1 | grep -v "deprecated"

# Aguardar inicialização
echo ""
echo "⏳ Aguardando inicialização dos serviços..."
sleep 15

# Verificar status
echo ""
echo "📊 Status dos containers:"
docker compose ps 2>/dev/null || docker-compose ps

# Verificar acesso ao frontend
echo ""
echo "🌐 Testando acesso aos serviços..."
echo ""

# Testar frontend
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200\|301\|302"; then
    echo "✅ Frontend acessível em http://localhost:3000"
else
    echo "⚠️  Frontend ainda não está respondendo"
    echo "   Verifique os logs: docker compose logs -f frontend"
fi

# Testar API
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs | grep -q "200\|301\|302"; then
    echo "✅ API acessível em http://localhost:8000"
else
    echo "⚠️  API ainda não está respondendo"
    echo "   Verifique os logs: docker compose logs -f api"
fi

# Testar banco
if docker compose exec -T db-postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo "✅ Banco de dados está pronto"
else
    echo "⚠️  Banco de dados ainda não está pronto"
    echo "   Verifique os logs: docker compose logs -f db-postgres"
fi

echo ""
echo "✨ Serviços iniciados!"
echo ""
echo "📍 URLs de acesso:"
echo "   Frontend: http://localhost:3000"
echo "   API:      http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📋 Comandos úteis:"
echo "   Ver logs:        docker compose logs -f [serviço]"
echo "   Parar tudo:      docker compose down"
echo "   Reiniciar:       docker compose restart [serviço]"
echo "   Status:          docker compose ps"
echo ""

