from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime

from ..models.database import SessionLocal
from ..models.orders import (
    service_orders_table, clients_table, equipments_table, 
    checklists_table, checklist_items_table,
    os_checklist_responses_table, os_photos_table
)
from ..models.auth import users_table
from ..models.order_models import (
    ServiceOrderCreate, 
    ServiceOrderRead, 
    ServiceOrderUpdate,
    ClientCreate, 
    ClientRead, 
    EquipmentCreate, 
    EquipmentRead,
    ChecklistCreate, 
    ChecklistRead, 
    ChecklistItemCreate, 
    ChecklistItemRead
)
from ..middleware.auth import get_current_active_user

router = APIRouter(
    prefix="/orders",
    tags=["service_orders"]
)

def get_db():
    """Dependência para obter sessão do banco"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== ORDENS DE SERVIÇO =====

@router.get("/", response_model=List[ServiceOrderRead])
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Lista ordens de serviço com filtros opcionais"""
    query = select(service_orders_table)
    
    # Aplicar filtros
    if status:
        query = query.where(service_orders_table.c.status == status)
    if user_id:
        query = query.where(service_orders_table.c.user_id == user_id)
    
    # Paginação
    query = query.offset(skip).limit(limit)
    
    # Executar query
    result = db.execute(query).fetchall()
    
    orders = []
    for row in result:
        # Buscar dados relacionados
        client = db.execute(
            select(clients_table).where(clients_table.c.id == row.client_id)
        ).first()
        
        equipment = db.execute(
            select(equipments_table).where(equipments_table.c.id == row.equipment_id)
        ).first()
        
        user = db.execute(
            select(users_table).where(users_table.c.id == row.user_id)
        ).first()
        
        order_data = {
            "id": row.id,
            "title": row.title,
            "description": row.description,
            "status": row.status,
            "client_id": row.client_id,
            "equipment_id": row.equipment_id,
            "user_id": row.user_id,
            "created_at": row.created_at,
            "updated_at": row.updated_at,
            "client": {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
                "address": client.address,
                "created_at": client.created_at
            } if client else None,
            "equipment": {
                "id": equipment.id,
                "type": equipment.type,
                "brand": equipment.brand,
                "model": equipment.model,
                "serial_number": equipment.serial_number,
                "client_id": equipment.client_id,
                "created_at": equipment.created_at
            } if equipment else None,
            "user": {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at
            } if user else None
        }
        orders.append(order_data)
    
    return orders

@router.get("/{order_id}", response_model=ServiceOrderRead)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Busca uma ordem de serviço por ID"""
    order = db.execute(
        select(service_orders_table).where(service_orders_table.c.id == order_id)
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    
    # Buscar dados relacionados
    client = db.execute(
        select(clients_table).where(clients_table.c.id == order.client_id)
    ).first()
    
    equipment = db.execute(
        select(equipments_table).where(equipments_table.c.id == order.equipment_id)
    ).first()
    
    user = db.execute(
        select(users_table).where(users_table.c.id == order.user_id)
    ).first()
    
    return {
        "id": order.id,
        "title": order.title,
        "description": order.description,
        "status": order.status,
        "client_id": order.client_id,
        "equipment_id": order.equipment_id,
        "user_id": order.user_id,
        "created_at": order.created_at,
        "updated_at": order.updated_at,
        "client": {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "address": client.address,
            "created_at": client.created_at
        } if client else None,
        "equipment": {
            "id": equipment.id,
            "type": equipment.type,
            "brand": equipment.brand,
            "model": equipment.model,
            "serial_number": equipment.serial_number,
            "client_id": equipment.client_id,
            "created_at": equipment.created_at
        } if equipment else None,
        "user": {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at
        } if user else None
    }

@router.post("/", response_model=ServiceOrderRead)
def create_order(
    order: ServiceOrderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Cria uma nova ordem de serviço"""
    # Verificar se cliente existe
    client = db.execute(
        select(clients_table).where(clients_table.c.id == order.client_id)
    ).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Verificar se equipamento existe
    equipment = db.execute(
        select(equipments_table).where(equipments_table.c.id == order.equipment_id)
    ).first()
    
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    
    # Criar ordem de serviço
    stmt = service_orders_table.insert().values(
        client_id=order.client_id,
        equipment_id=order.equipment_id,
        user_id=current_user.id,
        title=order.title,
        description=order.description,
        status=order.status
    )
    
    try:
        result = db.execute(stmt)
        db.commit()
        
        # Buscar a ordem criada
        new_order = db.execute(
            select(service_orders_table).where(service_orders_table.c.id == result.inserted_primary_key[0])
        ).first()
        
        return {
            "id": new_order.id,
            "title": new_order.title,
            "description": new_order.description,
            "status": new_order.status,
            "client_id": new_order.client_id,
            "equipment_id": new_order.equipment_id,
            "user_id": new_order.user_id,
            "created_at": new_order.created_at,
            "updated_at": new_order.updated_at,
            "client": {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
                "address": client.address,
                "created_at": client.created_at
            },
            "equipment": {
                "id": equipment.id,
                "type": equipment.type,
                "brand": equipment.brand,
                "model": equipment.model,
                "serial_number": equipment.serial_number,
                "client_id": equipment.client_id,
                "created_at": equipment.created_at
            },
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "name": current_user.name,
                "email": current_user.email,
                "role": current_user.role,
                "is_active": current_user.is_active,
                "created_at": current_user.created_at
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar ordem de serviço: {e}")

@router.put("/{order_id}", response_model=ServiceOrderRead)
def update_order(
    order_id: int,
    order_update: ServiceOrderUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Atualiza uma ordem de serviço"""
    # Verificar se ordem existe
    existing_order = db.execute(
        select(service_orders_table).where(service_orders_table.c.id == order_id)
    ).first()
    
    if not existing_order:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    
    # Preparar dados para atualização
    update_data = {}
    if order_update.title is not None:
        update_data["title"] = order_update.title
    if order_update.description is not None:
        update_data["description"] = order_update.description
    if order_update.status is not None:
        update_data["status"] = order_update.status
    
    update_data["updated_at"] = datetime.utcnow()
    
    # Atualizar ordem
    stmt = service_orders_table.update().where(
        service_orders_table.c.id == order_id
    ).values(**update_data)
    
    try:
        db.execute(stmt)
        db.commit()
        
        # Buscar ordem atualizada
        updated_order = db.execute(
            select(service_orders_table).where(service_orders_table.c.id == order_id)
        ).first()
        
        # Buscar dados relacionados
        client = db.execute(
            select(clients_table).where(clients_table.c.id == updated_order.client_id)
        ).first()
        
        equipment = db.execute(
            select(equipments_table).where(equipments_table.c.id == updated_order.equipment_id)
        ).first()
        
        user = db.execute(
            select(users_table).where(users_table.c.id == updated_order.user_id)
        ).first()
        
        return {
            "id": updated_order.id,
            "title": updated_order.title,
            "description": updated_order.description,
            "status": updated_order.status,
            "client_id": updated_order.client_id,
            "equipment_id": updated_order.equipment_id,
            "user_id": updated_order.user_id,
            "created_at": updated_order.created_at,
            "updated_at": updated_order.updated_at,
            "client": {
                "id": client.id,
                "name": client.name,
                "email": client.email,
                "phone": client.phone,
                "address": client.address,
                "created_at": client.created_at
            } if client else None,
            "equipment": {
                "id": equipment.id,
                "type": equipment.type,
                "brand": equipment.brand,
                "model": equipment.model,
                "serial_number": equipment.serial_number,
                "client_id": equipment.client_id,
                "created_at": equipment.created_at
            } if equipment else None,
            "user": {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "created_at": user.created_at
            } if user else None
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar ordem de serviço: {e}")

@router.put("/{order_id}/assign-technician")
def assign_technician(
    order_id: int,
    technician_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Atribui ou reatribui um técnico a uma ordem de serviço"""
    # Verificar se ordem existe
    existing_order = db.execute(
        select(service_orders_table).where(service_orders_table.c.id == order_id)
    ).first()
    
    if not existing_order:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    
    # Verificar se técnico existe e está ativo
    technician = db.execute(
        select(users_table).where(
            users_table.c.id == technician_id,
            users_table.c.is_active == True
        )
    ).first()
    
    if not technician:
        raise HTTPException(status_code=404, detail="Técnico não encontrado ou inativo")
    
    # Atualizar ordem com novo técnico
    stmt = service_orders_table.update().where(
        service_orders_table.c.id == order_id
    ).values(
        user_id=technician_id,
        updated_at=datetime.utcnow()
    )
    
    try:
        db.execute(stmt)
        db.commit()
        
        # Buscar ordem atualizada
        updated_order = db.execute(
            select(service_orders_table).where(service_orders_table.c.id == order_id)
        ).first()
        
        # Buscar dados relacionados
        client = db.execute(
            select(clients_table).where(clients_table.c.id == updated_order.client_id)
        ).first()
        
        equipment = db.execute(
            select(equipments_table).where(equipments_table.c.id == updated_order.equipment_id)
        ).first()
        
        return {
            "message": f"Técnico {technician.name or technician.username} atribuído com sucesso",
            "order": {
                "id": updated_order.id,
                "title": updated_order.title,
                "status": updated_order.status,
                "technician": {
                    "id": technician.id,
                    "username": technician.username,
                    "name": technician.name,
                    "email": technician.email,
                    "role": technician.role
                },
                "updated_at": updated_order.updated_at
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atribuir técnico: {e}")

@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Exclui uma ordem de serviço"""
    # Verificar se ordem existe
    existing_order = db.execute(
        select(service_orders_table).where(service_orders_table.c.id == order_id)
    ).first()
    
    if not existing_order:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    
    # Excluir ordem
    stmt = service_orders_table.delete().where(service_orders_table.c.id == order_id)
    
    try:
        result = db.execute(stmt)
        db.commit()
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
        
        return {"message": "Ordem de serviço excluída com sucesso"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao excluir ordem de serviço: {e}")

# ===== TÉCNICOS =====

@router.get("/technicians/")
def list_technicians(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Lista todos os técnicos disponíveis"""
    technicians = db.execute(
        select(users_table).where(users_table.c.is_active == True)
    ).fetchall()
    
    return [
        {
            "id": tech.id,
            "username": tech.username,
            "name": tech.name,
            "email": tech.email,
            "role": tech.role,
            "is_active": tech.is_active
        }
        for tech in technicians
    ]

# ===== CLIENTES =====

@router.get("/clients/", response_model=List[ClientRead])
def list_clients(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Lista todos os clientes"""
    clients = db.execute(select(clients_table)).fetchall()
    
    return [
        {
            "id": client.id,
            "name": client.name,
            "email": client.email,
            "phone": client.phone,
            "address": client.address,
            "created_at": client.created_at
        }
        for client in clients
    ]

@router.post("/clients/", response_model=ClientRead)
def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Cria um novo cliente"""
    stmt = clients_table.insert().values(
        name=client.name,
        email=client.email,
        phone=client.phone,
        address=client.address
    )
    
    try:
        result = db.execute(stmt)
        db.commit()
        
        new_client = db.execute(
            select(clients_table).where(clients_table.c.id == result.inserted_primary_key[0])
        ).first()
        
        return {
            "id": new_client.id,
            "name": new_client.name,
            "email": new_client.email,
            "phone": new_client.phone,
            "address": new_client.address,
            "created_at": new_client.created_at
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar cliente: {e}")

# ===== EQUIPAMENTOS =====

@router.get("/equipments/", response_model=List[EquipmentRead])
def list_equipments(
    client_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Lista equipamentos, opcionalmente filtrados por cliente"""
    query = select(equipments_table)
    
    if client_id:
        query = query.where(equipments_table.c.client_id == client_id)
    
    equipments = db.execute(query).fetchall()
    
    return [
        {
            "id": equipment.id,
            "type": equipment.type,
            "brand": equipment.brand,
            "model": equipment.model,
            "serial_number": equipment.serial_number,
            "client_id": equipment.client_id,
            "created_at": equipment.created_at
        }
        for equipment in equipments
    ]

@router.post("/equipments/", response_model=EquipmentRead)
def create_equipment(
    equipment: EquipmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Cria um novo equipamento"""
    # Verificar se cliente existe
    client = db.execute(
        select(clients_table).where(clients_table.c.id == equipment.client_id)
    ).first()
    
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    stmt = equipments_table.insert().values(
        client_id=equipment.client_id,
        type=equipment.type,
        brand=equipment.brand,
        model=equipment.model,
        serial_number=equipment.serial_number
    )
    
    try:
        result = db.execute(stmt)
        db.commit()
        
        new_equipment = db.execute(
            select(equipments_table).where(equipments_table.c.id == result.inserted_primary_key[0])
        ).first()
        
        return {
            "id": new_equipment.id,
            "type": new_equipment.type,
            "brand": new_equipment.brand,
            "model": new_equipment.model,
            "serial_number": new_equipment.serial_number,
            "client_id": new_equipment.client_id,
            "created_at": new_equipment.created_at
        }
        
    except Exception as e:
        db.rollback()
        if "unique" in str(e).lower():
            raise HTTPException(status_code=400, detail="Número de série já existe")
        raise HTTPException(status_code=400, detail=f"Erro ao criar equipamento: {e}")
