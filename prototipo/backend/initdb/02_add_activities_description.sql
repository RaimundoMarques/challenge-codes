-- Adicionar campo activities_description à tabela service_orders
-- Este script só executa se a tabela service_orders já existir
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'service_orders') THEN
        ALTER TABLE service_orders ADD COLUMN IF NOT EXISTS activities_description TEXT;
    END IF;
END $$;

-- Inserir alguns checklists de exemplo
INSERT INTO checklists (name) 
SELECT name FROM (VALUES 
    ('Checklist de Manutenção Preventiva'),
    ('Checklist de Reparo'),
    ('Checklist de Instalação')
) AS new_checklists(name)
WHERE NOT EXISTS (SELECT 1 FROM checklists WHERE checklists.name = new_checklists.name);

-- Inserir itens para o checklist de manutenção preventiva
INSERT INTO checklist_items (checklist_id, description) 
SELECT c.id, item FROM (VALUES 
    ('Verificar funcionamento geral do equipamento'),
    ('Limpeza externa e interna'),
    ('Verificação de conexões e cabos'),
    ('Teste de todos os componentes'),
    ('Verificação de atualizações de software'),
    ('Backup de dados (se aplicável)'),
    ('Documentação das atividades realizadas')
) AS items(item)
CROSS JOIN checklists c WHERE c.name = 'Checklist de Manutenção Preventiva'
  AND NOT EXISTS (SELECT 1 FROM checklist_items WHERE checklist_id = c.id AND description = items.item);

-- Inserir itens para o checklist de reparo
INSERT INTO checklist_items (checklist_id, description) 
SELECT c.id, item FROM (VALUES 
    ('Diagnóstico do problema'),
    ('Identificação da causa raiz'),
    ('Execução do reparo'),
    ('Teste de funcionamento'),
    ('Verificação de segurança'),
    ('Limpeza e organização'),
    ('Documentação do reparo')
) AS items(item)
CROSS JOIN checklists c WHERE c.name = 'Checklist de Reparo'
  AND NOT EXISTS (SELECT 1 FROM checklist_items WHERE checklist_id = c.id AND description = items.item);

-- Inserir itens para o checklist de instalação
INSERT INTO checklist_items (checklist_id, description) 
SELECT c.id, item FROM (VALUES 
    ('Verificação do local de instalação'),
    ('Preparação do ambiente'),
    ('Instalação do hardware'),
    ('Configuração do software'),
    ('Teste de funcionamento'),
    ('Treinamento do usuário'),
    ('Documentação da instalação')
) AS items(item)
CROSS JOIN checklists c WHERE c.name = 'Checklist de Instalação'
  AND NOT EXISTS (SELECT 1 FROM checklist_items WHERE checklist_id = c.id AND description = items.item);