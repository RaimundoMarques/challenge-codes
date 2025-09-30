# 🛠️ Sistema de Ordens de Serviço

Sistema completo para gerenciamento de ordens de serviço com autenticação, checklist de atividades e upload de fotos comprovantes.

## 📋 Funcionalidades

### ✅ **Implementadas**
- **🔐 Autenticação JWT**: Login seguro com tokens
- **👥 Gestão de Usuários**: CRUD completo (Criar, Listar, Editar, Excluir)
- **📋 Ordens de Serviço**: Criação, listagem e atribuição de técnicos
- **✅ Checklist de Atividades**: Preenchimento de checklists configuráveis
- **📝 Descrição de Atividades**: Campo para detalhar atividades realizadas
- **📸 Upload de Fotos**: Sistema de fotos comprovantes
- **🎯 Atribuição de Técnicos**: Sistema de assign/reassign de técnicos
- **🔒 Controle de Acesso**: Permissões por role (admin/tecnico)

### 🎨 **Interface**
- **📱 Responsiva**: Funciona em desktop, tablet e mobile
- **🎨 Design Moderno**: Interface limpa e intuitiva
- **⚡ Estados de Loading**: Feedback visual durante operações
- **🚨 Tratamento de Erros**: Mensagens claras e informativas

## 🏗️ Arquitetura

### **Backend (FastAPI)**
- **Python 3.11+** com FastAPI
- **PostgreSQL** como banco de dados
- **SQLAlchemy** como ORM
- **JWT** para autenticação
- **Bcrypt** para hash de senhas
- **Pydantic** para validação de dados

### **Frontend (Vue.js)**
- **Vue 3** com Composition API
- **Vue Router** para navegação
- **Vuex** para gerenciamento de estado
- **Axios** para requisições HTTP
- **CSS Grid/Flexbox** para layout responsivo

### **Infraestrutura**
- **Docker** e **Docker Compose**
- **Nginx** para servir o frontend
- **PostgreSQL** containerizado
- **Volumes persistentes** para dados

## 🚀 Instalação e Execução

### **Pré-requisitos**
- Docker e Docker Compose instalados
- Git

### **1. Clone o Repositório**
```bash
git clone <url-do-repositorio>
cd prototipo
```

### **2. Configuração do Ambiente**
```bash
# Copiar arquivo de ambiente (opcional - já configurado)
cp .env.example .env
```

### **3. Executar a Aplicação**
```bash
# Subir todos os serviços
docker-compose up -d --build

# Verificar se todos os containers estão rodando
docker-compose ps
```

### **4. Acessar a Aplicação**
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API**: http://localhost:8000

### **5. Credenciais Padrão**
- **Usuário**: admin
- **Senha**: 123456
- **Role**: administrador

## 📊 Estrutura do Banco de Dados

### **Tabelas Principais**
- **users**: Usuários do sistema
- **clients**: Clientes
- **equipments**: Equipamentos dos clientes
- **service_orders**: Ordens de serviço
- **checklists**: Templates de checklist
- **checklist_items**: Itens dos checklists
- **os_checklist_responses**: Respostas dos checklists por OS
- **os_photos**: Fotos das ordens de serviço
- **auth_tokens**: Tokens de autenticação

### **Relacionamentos**
```
Clientes (1) → (N) Equipamentos
Equipamentos (1) → (N) Ordens de Serviço
Usuários (1) → (N) Ordens de Serviço (como técnico)
Checklists (1) → (N) Items de Checklist
Ordens de Serviço (1) → (N) Respostas de Checklist
Ordens de Serviço (1) → (N) Fotos
```

## 🔧 Desenvolvimento

### **Estrutura do Projeto**
```
prototipo/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── models/         # Modelos de dados
│   │   ├── routers/        # Rotas da API
│   │   ├── middleware/     # Middlewares (auth)
│   │   └── utils/          # Utilitários
│   ├── requirements.txt    # Dependências Python
│   └── Dockerfile         # Container do backend
├── frontend/               # Interface Vue.js
│   ├── src/
│   │   ├── components/     # Componentes Vue
│   │   ├── views/          # Páginas
│   │   ├── router/         # Configuração de rotas
│   │   └── store/          # Estado global (Vuex)
│   ├── package.json       # Dependências Node
│   └── Dockerfile         # Container do frontend
├── initdb/                # Scripts de inicialização do banco
├── docker-compose.yml     # Orquestração dos containers
└── README.md             # Este arquivo
```

### **Comandos Úteis**
```bash
# Ver logs dos containers
docker-compose logs -f [service_name]

# Reiniciar um serviço específico
docker-compose restart [service_name]

# Parar todos os serviços
docker-compose down

# Parar e remover volumes (CUIDADO: apaga dados)
docker-compose down -v

# Executar comandos dentro do container
docker-compose exec [service_name] [command]

# Rebuild de um serviço específico
docker-compose up -d --build [service_name]
```

## 🧪 Testes

### **Testando a API**
```bash
# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "123456"}'

# Listar ordens (usar token do login)
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8000/orders/"
```

### **Testando o Frontend**
1. Acesse http://localhost:3000
2. Faça login com admin/123456
3. Navegue pelas funcionalidades:
   - Gestão de usuários
   - Criação de ordens
   - Preenchimento de checklist
   - Upload de fotos

## 🔒 Segurança

### **Implementadas**
- ✅ **Autenticação JWT**: Tokens seguros com expiração
- ✅ **Hash de Senhas**: Bcrypt para criptografia
- ✅ **Validação de Dados**: Pydantic no backend, validações no frontend
- ✅ **Controle de Acesso**: Permissões por role
- ✅ **CORS**: Configurado para desenvolvimento
- ✅ **SQL Injection**: Protegido pelo SQLAlchemy ORM

### **Recomendações para Produção**
- 🔧 Configurar HTTPS
- 🔧 Implementar rate limiting
- 🔧 Adicionar logs de auditoria
- 🔧 Configurar backup automático do banco
- 🔧 Usar secrets management para variáveis sensíveis

## 📈 Padrões de Projeto Aplicados

### **Backend**
- **Repository Pattern**: Separação entre modelos e lógica de negócio
- **Dependency Injection**: FastAPI Depends para injeção de dependências
- **MVC**: Separação clara entre rotas, modelos e lógica
- **Factory Pattern**: Criação de sessões de banco
- **Strategy Pattern**: Diferentes estratégias de autenticação/autorização

### **Frontend**
- **Component Pattern**: Componentes Vue reutilizáveis
- **Observer Pattern**: Vuex para gerenciamento de estado
- **Module Pattern**: Organização em módulos (auth, etc.)
- **Facade Pattern**: Axios como facade para requisições HTTP

## 🎯 Roadmap

### **Próximas Funcionalidades**
- [ ] Sistema de notificações
- [ ] Relatórios e dashboards
- [ ] Histórico de alterações
- [ ] Sistema de aprovação de OS
- [ ] Integração com calendário
- [ ] App mobile (React Native/Flutter)
- [ ] Sistema de backup automático
- [ ] Logs de auditoria

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas ou suporte:
- 📧 Email: [seu-email@exemplo.com]
- 🐛 Issues: [GitHub Issues]
- 📖 Documentação: [Wiki do projeto]

---

**Desenvolvido com ❤️ para otimizar o gerenciamento de ordens de serviço**