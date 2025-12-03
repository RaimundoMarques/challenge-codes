-- Adicionar campo activities_description à tabela service_orders
ALTER TABLE service_orders ADD COLUMN IF NOT EXISTS activities_description TEXT;

-- Inserir alguns checklists de exemplo
INSERT INTO checklists (name) VALUES 
('Checklist de Manutenção Preventiva'),
('Checklist de Reparo'),
('Checklist de Instalação')
ON CONFLICT DO NOTHING;

-- Inserir itens para o checklist de manutenção preventiva
INSERT INTO checklist_items (checklist_id, description) 
SELECT 1, item FROM (VALUES 
    ('Verificar funcionamento geral do equipamento'),
    ('Limpeza externa e interna'),
    ('Verificação de conexões e cabos'),
    ('Teste de todos os componentes'),
    ('Verificação de atualizações de software'),
    ('Backup de dados (se aplicável)'),
    ('Documentação das atividades realizadas')
) AS items(item)
WHERE EXISTS (SELECT 1 FROM checklists WHERE id = 1);

-- Inserir itens para o checklist de reparo
INSERT INTO checklist_items (checklist_id, description) 
SELECT 2, item FROM (VALUES 
    ('Diagnóstico do problema'),
    ('Identificação da causa raiz'),
    ('Execução do reparo'),
    ('Teste de funcionamento'),
    ('Verificação de segurança'),
    ('Limpeza e organização'),
    ('Documentação do reparo')
) AS items(item)
WHERE EXISTS (SELECT 1 FROM checklists WHERE id = 2);

-- Inserir itens para o checklist de instalação
INSERT INTO checklist_items (checklist_id, description) 
SELECT 3, item FROM (VALUES 
    ('Verificação do local de instalação'),
    ('Preparação do ambiente'),
    ('Instalação do hardware'),
    ('Configuração do software'),
    ('Teste de funcionamento'),
    ('Treinamento do usuário'),
    ('Documentação da instalação')
) AS items(item)
WHERE EXISTS (SELECT 1 FROM checklists WHERE id = 3);