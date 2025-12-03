#!/bin/bash

# Script de teste completo para os endpoints da API
# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

API_URL="http://localhost:8000"
TOKEN=""
USER_ID=""
ORDER_ID=""

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}🧪 TESTE COMPLETO DOS ENDPOINTS${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Função para fazer requisições
test_endpoint() {
    local method=$1
    local endpoint=$2
    local data=$3
    local description=$4
    local auth=$5
    
    echo -e "${YELLOW}Testing: ${description}${NC}"
    echo -e "  ${BLUE}${method} ${endpoint}${NC}"
    
    if [ "$auth" = "true" ] && [ -z "$TOKEN" ]; then
        echo -e "  ${RED}❌ SKIP - Token não disponível${NC}"
        return 1
    fi
    
    headers="-H 'Content-Type: application/json'"
    if [ "$auth" = "true" ]; then
        headers="$headers -H 'Authorization: Bearer $TOKEN'"
    fi
    
    if [ -n "$data" ]; then
        response=$(eval curl -s -w "\n%{http_code}" -X $method "$API_URL$endpoint" $headers -d "'$data'")
    else
        response=$(eval curl -s -w "\n%{http_code}" -X $method "$API_URL$endpoint" $headers)
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "  ${GREEN}✅ SUCCESS (HTTP $http_code)${NC}"
        echo "$body" | head -c 200
        echo ""
        return 0
    else
        echo -e "  ${RED}❌ FAILED (HTTP $http_code)${NC}"
        echo "$body" | head -c 300
        echo ""
        return 1
    fi
}

# ============================================
# 1. TESTE DE AUTENTICAÇÃO
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}1️⃣  TESTANDO AUTENTICAÇÃO${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 1.1 Login
echo "1.1 Login"
response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"username": "admin", "password": "123456"}')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" -eq 200 ]; then
    echo -e "${GREEN}✅ Login bem-sucedido${NC}"
    TOKEN=$(echo "$body" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    if [ -n "$TOKEN" ]; then
        echo -e "${GREEN}✅ Token obtido: ${TOKEN:0:50}...${NC}"
        USER_ID=$(echo "$body" | grep -o '"id":[0-9]*' | cut -d':' -f2)
    fi
else
    echo -e "${RED}❌ Falha no login (HTTP $http_code)${NC}"
    echo "$body"
    exit 1
fi
echo ""

# 1.2 Get Current User (me)
test_endpoint "GET" "/auth/me" "" "1.2 Get Current User" "true"
echo ""

# 1.3 Verify Token
test_endpoint "POST" "/auth/verify-token" "" "1.3 Verify Token" "true"
echo ""

# ============================================
# 2. TESTE DE USUÁRIOS
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}2️⃣  TESTANDO USUÁRIOS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 2.1 List Users
test_endpoint "GET" "/users/" "" "2.1 List Users" "true"
echo ""

# 2.2 Create User
test_data='{"username": "teste_user_'$(date +%s)'", "password": "123456", "name": "Usuário Teste", "email": "teste@teste.com", "role": "tecnico"}'
response=$(test_endpoint "POST" "/users/" "$test_data" "2.2 Create User" "true")
NEW_USER_ID=$(echo "$response" | grep -o '"id":[0-9]*' | cut -d':' -f2 | head -1)
echo ""

# 2.3 Get User by ID
if [ -n "$USER_ID" ]; then
    test_endpoint "GET" "/users/$USER_ID" "" "2.3 Get User by ID" "true"
    echo ""
fi

# ============================================
# 3. TESTE DE ORDENS DE SERVIÇO
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}3️⃣  TESTANDO ORDENS DE SERVIÇO${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 3.1 List Orders
test_endpoint "GET" "/orders/" "" "3.1 List Orders" "true"
echo ""

# 3.2 List Technicians
test_endpoint "GET" "/orders/technicians/" "" "3.2 List Technicians" "true"
echo ""

# 3.3 List Clients
test_endpoint "GET" "/orders/clients/" "" "3.3 List Clients" "true"
CLIENT_ID=$(curl -s -X GET "$API_URL/orders/clients/" \
    -H "Authorization: Bearer $TOKEN" | grep -o '"id":[0-9]*' | cut -d':' -f2 | head -1)
echo ""

# 3.4 List Equipments
if [ -n "$CLIENT_ID" ]; then
    test_endpoint "GET" "/orders/equipments/?client_id=$CLIENT_ID" "" "3.4 List Equipments by Client" "true"
    EQUIPMENT_ID=$(curl -s -X GET "$API_URL/orders/equipments/?client_id=$CLIENT_ID" \
        -H "Authorization: Bearer $TOKEN" | grep -o '"id":[0-9]*' | cut -d':' -f2 | head -1)
else
    test_endpoint "GET" "/orders/equipments/" "" "3.4 List All Equipments" "true"
    EQUIPMENT_ID=$(curl -s -X GET "$API_URL/orders/equipments/" \
        -H "Authorization: Bearer $TOKEN" | grep -o '"id":[0-9]*' | cut -d':' -f2 | head -1)
fi
echo ""

# 3.5 Create Order
if [ -n "$CLIENT_ID" ] && [ -n "$EQUIPMENT_ID" ] && [ -n "$USER_ID" ]; then
    test_data="{\"title\": \"Ordem de Teste $(date +%H:%M:%S)\", \"description\": \"Descrição de teste\", \"status\": \"open\", \"client_id\": $CLIENT_ID, \"equipment_id\": $EQUIPMENT_ID}"
    response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/orders/" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d "$test_data")
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq 200 ]; then
        echo -e "${GREEN}✅ 3.5 Create Order - SUCCESS${NC}"
        ORDER_ID=$(echo "$body" | grep -o '"id":[0-9]*' | cut -d':' -f2 | head -1)
        echo "  Order ID: $ORDER_ID"
    else
        echo -e "${RED}❌ 3.5 Create Order - FAILED (HTTP $http_code)${NC}"
        echo "$body"
    fi
fi
echo ""

# 3.6 Get Order by ID
if [ -n "$ORDER_ID" ]; then
    test_endpoint "GET" "/orders/$ORDER_ID" "" "3.6 Get Order by ID" "true"
    echo ""
fi

# 3.7 List Checklists
test_endpoint "GET" "/orders/checklists/" "" "3.7 List Checklists" "true"
echo ""

# ============================================
# 4. TESTE DE CLIENTES
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}4️⃣  TESTANDO CLIENTES${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 4.1 Create Client
test_data='{"name": "Cliente Teste '$(date +%s)'", "email": "cliente@teste.com", "phone": "(92) 99999-9999", "address": "Endereço de teste"}'
test_endpoint "POST" "/orders/clients/" "$test_data" "4.1 Create Client" "true"
echo ""

# ============================================
# 5. TESTE DE EQUIPAMENTOS
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}5️⃣  TESTANDO EQUIPAMENTOS${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 5.1 Create Equipment
if [ -n "$CLIENT_ID" ]; then
    test_data="{\"type\": \"Notebook\", \"brand\": \"Dell\", \"model\": \"Inspiron Test\", \"serial_number\": \"SN-TEST-$(date +%s)\", \"client_id\": $CLIENT_ID}"
    test_endpoint "POST" "/orders/equipments/" "$test_data" "5.1 Create Equipment" "true"
    echo ""
fi

# ============================================
# 6. TESTE DE ATUALIZAÇÃO
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}6️⃣  TESTANDO ATUALIZAÇÕES${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 6.1 Update Order
if [ -n "$ORDER_ID" ]; then
    test_data='{"status": "in_progress", "description": "Descrição atualizada"}'
    test_endpoint "PUT" "/orders/$ORDER_ID" "$test_data" "6.1 Update Order" "true"
    echo ""
fi

# ============================================
# 7. TESTE DE LOGOUT
# ============================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}7️⃣  TESTANDO LOGOUT${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 7.1 Logout
test_endpoint "POST" "/auth/logout" "" "7.1 Logout" "true"
echo ""

# ============================================
# RESUMO
# ============================================
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}📊 RESUMO DOS TESTES${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Token usado: ${TOKEN:0:50}..."
if [ -n "$ORDER_ID" ]; then
    echo -e "Order ID criado: $ORDER_ID"
fi
if [ -n "$NEW_USER_ID" ]; then
    echo -e "User ID criado: $NEW_USER_ID"
fi
echo ""
echo -e "${GREEN}✅ Testes concluídos!${NC}"
echo ""

