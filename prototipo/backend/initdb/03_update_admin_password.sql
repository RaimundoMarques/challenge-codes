-- Atualizar senha do usuário admin para usar hash bcrypt
-- Senha: 123456
UPDATE users 
SET password_hash = '$2b$12$SnxPa/1XTSLcB262HfETa.fEhWIQ5wRLMQNleuqDM9WoA/mwyx2Z2' 
WHERE username = 'admin' 
  AND (password_hash = '123456' OR password_hash NOT LIKE '$2b$%');

