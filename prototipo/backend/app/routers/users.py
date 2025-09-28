from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.database import SessionLocal
from ..models.auth import users_table
from ..models.auth_models import UserBase, UserCreate, UserRead
from ..middleware.auth import get_current_active_user, require_admin
from ..utils.security import get_password_hash
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Dependência para obter a sessão
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas protegidas
@router.get("/", response_model=List[UserRead])
def list_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Lista todos os usuários (requer autenticação)"""
    query = db.execute(users_table.select()).fetchall()
    
    # Converter tuplas para dicionários
    users = []
    for row in query:
        user_dict = {
            "id": row.id,
            "username": row.username,
            "name": row.name,
            "email": row.email,
            "role": row.role,
            "is_active": row.is_active,
            "created_at": row.created_at
        }
        users.append(user_dict)
    
    return users

@router.get("/{user_id}", response_model=UserRead)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Busca um usuário por ID (requer autenticação)"""
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
        "role": query.role,
        "is_active": query.is_active,
        "created_at": query.created_at
    }

@router.post("/", response_model=UserRead)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # Apenas admin pode criar usuários
):
    """Cria um novo usuário (requer privilégios de administrador)"""
    # Validações básicas
    if len(user.username) < 3:
        raise HTTPException(status_code=400, detail="Username deve ter pelo menos 3 caracteres")
    
    if user.email and "@" not in user.email:
        raise HTTPException(status_code=400, detail="Email inválido")
    
    # Hash da senha
    hashed_password = get_password_hash(user.password)
    
    stmt = users_table.insert().values(
        username=user.username,
        password_hash=hashed_password,
        name=user.name,
        email=user.email,
        role=user.role
    )
    
    try:
        result = db.execute(stmt)
        db.commit()
        
        # Buscar o usuário criado
        new_user = db.execute(
            users_table.select().where(users_table.c.id == result.inserted_primary_key[0])
        ).first()
        
        return {
            "id": new_user.id,
            "username": new_user.username,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role,
            "is_active": new_user.is_active,
            "created_at": new_user.created_at
        }
        
    except Exception as e:
        db.rollback()
        if "unique" in str(e).lower():
            raise HTTPException(status_code=400, detail="Username ou email já existem")
        raise HTTPException(status_code=400, detail=f"Erro ao criar usuário: {e}")

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # Apenas admin pode deletar usuários
):
    """Desativa um usuário (soft delete) - requer privilégios de administrador"""
    stmt = users_table.update().where(
        users_table.c.id == user_id
    ).values(is_active=False)
    
    result = db.execute(stmt)
    db.commit()
    
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {"message": "Usuário desativado com sucesso"}