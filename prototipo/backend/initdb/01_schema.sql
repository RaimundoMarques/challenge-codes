-- =========================================
-- Usuários (técnicos da empresa)
-- =========================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    role VARCHAR(30) DEFAULT 'tecnico',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserindo técnico administrador
-- Senha: 123456 (hash bcrypt)
INSERT INTO users (username, password_hash, name, email, role)
VALUES ('admin', '$2b$12$SnxPa/1XTSLcB262HfETa.fEhWIQ5wRLMQNleuqDM9WoA/mwyx2Z2', 'Administrador', 'admin@empresa.com', 'administrador')
ON CONFLICT (username) DO NOTHING;

-- =========================================
-- Clientes
-- =========================================
CREATE TABLE IF NOT EXISTS clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cliente de exemplo
INSERT INTO clients (name, email, phone, address)
SELECT 'Kodigos', 'contato@kodigos.com.br', '+55 (92) 99461-7117', 'Skye Platinum Offices - Av. Dr. Theomário Pinto da Costa, 811 - Sala 1201 - Chapada, Manaus - AM, 69050-055'
WHERE NOT EXISTS (SELECT 1 FROM clients WHERE name = 'Kodigos');

-- =========================================
-- Equipamentos
-- =========================================
CREATE TABLE IF NOT EXISTS equipments (
    id SERIAL PRIMARY KEY,
    client_id INT NOT NULL REFERENCES clients(id),
    type VARCHAR(50) NOT NULL,          -- ex: Desktop, Notebook, Servidor
    brand VARCHAR(50),
    model VARCHAR(100),
    serial_number VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Equipamento exemplo
INSERT INTO equipments (client_id, type, brand, model, serial_number)
SELECT id, 'Notebook', 'Dell', 'Inspiron 15', 'SN123456789'
FROM clients WHERE name = 'Kodigos'
ON CONFLICT (serial_number) DO NOTHING;

-- =========================================
-- Ordem de Serviço
-- =========================================
CREATE TABLE IF NOT EXISTS service_orders (
    id SERIAL PRIMARY KEY,
    client_id INT NOT NULL REFERENCES clients(id),
    equipment_id INT NOT NULL REFERENCES equipments(id),
    user_id INT NOT NULL REFERENCES users(id), -- técnico responsável
    title VARCHAR(150) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'open', -- open, in_progress, closed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ordem de serviço exemplo
INSERT INTO service_orders (client_id, equipment_id, user_id, title, description, status)
SELECT c.id, e.id, u.id, 
       'Formatação de notebook', 
       'Notebook lento, cliente solicitou backup e formatação', 
       'open'
FROM clients c
JOIN equipments e ON e.client_id = c.id
JOIN users u ON u.username = 'admin'
WHERE c.name = 'Kodigos'
  AND NOT EXISTS (
    SELECT 1 FROM service_orders so 
    WHERE so.client_id = c.id 
      AND so.equipment_id = e.id 
      AND so.title = 'Formatação de notebook'
  );

-- =========================================
-- Checklists
-- =========================================
CREATE TABLE IF NOT EXISTS checklists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS checklist_items (
    id SERIAL PRIMARY KEY,
    checklist_id INT NOT NULL REFERENCES checklists(id),
    description VARCHAR(255) NOT NULL
);

-- Checklist exemplo: manutenção preventiva de computadores
INSERT INTO checklists (name)
SELECT 'Manutenção preventiva de computadores'
WHERE NOT EXISTS (SELECT 1 FROM checklists WHERE name = 'Manutenção preventiva de computadores');

INSERT INTO checklist_items (checklist_id, description)
SELECT c.id, 'Verificar saúde do HD/SSD'
FROM checklists c WHERE c.name = 'Manutenção preventiva de computadores'
  AND NOT EXISTS (SELECT 1 FROM checklist_items WHERE checklist_id = c.id AND description = 'Verificar saúde do HD/SSD');

INSERT INTO checklist_items (checklist_id, description)
SELECT c.id, 'Limpar ventoinhas e dissipadores'
FROM checklists c WHERE c.name = 'Manutenção preventiva de computadores'
  AND NOT EXISTS (SELECT 1 FROM checklist_items WHERE checklist_id = c.id AND description = 'Limpar ventoinhas e dissipadores');

INSERT INTO checklist_items (checklist_id, description)
SELECT c.id, 'Trocar pasta térmica do processador'
FROM checklists c WHERE c.name = 'Manutenção preventiva de computadores'
  AND NOT EXISTS (SELECT 1 FROM checklist_items WHERE checklist_id = c.id AND description = 'Trocar pasta térmica do processador');

INSERT INTO checklist_items (checklist_id, description)
SELECT c.id, 'Rodar antivírus completo'
FROM checklists c WHERE c.name = 'Manutenção preventiva de computadores'
  AND NOT EXISTS (SELECT 1 FROM checklist_items WHERE checklist_id = c.id AND description = 'Rodar antivírus completo');

-- =========================================
-- Respostas de checklist em uma OS
-- =========================================
CREATE TABLE IF NOT EXISTS os_checklist_responses (
    id SERIAL PRIMARY KEY,
    service_order_id INT NOT NULL REFERENCES service_orders(id),
    checklist_item_id INT NOT NULL REFERENCES checklist_items(id),
    is_checked BOOLEAN NOT NULL,
    responded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- Fotos da OS
-- =========================================
CREATE TABLE IF NOT EXISTS os_photos (
    id SERIAL PRIMARY KEY,
    service_order_id INT NOT NULL REFERENCES service_orders(id),
    photo_url TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Tabela de tokens de autenticação
CREATE TABLE IF NOT EXISTS auth_tokens (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token TEXT UNIQUE NOT NULL, -- JWT ou UUID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,       -- tempo de validade do token
    is_revoked BOOLEAN DEFAULT FALSE
);
