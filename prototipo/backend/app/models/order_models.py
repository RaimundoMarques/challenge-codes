from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Modelos para Clientes
class ClientBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientRead(ClientBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelos para Equipamentos
class EquipmentBase(BaseModel):
    type: str
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None

class EquipmentCreate(EquipmentBase):
    client_id: int

class EquipmentRead(EquipmentBase):
    id: int
    client_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Modelos para Ordens de Serviço
class ServiceOrderBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "open"

class ServiceOrderCreate(ServiceOrderBase):
    client_id: int
    equipment_id: int

class ServiceOrderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class ServiceOrderRead(ServiceOrderBase):
    id: int
    client_id: int
    equipment_id: int
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Relacionamentos
    client: Optional[ClientRead] = None
    equipment: Optional[EquipmentRead] = None
    user: Optional[dict] = None  # UserRead

    class Config:
        from_attributes = True

# Modelos para Checklists
class ChecklistItemBase(BaseModel):
    description: str

class ChecklistItemCreate(ChecklistItemBase):
    checklist_id: int

class ChecklistItemRead(ChecklistItemBase):
    id: int
    checklist_id: int

    class Config:
        from_attributes = True

class ChecklistBase(BaseModel):
    name: str

class ChecklistCreate(ChecklistBase):
    pass

class ChecklistRead(ChecklistBase):
    id: int
    items: Optional[List[ChecklistItemRead]] = []

    class Config:
        from_attributes = True

# Modelos para Respostas de Checklist
class ChecklistResponseBase(BaseModel):
    is_checked: bool

class ChecklistResponseCreate(ChecklistResponseBase):
    service_order_id: int
    checklist_item_id: int

class ChecklistResponseRead(ChecklistResponseBase):
    id: int
    service_order_id: int
    checklist_item_id: int
    responded_at: Optional[datetime] = None
    checklist_item: Optional[ChecklistItemRead] = None

    class Config:
        from_attributes = True

# Modelos para Fotos
class PhotoBase(BaseModel):
    photo_url: str

class PhotoCreate(PhotoBase):
    service_order_id: int

class PhotoRead(PhotoBase):
    id: int
    service_order_id: int
    uploaded_at: Optional[datetime] = None

    class Config:
        from_attributes = True
