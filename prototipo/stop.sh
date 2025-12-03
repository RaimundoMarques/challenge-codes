#!/bin/bash

# Script para parar todos os serviços
echo "🛑 Parando serviços..."
docker-compose -f docker-compose.frontend.yml down
docker-compose -f docker-compose.backend.yml down
echo "✅ Serviços parados!"

