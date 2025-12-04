#!/bin/bash

# Script simples para parar serviços
# Uso: ./stop.sh [backend|frontend|all]

# Cores para output
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar se o Docker está rodando
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo ""
        echo -e "${RED}════════════════════════════════════════${NC}"
        echo -e "${RED}  ❌ Docker não está rodando!${NC}"
        echo -e "${RED}════════════════════════════════════════${NC}"
        echo ""
        echo -e "${YELLOW}Por favor, inicie o Docker Desktop e tente novamente.${NC}"
        echo ""
        echo -e "No Windows/WSL:"
        echo -e "  1. Abra o Docker Desktop"
        echo -e "  2. Configure a integração WSL no Docker Desktop (Settings > Resources > WSL Integration)"
        echo -e "  3. Aguarde o Docker inicializar completamente"
        echo -e "  4. Execute o script novamente"
        echo ""
        exit 1
    fi
}

# Função wrapper para executar Docker Compose
# Detecta automaticamente se usar 'docker compose' (V2) ou 'docker-compose' (V1)
docker_compose() {
    if docker compose version > /dev/null 2>&1; then
        docker compose "$@"
    elif docker-compose version > /dev/null 2>&1; then
        docker-compose "$@"
    else
        # Se não encontrar, tenta docker-compose como último recurso
        docker-compose "$@"
    fi
}

# Verificar Docker antes de continuar (opcional para stop, mas útil)
check_docker 2>/dev/null || true

SERVICE=${1:-all}

echo ""
case $SERVICE in
  backend)
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${RED}  Parando Backend (Banco + API)${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    docker_compose -f docker-compose.backend.yml down 2>/dev/null || echo -e "${YELLOW}  ⚠ Backend já estava parado ou não existe${NC}"
    echo ""
    echo -e "${GREEN}✓ Backend parado com sucesso!${NC}"
    ;;
  frontend)
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${RED}  Parando Frontend${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    docker_compose -f docker-compose.frontend.yml down 2>/dev/null || echo -e "${YELLOW}  ⚠ Frontend já estava parado ou não existe${NC}"
    echo ""
    echo -e "${GREEN}✓ Frontend parado com sucesso!${NC}"
    ;;
  all|*)
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${RED}  Parando todos os serviços${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    echo "Parando Frontend..."
    docker_compose -f docker-compose.frontend.yml down 2>/dev/null || echo -e "${YELLOW}  ⚠ Frontend já estava parado ou não existe${NC}"
    echo ""
    echo "Parando Backend..."
    docker_compose -f docker-compose.backend.yml down 2>/dev/null || echo -e "${YELLOW}  ⚠ Backend já estava parado ou não existe${NC}"
    echo ""
    echo -e "${GREEN}✓ Todos os serviços parados com sucesso!${NC}"
    ;;
esac
echo ""

