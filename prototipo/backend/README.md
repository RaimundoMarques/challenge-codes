# 🚀 Sistema de Ordens de Serviço - Backend

## 📋 Visão Geral

Este é o backend da aplicação de gerenciamento de ordens de serviço, construído com **FastAPI** e **PostgreSQL**. O sistema oferece uma API REST completa para gerenciar usuários, clientes, equipamentos, ordens de serviço, checklists e fotos de evidência.

## 🏗️ Arquitetura

### Tecnologias Utilizadas
- **FastAPI** - Framework web moderno e rápido
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para Python
- **JWT** - Autenticação via tokens
- **Bcrypt** - Hash de senhas
- **Docker** - Containerização

### Estrutura do Projeto
```
backend/
├── app/
│   ├── models/           # Modelos de dados e tabelas
│   ├── routers/          # Endpoints da API
│   ├── middleware/       # Middleware de autenticação
│   └── utils/            # Utilitários e segurança
├── requirements.txt      # Dependências Python
└── Dockerfile          # Configuração Docker
```

## 🔐 Sistema de Autenticação

### JWT (JSON Web Tokens)
- **Algoritmo**: HS256
- **Expiração**: 30 minutos
- **Refresh**: Automático via middleware
- **Revogação**: Tokens invalidados no logout

### Fluxo de Autenticação
1. **Login**: `POST /auth/login`
   - Validação de credenciais
   - Geração de JWT
   - Armazenamento no banco
2. **Proteção**: Middleware `get_current_active_user`
   - Validação de token
   - Verificação de expiração
   - Carregamento de usuário
3. **Logout**: `POST /auth/logout`
   - Revogação de token
   - Limpeza de sessão

### Níveis de Acesso
- **Administrador**: Acesso total ao sistema
- **Técnico**: Acesso limitado às suas ordens

## 📊 Modelos de Dados

### Principais Entidades
- **Users**: Usuários do sistema (admin/tecnico)
- **Clients**: Clientes atendidos
- **Equipments**: Equipamentos dos clientes
- **Service Orders**: Ordens de serviço
- **Checklists**: Listas de verificação
- **Photos**: Fotos de evidência

### Relacionamentos
```
Users (1) ←→ (N) Service Orders
Clients (1) ←→ (N) Equipments
Clients (1) ←→ (N) Service Orders
Equipments (1) ←→ (N) Service Orders
Service Orders (1) ←→ (N) Photos
Checklists (1) ←→ (N) Checklist Items
```

## 🛠️ Endpoints da API

### Autenticação
- `POST /auth/login` - Login de usuário
- `POST /auth/logout` - Logout de usuário
- `GET /auth/me` - Dados do usuário atual
- `POST /auth/verify-token` - Verificar token

### Usuários
- `GET /users/` - Listar usuários
- `GET /users/{id}` - Buscar usuário
- `POST /users/` - Criar usuário
- `PUT /users/{id}` - Atualizar usuário
- `DELETE /users/{id}` - Excluir usuário

### Ordens de Serviço
- `GET /orders/` - Listar ordens
- `GET /orders/{id}` - Buscar ordem
- `POST /orders/` - Criar ordem
- `PUT /orders/{id}` - Atualizar ordem
- `DELETE /orders/{id}` - Excluir ordem
- `PUT /orders/{id}/assign-technician` - Atribuir técnico

### Clientes
- `GET /orders/clients/` - Listar clientes
- `POST /orders/clients/` - Criar cliente
- `PUT /orders/clients/{id}` - Atualizar cliente
- `DELETE /orders/clients/{id}` - Excluir cliente

### Equipamentos
- `GET /orders/equipments/` - Listar equipamentos
- `POST /orders/equipments/` - Criar equipamento
- `PUT /orders/equipments/{id}` - Atualizar equipamento
- `DELETE /orders/equipments/{id}` - Excluir equipamento

### Fotos
- `POST /orders/{id}/photos` - Upload de foto
- `GET /orders/{id}/photos` - Listar fotos
- `DELETE /orders/photos/{id}` - Excluir foto
- `GET /orders/uploads/{filename}` - Servir arquivo

### Checklists
- `GET /orders/checklists/` - Listar checklists
- `POST /orders/{id}/checklist-responses/` - Salvar respostas

## 🔧 Configuração e Instalação

### Variáveis de Ambiente
```env
# Database
DB_HOST=db-postgres
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=postgres

# Security
SECRET_KEY=your-secret-key-change-in-production
```

### Instalação Local
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker
```bash
# Build e execução
docker-compose up -d --build

# Logs
docker-compose logs -f api
```

## 📁 Estrutura de Arquivos

### Models (`app/models/`)
- `database.py` - Configuração do SQLAlchemy
- `auth.py` - Tabelas de autenticação
- `orders.py` - Tabelas de ordens
- `auth_models.py` - Modelos Pydantic de auth
- `order_models.py` - Modelos Pydantic de ordens

### Routers (`app/routers/`)
- `auth.py` - Endpoints de autenticação
- `users.py` - Endpoints de usuários
- `orders.py` - Endpoints de ordens

### Middleware (`app/middleware/`)
- `auth.py` - Middleware de autenticação JWT

### Utils (`app/utils/`)
- `security.py` - Funções de segurança e hash

## 🔒 Segurança

### Hash de Senhas
- **Algoritmo**: Bcrypt
- **Salt**: Automático
- **Rounds**: 12

### Validação de Dados
- **Pydantic**: Validação automática
- **Sanitização**: Inputs limpos
- **SQL Injection**: Proteção via SQLAlchemy

### CORS
- **Origins**: `http://localhost:3000`
- **Methods**: Todos permitidos
- **Headers**: Todos permitidos

## 📈 Performance

### Otimizações
- **Connection Pooling**: SQLAlchemy
- **Lazy Loading**: Relacionamentos
- **Indexes**: Chaves primárias e estrangeiras
- **Caching**: Tokens em memória

### Monitoramento
- **Logs**: Estruturados
- **Health Check**: `/` endpoint
- **Metrics**: FastAPI automático

## 🚀 Deploy

### Produção
1. **Variáveis**: Configurar `.env`
2. **Database**: Migrar schema
3. **SSL**: Configurar certificados
4. **Reverse Proxy**: Nginx/Apache
5. **Monitoring**: Logs e métricas

### Docker Production
```dockerfile
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /code
WORKDIR /code
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📚 Documentação

### Swagger UI
- **URL**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Exemplos de Uso
```python
# Login
response = requests.post('http://localhost:8000/auth/login', json={
    'username': 'admin',
    'password': '123456'
})
token = response.json()['access_token']

# Request autenticado
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/users/', headers=headers)
```

## 🐛 Troubleshooting

### Problemas Comuns
1. **Database Connection**: Verificar variáveis de ambiente
2. **JWT Invalid**: Verificar SECRET_KEY
3. **CORS Error**: Verificar configuração de origins
4. **Permission Denied**: Verificar roles de usuário

### Logs
```bash
# Docker logs
docker-compose logs api

# Debug mode
uvicorn app.main:app --reload --log-level debug
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar logs da aplicação
2. Consultar documentação Swagger
3. Verificar configuração de ambiente
4. Testar endpoints individualmente

---

**Desenvolvido com FastAPI + PostgreSQL**
