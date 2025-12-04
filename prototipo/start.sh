#!/bin/bash

# Script simples para iniciar serviços
# Uso: ./start.sh [backend|frontend|all]

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
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
        echo ""
        echo -e "${RED}════════════════════════════════════════${NC}"
        echo -e "${RED}  ❌ Docker Compose não encontrado!${NC}"
        echo -e "${RED}════════════════════════════════════════${NC}"
        echo ""
        echo -e "${YELLOW}Por favor, instale o Docker Compose ou habilite a integração WSL no Docker Desktop.${NC}"
        echo ""
        echo -e "No WSL 2:"
        echo -e "  1. Abra o Docker Desktop"
        echo -e "  2. Vá em Settings > Resources > WSL Integration"
        echo -e "  3. Ative a integração para sua distribuição WSL"
        echo -e "  4. Reinicie o Docker Desktop"
        echo ""
        exit 1
    fi
}

# Verificar Docker antes de continuar
check_docker

SERVICE=${1:-all}

echo ""
case $SERVICE in
  backend)
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Iniciando Backend (Banco + API)${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    if docker_compose -f docker-compose.backend.yml up -d --build; then
        echo ""
        echo -e "${GREEN}✓ Backend iniciado com sucesso!${NC}"
    else
        echo ""
        echo -e "${RED}❌ Erro ao iniciar o backend${NC}"
        exit 1
    fi
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
    if docker_compose -f docker-compose.frontend.yml up -d --build; then
        echo ""
        echo -e "${GREEN}✓ Frontend iniciado com sucesso!${NC}"
    else
        echo ""
        echo -e "${RED}❌ Erro ao iniciar o frontend${NC}"
        exit 1
    fi
    echo ""
    echo -e "${YELLOW}📍 URL disponível:${NC}"
    echo -e "   • Frontend: http://localhost:3000"
    ;;
  all|*)
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}  Iniciando Backend (Banco + API)${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo ""
    if docker_compose -f docker-compose.backend.yml up -d --build; then
        echo ""
        echo -e "${YELLOW}⏳ Aguardando backend ficar pronto...${NC}"
        sleep 8
        
        echo ""
        echo -e "${BLUE}════════════════════════════════════════${NC}"
        echo -e "${BLUE}  Iniciando Frontend${NC}"
        echo -e "${BLUE}════════════════════════════════════════${NC}"
        echo ""
        if docker_compose -f docker-compose.frontend.yml up -d --build; then
            echo ""
            echo -e "${GREEN}✓ Todos os serviços iniciados com sucesso!${NC}"
        else
            echo ""
            echo -e "${RED}❌ Erro ao iniciar o frontend${NC}"
            exit 1
        fi
    else
        echo ""
        echo -e "${RED}❌ Erro ao iniciar o backend${NC}"
        exit 1
    fi
    echo ""
    echo -e "${YELLOW}📍 URLs disponíveis:${NC}"
    echo -e "   • Frontend: http://localhost:3000"
    echo -e "   • API: http://localhost:8000"
    echo -e "   • Docs: http://localhost:8000/docs"
    ;;
esac
echo ""

