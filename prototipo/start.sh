#!/bin/bash

# Script unificado para iniciar serviços
# Uso: ./start.sh [backend|frontend|all]

SERVICE=${1:-all}

case $SERVICE in
  backend)
    echo "🚀 Iniciando Backend..."
    docker-compose -f docker-compose.backend.yml up -d --build
    ;;
  frontend)
    echo "🚀 Iniciando Frontend..."
    docker-compose -f docker-compose.frontend.yml up -d --build
    ;;
  all|*)
    echo "🚀 Iniciando Backend e Frontend..."
    docker-compose -f docker-compose.backend.yml up -d --build
    sleep 5
    docker-compose -f docker-compose.frontend.yml up -d --build
    ;;
esac

echo ""
echo "✨ Serviços iniciados!"
echo "📍 URLs: Frontend http://localhost:3000 | API http://localhost:8000"

