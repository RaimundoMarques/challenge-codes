import os
import bcrypt
from datetime import datetime, timedelta
from jose import JWTError, jwt
# from passlib.context import CryptContext
from typing import Optional
from sqlalchemy.orm import Session
from ..models.database import SessionLocal
from ..models.auth import users_table, auth_tokens_table

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hash de senhas
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    """Gera hash da senha"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verifica e decodifica o token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return payload
    except JWTError:
        return None

def authenticate_user(db: Session, username: str, password: str):
    """Autentica usuário com username e senha"""
    # Buscar usuário no banco
    user = db.execute(
        users_table.select().where(users_table.c.username == username)
    ).first()
    
    if not user:
        return False
    
    # Verificar se usuário está ativo
    if not user.is_active:
        return False
    
    # Verificar senha
    if not verify_password(password, user.password_hash):
        return False
    
    return user

def get_user_by_username(db: Session, username: str):
    """Busca usuário por username"""
    user = db.execute(
        users_table.select().where(users_table.c.username == username)
    ).first()
    return user

def create_token_record(db: Session, user_id: int, token: str, expires_at: datetime):
    """Cria registro de token no banco"""
    stmt = auth_tokens_table.insert().values(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.execute(stmt)
    db.commit()

def revoke_token(db: Session, token: str):
    """Revoga token no banco"""
    stmt = auth_tokens_table.update().where(
        auth_tokens_table.c.token == token
    ).values(is_revoked=True)
    db.execute(stmt)
    db.commit()

def is_token_revoked(db: Session, token: str) -> bool:
    """Verifica se token foi revogado"""
    result = db.execute(
        auth_tokens_table.select().where(
            auth_tokens_table.c.token == token
        )
    ).first()
    
    if not result:
        return True  # Token não existe = considerado revogado
    
    return result.is_revoked or (result.expires_at and result.expires_at < datetime.utcnow())
