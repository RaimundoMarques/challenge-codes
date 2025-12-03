#!/bin/bash

# Script simples para parar serviços
# Uso: ./stop.sh [backend|frontend|all]

SERVICE=${1:-all}

# Cores para output
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo ""
case $SERVICE in
  backend)
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${RED}  Parando Backend (Banco + API)${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    docker-compose -f docker-compose.backend.yml down
    echo ""
    echo -e "${GREEN}✓ Backend parado com sucesso!${NC}"
    ;;
  frontend)
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${RED}  Parando Frontend${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    docker-compose -f docker-compose.frontend.yml down
    echo ""
    echo -e "${GREEN}✓ Frontend parado com sucesso!${NC}"
    ;;
  all|*)
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${RED}  Parando todos os serviços${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo "Parando Frontend..."
    docker-compose -f docker-compose.frontend.yml down
    echo ""
    echo "Parando Backend..."
    docker-compose -f docker-compose.backend.yml down
    echo ""
    echo -e "${GREEN}✓ Todos os serviços parados com sucesso!${NC}"
    ;;
esac
echo ""

