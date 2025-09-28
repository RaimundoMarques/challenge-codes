from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.database import SessionLocal
from pydantic import BaseModel
from typing import List
from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, Text, TIMESTAMP
from sqlalchemy.sql import func

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

class UserBase(BaseModel):
    username: str
    name: str | None = None
    email: str | None = None

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool = True
    created_at: str | None = None

    class Config:
        from_attributes = True  # FastAPI v2

# Definir metadata corretamente
metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True, nullable=False),
    Column("password_hash", Text, nullable=False),
    Column("name", String(100)),
    Column("email", String(100), unique=True),
    Column("is_active", Boolean, default=True),
    Column("created_at", TIMESTAMP, default=func.current_timestamp())
)

# Dependência para obter a sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas
@router.get("/", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    """Lista todos os usuários"""
    query = db.execute(users_table.select()).fetchall()

    users = []
    for row in query:
        user_dict = {
            "id": row.id,
            "username": row.username,
            "name": row.name,
            "email": row.email,
            "is_active": row.is_active,
            "created_at": str(row.created_at) if row.created_at else None
        }
        users.append(user_dict)
    
    return users

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Busca um usuário por ID"""
    query = db.execute(
        users_table.select().where(users_table.c.id == user_id)
    ).first()
    
    if not query:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {
        "id": query.id,
        "username": query.username,
        "name": query.name,
        "email": query.email,
        "is_active": query.is_active,
        "created_at": str(query.created_at) if query.created_at else None
    }

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário"""
    # Validações básicas
    if len(user.username) < 3:
        raise HTTPException(status_code=400, detail="Username deve ter pelo menos 3 caracteres")
    
    if user.email and "@" not in user.email:
        raise HTTPException(status_code=400, detail="Email inválido")
    
    stmt = users_table.insert().values(
        username=user.username,
        password_hash=user.password,
        name=user.name,
        email=user.email
    )
    
    try:
        result = db.execute(stmt)
        db.commit()
        
        new_user = db.execute(
            users_table.select().where(users_table.c.id == result.inserted_primary_key[0])
        ).first()
        
        return {
            "id": new_user.id,
            "username": new_user.username,
            "name": new_user.name,
            "email": new_user.email,
            "is_active": new_user.is_active,
            "created_at": str(new_user.created_at) if new_user.created_at else None
        }
        
    except Exception as e:
        db.rollback()
        if "unique" in str(e).lower():
            raise HTTPException(status_code=400, detail="Username ou email já existem")
        raise HTTPException(status_code=400, detail=f"Erro ao criar usuário: {e}")

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Desativa um usuário (soft delete)"""
    stmt = users_table.update().where(
        users_table.c.id == user_id
    ).values(is_active=False)
    
    result = db.execute(stmt)
    db.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {"message": "Usuário desativado com sucesso"}