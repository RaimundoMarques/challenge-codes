#!/usr/bin/env python3
import os
import bcrypt
from sqlalchemy import create_engine, text

# Configurações do banco
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_HOST = os.getenv("DB_HOST", "db-postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def hash_password(password: str) -> str:
    """Gera hash da senha"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def update_admin_password():
    """Atualiza a senha do admin com hash bcrypt"""
    engine = create_engine(DATABASE_URL)
    
    # Gerar hash da senha
    password_hash = hash_password("123456")
    
    # Atualizar no banco
    with engine.connect() as conn:
        result = conn.execute(
            text("UPDATE users SET password_hash = :password_hash WHERE username = 'admin'"),
            {"password_hash": password_hash}
        )
        conn.commit()
        
        print(f"Senha do admin atualizada com sucesso!")
        print(f"Hash gerado: {password_hash}")

if __name__ == "__main__":
    update_admin_password()
