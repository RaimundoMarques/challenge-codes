from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime
import os
import uuid
import shutil

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
    ChecklistItemRead,
    ChecklistResponseCreate,
    PhotoCreate,
    PhotoRead
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
    
    # Buscar fotos da ordem
    photos = db.execute(
        select(os_photos_table).where(os_photos_table.c.service_order_id == order_id)
        .order_by(os_photos_table.c.uploaded_at.desc())
    ).fetchall()
    
    return {
        "id": order.id,
        "title": order.title,
        "description": order.description,
        "activities_description": order.activities_description,
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
        } if user else None,
        "photos": [
            {
                "id": photo.id,
                "service_order_id": photo.service_order_id,
                "photo_url": photo.photo_url,
                "uploaded_at": photo.uploaded_at
            }
            for photo in photos
        ]
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
    if order_update.activities_description is not None:
        update_data["activities_description"] = order_update.activities_description
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





# ===== CHECKLISTS =====

@router.get("/checklists/", response_model=List[ChecklistRead])
def list_checklists(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Lista todos os checklists"""
    checklists = db.execute(select(checklists_table)).fetchall()
    
    result = []
    for checklist in checklists:
        # Buscar itens do checklist
        items = db.execute(
            select(checklist_items_table).where(checklist_items_table.c.checklist_id == checklist.id)
        ).fetchall()
        
        checklist_data = {
            "id": checklist.id,
            "name": checklist.name,
            "items": [
                {
                    "id": item.id,
                    "description": item.description,
                    "checklist_id": item.checklist_id
                }
                for item in items
            ]
        }
        result.append(checklist_data)
    
    return result

@router.post("/checklists/", response_model=ChecklistRead)
def create_checklist(
    checklist: ChecklistCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Cria um novo checklist (apenas admin)"""
    stmt = checklists_table.insert().values(name=checklist.name)
    
    try:
        result = db.execute(stmt)
        db.commit()
        
        new_checklist = db.execute(
            select(checklists_table).where(checklists_table.c.id == result.inserted_primary_key[0])
        ).first()
        
        return {
            "id": new_checklist.id,
            "name": new_checklist.name,
            "items": []
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar checklist: {e}")

@router.post("/checklists/{checklist_id}/items/", response_model=ChecklistItemRead)
def create_checklist_item(
    checklist_id: int,
    item: ChecklistItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Adiciona item a um checklist"""
    # Verificar se checklist existe
    checklist = db.execute(
        select(checklists_table).where(checklists_table.c.id == checklist_id)
    ).first()
    
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist não encontrado")
    
    stmt = checklist_items_table.insert().values(
        checklist_id=checklist_id,
        description=item.description
    )
    
    try:
        result = db.execute(stmt)
        db.commit()
        
        new_item = db.execute(
            select(checklist_items_table).where(checklist_items_table.c.id == result.inserted_primary_key[0])
        ).first()
        
        return {
            "id": new_item.id,
            "description": new_item.description,
            "checklist_id": new_item.checklist_id
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar item do checklist: {e}")





# ===== RESPOSTAS DE CHECKLIST =====

@router.get("/{order_id}/checklist-responses/")
def get_checklist_responses(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Busca respostas do checklist de uma ordem de serviço"""
    responses = db.execute(
        select(os_checklist_responses_table).where(
            os_checklist_responses_table.c.service_order_id == order_id
        )
    ).fetchall()
    
    result = []
    for response in responses:
        # Buscar item do checklist
        item = db.execute(
            select(checklist_items_table).where(
                checklist_items_table.c.id == response.checklist_item_id
            )
        ).first()
        
        result.append({
            "id": response.id,
            "service_order_id": response.service_order_id,
            "checklist_item_id": response.checklist_item_id,
            "is_checked": response.is_checked,
            "responded_at": response.responded_at,
            "checklist_item": {
                "id": item.id,
                "description": item.description,
                "checklist_id": item.checklist_id
            } if item else None
        })
    
    return result

@router.post("/{order_id}/checklist-responses/")
def save_checklist_responses(
    order_id: int,
    responses: List[ChecklistResponseCreate],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Salva respostas do checklist de uma ordem de serviço"""
    # Verificar se ordem existe
    order = db.execute(
        select(service_orders_table).where(service_orders_table.c.id == order_id)
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    
    try:
        # Limpar respostas existentes
        db.execute(
            os_checklist_responses_table.delete().where(
                os_checklist_responses_table.c.service_order_id == order_id
            )
        )
        
        # Inserir novas respostas
        for response in responses:
            db.execute(
                os_checklist_responses_table.insert().values(
                    service_order_id=order_id,
                    checklist_item_id=response.checklist_item_id,
                    is_checked=response.is_checked
                )
            )
        
        db.commit()
        
        return {"message": "Respostas do checklist salvas com sucesso"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao salvar respostas: {e}")


# =========================================
# Endpoints para Fotos
# =========================================

# Configuração do diretório de upload
UPLOAD_DIR = "/code/uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def ensure_upload_dir():
    """Garante que o diretório de upload existe"""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR, exist_ok=True)

def is_allowed_file(filename: str) -> bool:
    """Verifica se o arquivo tem uma extensão permitida"""
    return any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)

@router.post("/{order_id}/photos", response_model=PhotoRead)
async def upload_photo(
    order_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Upload de uma foto para uma ordem de serviço"""
    # Verificar se ordem existe
    order = db.execute(
        select(service_orders_table).where(service_orders_table.c.id == order_id)
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    
    # Verificar se é um arquivo de imagem
    if not is_allowed_file(file.filename):
        raise HTTPException(
            status_code=400, 
            detail="Formato de arquivo não permitido. Use: jpg, jpeg, png, gif, bmp, webp"
        )
    
    # Verificar tamanho do arquivo
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, 
            detail=f"Arquivo muito grande. Tamanho máximo: {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    try:
        # Garantir que o diretório existe
        ensure_upload_dir()
        
        # Gerar nome único para o arquivo
        file_extension = os.path.splitext(file.filename)[1].lower()
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Salvar arquivo
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # Salvar referência no banco
        photo_url = f"/uploads/{unique_filename}"
        stmt = os_photos_table.insert().values(
            service_order_id=order_id,
            photo_url=photo_url
        )
        result = db.execute(stmt)
        db.commit()
        
        # Buscar foto criada
        photo = db.execute(
            select(os_photos_table).where(os_photos_table.c.id == result.inserted_primary_key[0])
        ).first()
        
        return {
            "id": photo.id,
            "service_order_id": photo.service_order_id,
            "photo_url": photo.photo_url,
            "uploaded_at": photo.uploaded_at
        }
        
    except Exception as e:
        # Se houver erro, remover arquivo se foi criado
        if os.path.exists(file_path):
            os.remove(file_path)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")

@router.get("/{order_id}/photos", response_model=List[PhotoRead])
def get_order_photos(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Lista todas as fotos de uma ordem de serviço"""
    # Verificar se ordem existe
    order = db.execute(
        select(service_orders_table).where(service_orders_table.c.id == order_id)
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Ordem de serviço não encontrada")
    
    # Buscar fotos
    photos = db.execute(
        select(os_photos_table).where(os_photos_table.c.service_order_id == order_id)
        .order_by(os_photos_table.c.uploaded_at.desc())
    ).fetchall()
    
    return [
        {
            "id": photo.id,
            "service_order_id": photo.service_order_id,
            "photo_url": photo.photo_url,
            "uploaded_at": photo.uploaded_at
        }
        for photo in photos
    ]

@router.delete("/photos/{photo_id}")
def delete_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Remove uma foto de uma ordem de serviço"""
    # Buscar foto
    photo = db.execute(
        select(os_photos_table).where(os_photos_table.c.id == photo_id)
    ).first()
    
    if not photo:
        raise HTTPException(status_code=404, detail="Foto não encontrada")
    
    try:
        # Remover arquivo do sistema
        file_path = os.path.join(UPLOAD_DIR, os.path.basename(photo.photo_url))
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Remover registro do banco
        db.execute(os_photos_table.delete().where(os_photos_table.c.id == photo_id))
        db.commit()
        
        return {"message": "Foto removida com sucesso"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao remover foto: {str(e)}")

@router.get("/uploads/{filename}")
async def serve_uploaded_file(filename: str):
    """Serve arquivos de upload"""
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")
    
    # Verificar se é uma imagem
    if not is_allowed_file(filename):
        raise HTTPException(status_code=403, detail="Tipo de arquivo não permitido")
    
    from fastapi.responses import FileResponse
    return FileResponse(file_path)
