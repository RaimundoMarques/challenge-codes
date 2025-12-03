#!/bin/bash

# Script simples para iniciar serviços
# Uso: ./start.sh [backend|frontend|all]

set -e

SERVICE=${1:-all}

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
case $SERVICE in
  backend)
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Iniciando Backend (Banco + API)${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    docker-compose -f docker-compose.backend.yml up -d --build
    echo ""
    echo -e "${GREEN}✓ Backend iniciado com sucesso!${NC}"
    echo ""
    echo -e "${YELLOW}📍 URLs disponíveis:${NC}"
    echo -e "   • API: http://localhost:8000"
    echo -e "   • Docs: http://localhost:8000/docs"
    echo -e "   • Banco: localhost:5441"
    ;;
  frontend)
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Iniciando Frontend${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    docker-compose -f docker-compose.frontend.yml up -d --build
    echo ""
    echo -e "${GREEN}✓ Frontend iniciado com sucesso!${NC}"
    echo ""
    echo -e "${YELLOW}📍 URL disponível:${NC}"
    echo -e "   • Frontend: http://localhost:3000"
    ;;
  all|*)
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Iniciando Backend (Banco + API)${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    docker-compose -f docker-compose.backend.yml up -d --build
    
    echo ""
    echo -e "${YELLOW}⏳ Aguardando backend ficar pronto...${NC}"
    sleep 8
    
    echo ""
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Iniciando Frontend${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    docker-compose -f docker-compose.frontend.yml up -d --build
    
    echo ""
    echo -e "${GREEN}✓ Todos os serviços iniciados com sucesso!${NC}"
    echo ""
    echo -e "${YELLOW}📍 URLs disponíveis:${NC}"
    echo -e "   • Frontend: http://localhost:3000"
    echo -e "   • API: http://localhost:8000"
    echo -e "   • Docs: http://localhost:8000/docs"
    ;;
esac
echo ""

