#!/usr/bin/env python3
"""
Script de teste completo para os endpoints da API
"""
import requests
import json
import sys
from datetime import datetime
from typing import Dict, Optional

# Configurações
API_URL = "http://localhost:8000"
TOKEN: Optional[str] = None
USER_ID: Optional[int] = None
ORDER_ID: Optional[int] = None
CLIENT_ID: Optional[int] = None
EQUIPMENT_ID: Optional[int] = None

# Cores para output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

def print_header(title: str):
    """Imprime cabeçalho formatado"""
    print(f"\n{Colors.BLUE}{'='*50}{Colors.NC}")
    print(f"{Colors.BLUE}{title}{Colors.NC}")
    print(f"{Colors.BLUE}{'='*50}{Colors.NC}\n")

def print_test(test_name: str, endpoint: str, method: str = "GET"):
    """Imprime informações do teste"""
    print(f"{Colors.YELLOW}>> {test_name}{Colors.NC}")
    print(f"   {Colors.CYAN}{method} {endpoint}{Colors.NC}")

def test_endpoint(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
    description: str = "",
    require_auth: bool = False,
    expected_status: int = 200
) -> tuple[bool, Dict]:
    """
    Testa um endpoint e retorna sucesso e dados da resposta
    """
    global TOKEN
    
    if require_auth and not TOKEN:
        print(f"   {Colors.RED}[X] SKIP - Token não disponível{Colors.NC}\n")
        return False, {}
    
    headers = {"Content-Type": "application/json"}
    if require_auth:
        headers["Authorization"] = f"Bearer {TOKEN}"
    
    try:
        url = f"{API_URL}{endpoint}"
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=10)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        else:
            print(f"   {Colors.RED}[X] Método {method} não suportado{Colors.NC}\n")
            return False, {}
        
        if response.status_code == expected_status:
            print(f"   {Colors.GREEN}[OK] SUCCESS (HTTP {response.status_code}){Colors.NC}")
            try:
                response_data = response.json()
                # Mostrar preview da resposta
                preview = json.dumps(response_data, indent=2, ensure_ascii=False)[:300]
                if len(json.dumps(response_data)) > 300:
                    preview += "..."
                print(f"   {preview}")
            except:
                print(f"   {response.text[:200]}")
            print()
            return True, response.json() if response.text else {}
        else:
            print(f"   {Colors.RED}[X] FAILED (HTTP {response.status_code}){Colors.NC}")
            try:
                error_data = response.json()
                print(f"   {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"   {response.text[:300]}")
            print()
            return False, {}
            
    except requests.exceptions.ConnectionError:
        print(f"   {Colors.RED}[X] ERRO: Não foi possível conectar à API em {API_URL}{Colors.NC}")
        print(f"   {Colors.YELLOW}Verifique se a API está rodando{Colors.NC}\n")
        return False, {}
    except Exception as e:
        print(f"   {Colors.RED}[X] ERRO: {str(e)}{Colors.NC}\n")
        return False, {}


def main():
    """Executa todos os testes"""
    global TOKEN, USER_ID, ORDER_ID, CLIENT_ID, EQUIPMENT_ID
    
    print(f"{Colors.BLUE}{'='*50}{Colors.NC}")
    print(f"{Colors.BLUE}TESTE COMPLETO DOS ENDPOINTS{Colors.NC}")
    print(f"{Colors.BLUE}{'='*50}{Colors.NC}")
    print(f"API URL: {API_URL}")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skipped": 0
    }
    
    # ============================================
    # 1. TESTE DE AUTENTICAÇÃO
    # ============================================
    print_header("1. TESTANDO AUTENTICACAO")
    
    # 1.1 Login
    print_test("1.1 Login", "/auth/login", "POST")
    success, data = test_endpoint(
        "POST",
        "/auth/login",
        {"username": "admin", "password": "123456"},
        expected_status=200
    )
    results["total"] += 1
    if success:
        results["passed"] += 1
        TOKEN = data.get("access_token")
        if "user" in data:
            USER_ID = data["user"].get("id")
        print(f"   {Colors.GREEN}Token obtido: {TOKEN[:50] if TOKEN else 'N/A'}...{Colors.NC}")
        if USER_ID:
            print(f"   {Colors.GREEN}User ID: {USER_ID}{Colors.NC}")
        print()
    else:
        results["failed"] += 1
        print(f"{Colors.RED}[X] Não foi possível fazer login. Testes subsequentes serão pulados.{Colors.NC}\n")
        return
    
    # 1.2 Get Current User
    print_test("1.2 Get Current User", "/auth/me")
    results["total"] += 1
    if test_endpoint("GET", "/auth/me", require_auth=True)[0]:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # 1.3 Verify Token
    print_test("1.3 Verify Token", "/auth/verify-token", "POST")
    results["total"] += 1
    if test_endpoint("POST", "/auth/verify-token", require_auth=True)[0]:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # ============================================
    # 2. TESTE DE USUÁRIOS
    # ============================================
    print_header("2. TESTANDO USUARIOS")
    
    # 2.1 List Users
    print_test("2.1 List Users", "/users/")
    results["total"] += 1
    if test_endpoint("GET", "/users/", require_auth=True)[0]:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # 2.2 Create User
    timestamp = int(datetime.now().timestamp())
    print_test("2.2 Create User", "/users/", "POST")
    results["total"] += 1
    success, data = test_endpoint(
        "POST",
        "/users/",
        {
            "username": f"teste_user_{timestamp}",
            "password": "123456",
            "name": "Usuário Teste",
            "email": f"teste_{timestamp}@teste.com",
            "role": "tecnico"
        },
        require_auth=True
    )
    if success:
        results["passed"] += 1
        if "id" in data:
            print(f"   {Colors.GREEN}[OK] Usuário criado com ID: {data['id']}{Colors.NC}\n")
    else:
        results["failed"] += 1
    
    # 2.3 Get User by ID
    if USER_ID:
        print_test(f"2.3 Get User by ID ({USER_ID})", f"/users/{USER_ID}")
        results["total"] += 1
        if test_endpoint("GET", f"/users/{USER_ID}", require_auth=True)[0]:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # ============================================
    # 3. TESTE DE ORDENS DE SERVIÇO
    # ============================================
    print_header("3. TESTANDO ORDENS DE SERVICO")
    
    # 3.1 List Orders
    print_test("3.1 List Orders", "/orders/")
    results["total"] += 1
    if test_endpoint("GET", "/orders/", require_auth=True)[0]:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # 3.2 List Technicians
    print_test("3.2 List Technicians", "/orders/technicians/")
    results["total"] += 1
    if test_endpoint("GET", "/orders/technicians/", require_auth=True)[0]:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # 3.3 List Clients
    print_test("3.3 List Clients", "/orders/clients/")
    results["total"] += 1
    success, data = test_endpoint("GET", "/orders/clients/", require_auth=True)
    if success:
        results["passed"] += 1
        if isinstance(data, list) and len(data) > 0:
            CLIENT_ID = data[0].get("id")
            print(f"   {Colors.GREEN}[OK] Client ID disponível: {CLIENT_ID}{Colors.NC}\n")
    else:
        results["failed"] += 1
    
    # 3.4 List Equipments
    if CLIENT_ID:
        print_test(f"3.4 List Equipments (client_id={CLIENT_ID})", f"/orders/equipments/?client_id={CLIENT_ID}")
    else:
        print_test("3.4 List All Equipments", "/orders/equipments/")
    results["total"] += 1
    endpoint = f"/orders/equipments/?client_id={CLIENT_ID}" if CLIENT_ID else "/orders/equipments/"
    success, data = test_endpoint("GET", endpoint, require_auth=True)
    if success:
        results["passed"] += 1
        if isinstance(data, list) and len(data) > 0:
            EQUIPMENT_ID = data[0].get("id")
            print(f"   {Colors.GREEN}[OK] Equipment ID disponível: {EQUIPMENT_ID}{Colors.NC}\n")
    else:
        results["failed"] += 1
    
    # 3.5 Create Order
    if CLIENT_ID and EQUIPMENT_ID and USER_ID:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print_test("3.5 Create Order", "/orders/", "POST")
        results["total"] += 1
        success, data = test_endpoint(
            "POST",
            "/orders/",
            {
                "title": f"Ordem de Teste {timestamp}",
                "description": "Descrição de teste automatizado",
                "status": "open",
                "client_id": CLIENT_ID,
                "equipment_id": EQUIPMENT_ID
            },
            require_auth=True
        )
        if success:
            results["passed"] += 1
            ORDER_ID = data.get("id")
            if ORDER_ID:
                print(f"   {Colors.GREEN}[OK] Order criada com ID: {ORDER_ID}{Colors.NC}\n")
        else:
            results["failed"] += 1
    else:
        print_test("3.5 Create Order", "/orders/", "POST")
        print(f"   {Colors.YELLOW}[!]  SKIP - Dados necessários não disponíveis{Colors.NC}\n")
        results["skipped"] += 1
    
    # 3.6 Get Order by ID
    if ORDER_ID:
        print_test(f"3.6 Get Order by ID ({ORDER_ID})", f"/orders/{ORDER_ID}")
        results["total"] += 1
        if test_endpoint("GET", f"/orders/{ORDER_ID}", require_auth=True)[0]:
            results["passed"] += 1
        else:
            results["failed"] += 1
    
    # 3.7 List Checklists
    print_test("3.7 List Checklists", "/orders/checklists/")
    results["total"] += 1
    if test_endpoint("GET", "/orders/checklists/", require_auth=True)[0]:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # ============================================
    # 4. TESTE DE CLIENTES
    # ============================================
    print_header("4. TESTANDO CLIENTES")
    
    # 4.1 Create Client
    timestamp = int(datetime.now().timestamp())
    print_test("4.1 Create Client", "/orders/clients/", "POST")
    results["total"] += 1
    success, data = test_endpoint(
        "POST",
        "/orders/clients/",
        {
            "name": f"Cliente Teste {timestamp}",
            "email": f"cliente_{timestamp}@teste.com",
            "phone": "(92) 99999-9999",
            "address": "Endereço de teste"
        },
        require_auth=True
    )
    if success:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # ============================================
    # 5. TESTE DE EQUIPAMENTOS
    # ============================================
    print_header("5. TESTANDO EQUIPAMENTOS")
    
    # 5.1 Create Equipment
    if CLIENT_ID:
        timestamp = int(datetime.now().timestamp())
        print_test("5.1 Create Equipment", "/orders/equipments/", "POST")
        results["total"] += 1
        success, data = test_endpoint(
            "POST",
            "/orders/equipments/",
            {
                "type": "Notebook",
                "brand": "Dell",
                "model": "Inspiron Test",
                "serial_number": f"SN-TEST-{timestamp}",
                "client_id": CLIENT_ID
            },
            require_auth=True
        )
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
    else:
        print_test("5.1 Create Equipment", "/orders/equipments/", "POST")
        print(f"   {Colors.YELLOW}[!]  SKIP - Client ID não disponível{Colors.NC}\n")
        results["skipped"] += 1
    
    # ============================================
    # 6. TESTE DE ATUALIZAÇÃO
    # ============================================
    print_header("6. TESTANDO ATUALIZACOES")
    
    # 6.1 Update Order
    if ORDER_ID:
        print_test(f"6.1 Update Order ({ORDER_ID})", f"/orders/{ORDER_ID}", "PUT")
        results["total"] += 1
        success, data = test_endpoint(
            "PUT",
            f"/orders/{ORDER_ID}",
            {
                "status": "in_progress",
                "description": "Descrição atualizada por teste automatizado"
            },
            require_auth=True
        )
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
    else:
        print_test("6.1 Update Order", "/orders/{id}", "PUT")
        print(f"   {Colors.YELLOW}[!]  SKIP - Order ID não disponível{Colors.NC}\n")
        results["skipped"] += 1
    
    # ============================================
    # 7. TESTE DE LOGOUT
    # ============================================
    print_header("7. TESTANDO LOGOUT")
    
    # 7.1 Logout
    print_test("7.1 Logout", "/auth/logout", "POST")
    results["total"] += 1
    if test_endpoint("POST", "/auth/logout", require_auth=True)[0]:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # ============================================
    # RESUMO
    # ============================================
    print_header("RESUMO DOS TESTES")
    
    print(f"Total de testes: {results['total']}")
    print(f"{Colors.GREEN}[OK] Passou: {results['passed']}{Colors.NC}")
    print(f"{Colors.RED}[X] Falhou: {results['failed']}{Colors.NC}")
    if results['skipped'] > 0:
        print(f"{Colors.YELLOW}[!]  Pulado: {results['skipped']}{Colors.NC}")
    
    success_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
    print(f"\nTaxa de sucesso: {success_rate:.1f}%")
    
    if results['failed'] == 0:
        print(f"\n{Colors.GREEN}*** Todos os testes passaram! ***{Colors.NC}\n")
        return 0
    else:
        print(f"\n{Colors.RED}[!]  Alguns testes falharam. Verifique os logs acima.{Colors.NC}\n")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Testes interrompidos pelo usuario{Colors.NC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}[X] Erro inesperado: {str(e)}{Colors.NC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

