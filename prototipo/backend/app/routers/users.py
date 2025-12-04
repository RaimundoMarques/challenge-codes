from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.database import SessionLocal
from ..models.auth import users_table
from ..models.orders import service_orders_table
from ..models.auth_models import UserCreate, UserRead, UserUpdate
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

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # Apenas admin pode atualizar usuários
):
    """Atualiza um usuário (requer privilégios de administrador)"""
    # Verificar se usuário existe
    existing_user = db.execute(
        users_table.select().where(users_table.c.id == user_id)
    ).first()
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Preparar dados para atualização
    update_data = {}
    if user_update.username is not None:
        update_data["username"] = user_update.username
    if user_update.name is not None:
        update_data["name"] = user_update.name
    if user_update.email is not None:
        update_data["email"] = user_update.email
    if user_update.role is not None:
        update_data["role"] = user_update.role
    if user_update.is_active is not None:
        update_data["is_active"] = user_update.is_active
    
    # Atualizar senha se fornecida
    if user_update.password is not None and user_update.password.strip():
        update_data["password_hash"] = get_password_hash(user_update.password)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização")
    
    # Atualizar usuário
    stmt = users_table.update().where(
        users_table.c.id == user_id
    ).values(**update_data)
    
    try:
        result = db.execute(stmt)
        db.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        # Buscar usuário atualizado
        updated_user = db.execute(
            users_table.select().where(users_table.c.id == user_id)
        ).first()
        
        return {
            "id": updated_user.id,
            "username": updated_user.username,
            "name": updated_user.name,
            "email": updated_user.email,
            "role": updated_user.role,
            "is_active": updated_user.is_active,
            "created_at": updated_user.created_at
        }
        
    except Exception as e:
        db.rollback()
        if "unique" in str(e).lower():
            raise HTTPException(status_code=400, detail="Username ou email já existem")
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar usuário: {e}")

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)  # Apenas admin pode deletar usuários
):
    """Exclui um usuário permanentemente (requer privilégios de administrador)"""
    # Verificar se usuário existe
    existing_user = db.execute(
        users_table.select().where(users_table.c.id == user_id)
    ).first()
    
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Não permitir que admin se exclua
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Você não pode excluir a si mesmo")
    
    # Verificar se o usuário tem ordens de serviço associadas
    orders_count = db.execute(
        select(service_orders_table.c.id).where(service_orders_table.c.user_id == user_id)
    ).fetchall()
    
    if orders_count:
        count = len(orders_count)
        raise HTTPException(
            status_code=400, 
            detail=f"Este usuário está vinculado a {count} ordem(ns) de serviço. Reatribua as ordens para outro técnico ou desative o usuário em vez de excluí-lo."
        )
    
    # Excluir usuário
    stmt = users_table.delete().where(users_table.c.id == user_id)
    
    try:
        result = db.execute(stmt)
        db.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return {"message": "Usuário excluído com sucesso"}
        
    except Exception as e:
        db.rollback()
        # Verificar se é erro de foreign key
        error_str = str(e).lower()
        if "foreign key" in error_str or "violates foreign key constraint" in error_str or "service_orders" in error_str:
            # Contar quantas ordens estão vinculadas
            try:
                orders_count = db.execute(
                    select(service_orders_table.c.id).where(service_orders_table.c.user_id == user_id)
                ).fetchall()
                count = len(orders_count)
                raise HTTPException(
                    status_code=400,
                    detail=f"Este usuário está vinculado a {count} ordem(ns) de serviço. Reatribua as ordens para outro técnico ou desative o usuário em vez de excluí-lo."
                )
            except HTTPException:
                raise
            except Exception:
                raise HTTPException(
                    status_code=400,
                    detail="Este usuário está vinculado a ordens de serviço. Reatribua as ordens para outro técnico ou desative o usuário em vez de excluí-lo."
                )
        raise HTTPException(status_code=400, detail=f"Erro ao excluir usuário: {e}")