# 📝 Histórico de Mudanças do Projeto

## ✅ Reorganização do Projeto

Este documento resume todas as reorganizações e melhorias realizadas no projeto.

---

## 🏗️ Estrutura Reorganizada

### Separação Backend/Frontend
- Backend e frontend agora têm Docker Compose separados
- `docker-compose.backend.yml` - Banco + API
- `docker-compose.frontend.yml` - Frontend Vue.js

### Pasta initdb
- Movida de `/initdb/` para `/backend/initdb/`
- Scripts SQL agora estão junto com o código do backend

### Scripts Simplificados
- **Antes**: 8 scripts separados (bash + PowerShell)
- **Depois**: 2 scripts unificados
  - `start.sh` - Inicia serviços (aceita parâmetros: backend, frontend, all)
  - `stop.sh` - Para todos os serviços

---

## 🔧 Ajustes Técnicos

### Campo activities_description
- Adicionada coluna na tabela `service_orders`
- Corrigida criação, listagem e atualização de ordens

### Dockerfiles Melhorados
- Backend: Suporte para psycopg2, curl para healthcheck
- Frontend: Curl para healthcheck, otimizações

---

## 📚 Documentação Organizada

Toda documentação está organizada em pastas específicas:
- `/docs/` - Documentação geral
- `/backend/docs/` - Documentação do backend
- `/frontend/docs/` - Documentação do frontend

---

**Data:** 03/12/2025

