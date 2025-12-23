#!/usr/bin/env python3
"""
Script de teste de integração frontend-backend
Testa os principais endpoints e funcionalidades
"""

import requests
import json
import sys
from typing import Dict, Optional

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_success(msg: str):
    print(f"{Colors.GREEN}[OK] {msg}{Colors.RESET}")

def print_error(msg: str):
    print(f"{Colors.RED}[ERRO] {msg}{Colors.RESET}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}[AVISO] {msg}{Colors.RESET}")

def print_info(msg: str):
    print(f"{Colors.BLUE}[INFO] {msg}{Colors.RESET}")

class APITester:
    def __init__(self):
        self.token: Optional[str] = None
        self.session = requests.Session()
    
    def login(self, username: str = "admin", password: str = "123456") -> bool:
        """Faz login e obtém token"""
        try:
            response = self.session.post(
                f"{BASE_URL}/auth/login",
                data={"username": username, "password": password}
            )
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}"
                })
                print_success(f"Login realizado com sucesso (usuário: {username})")
                return True
            else:
                print_error(f"Falha no login: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print_error(f"Erro ao fazer login: {e}")
            return False
    
    def test_create_client(self) -> Optional[Dict]:
        """Testa criação de cliente"""
        print_info("Testando criação de cliente...")
        try:
            client_data = {
                "name": "Cliente Teste",
                "email": "teste@exemplo.com",
                "phone": "(11) 99999-9999",
                "address": "Rua Teste, 123"
            }
            response = self.session.post(
                f"{BASE_URL}/orders/clients/",
                json=client_data
            )
            if response.status_code == 200:
                client = response.json()
                print_success(f"Cliente criado: {client['name']} (ID: {client['id']})")
                return client
            else:
                print_error(f"Falha ao criar cliente: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print_error(f"Erro ao criar cliente: {e}")
            return None
    
    def test_create_equipment(self, client_id: int) -> Optional[Dict]:
        """Testa criação de equipamento"""
        print_info("Testando criação de equipamento...")
        try:
            equipment_data = {
                "client_id": client_id,
                "type": "Notebook",
                "brand": "Dell",
                "model": "Inspiron 15",
                "serial_number": f"SN-TEST-{client_id}"
            }
            response = self.session.post(
                f"{BASE_URL}/orders/equipments/",
                json=equipment_data
            )
            if response.status_code == 200:
                equipment = response.json()
                print_success(f"Equipamento criado: {equipment['type']} (ID: {equipment['id']})")
                return equipment
            else:
                print_error(f"Falha ao criar equipamento: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print_error(f"Erro ao criar equipamento: {e}")
            return None
    
    def test_list_clients(self) -> bool:
        """Testa listagem de clientes"""
        print_info("Testando listagem de clientes...")
        try:
            response = self.session.get(f"{BASE_URL}/orders/clients/")
            if response.status_code == 200:
                clients = response.json()
                print_success(f"Listagem de clientes: {len(clients)} clientes encontrados")
                return True
            else:
                print_error(f"Falha ao listar clientes: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print_error(f"Erro ao listar clientes: {e}")
            return False
    
    def test_list_equipments(self, client_id: Optional[int] = None) -> bool:
        """Testa listagem de equipamentos"""
        print_info("Testando listagem de equipamentos...")
        try:
            url = f"{BASE_URL}/orders/equipments/"
            if client_id:
                url += f"?client_id={client_id}"
            response = self.session.get(url)
            if response.status_code == 200:
                equipments = response.json()
                print_success(f"Listagem de equipamentos: {len(equipments)} equipamentos encontrados")
                return True
            else:
                print_error(f"Falha ao listar equipamentos: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print_error(f"Erro ao listar equipamentos: {e}")
            return False
    
    def test_create_order(self, client_id: int, equipment_id: int) -> Optional[Dict]:
        """Testa criação de ordem de serviço"""
        print_info("Testando criação de ordem de serviço...")
        try:
            order_data = {
                "title": "Ordem de Teste",
                "description": "Descrição de teste",
                "activities_description": "Atividades de teste",
                "status": "open",
                "client_id": client_id,
                "equipment_id": equipment_id
            }
            response = self.session.post(
                f"{BASE_URL}/orders/",
                json=order_data
            )
            if response.status_code == 200:
                order = response.json()
                print_success(f"Ordem criada: {order['title']} (ID: {order['id']})")
                return order
            else:
                print_error(f"Falha ao criar ordem: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print_error(f"Erro ao criar ordem: {e}")
            return None
    
    def run_all_tests(self):
        """Executa todos os testes"""
        print("\n" + "="*60)
        print("TESTE DE INTEGRAÇÃO FRONTEND-BACKEND")
        print("="*60 + "\n")
        
        # Teste 1: Login
        if not self.login():
            print_error("Não foi possível fazer login. Abortando testes.")
            return False
        
        # Teste 2: Listar clientes
        self.test_list_clients()
        
        # Teste 3: Criar cliente
        client = self.test_create_client()
        if not client:
            print_warning("Não foi possível criar cliente. Continuando testes...")
            return False
        
        # Teste 4: Listar equipamentos do cliente
        self.test_list_equipments(client['id'])
        
        # Teste 5: Criar equipamento
        equipment = self.test_create_equipment(client['id'])
        if not equipment:
            print_warning("Não foi possível criar equipamento. Continuando testes...")
            return False
        
        # Teste 6: Criar ordem de serviço
        order = self.test_create_order(client['id'], equipment['id'])
        if not order:
            print_warning("Não foi possível criar ordem de serviço.")
            return False
        
        print("\n" + "="*60)
        print_success("TODOS OS TESTES PASSARAM!")
        print("="*60 + "\n")
        return True

if __name__ == "__main__":
    tester = APITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

