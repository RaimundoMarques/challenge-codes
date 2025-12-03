from sqlalchemy import Table, Column, Integer, String, Boolean, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from .auth import metadata

# Tabela de clientes
clients_table = Table(
    "clients",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(150), nullable=False),
    Column("email", String(100)),
    Column("phone", String(20)),
    Column("address", Text),
    Column("created_at", TIMESTAMP, default=func.current_timestamp())
)

# Tabela de equipamentos
equipments_table = Table(
    "equipments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("client_id", Integer, ForeignKey("clients.id"), nullable=False),
    Column("type", String(50), nullable=False),
    Column("brand", String(50)),
    Column("model", String(100)),
    Column("serial_number", String(100), unique=True),
    Column("created_at", TIMESTAMP, default=func.current_timestamp())
)

# Tabela de ordens de serviço
service_orders_table = Table(
    "service_orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("client_id", Integer, ForeignKey("clients.id"), nullable=False),
    Column("equipment_id", Integer, ForeignKey("equipments.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("title", String(150), nullable=False),
    Column("description", Text),
    Column("activities_description", Text),  # Descrição das atividades realizadas
    Column("status", String(20), default="open"),
    Column("created_at", TIMESTAMP, default=func.current_timestamp()),
    Column("updated_at", TIMESTAMP, default=func.current_timestamp())
)

# Tabela de checklists
checklists_table = Table(
    "checklists",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False)
)

# Tabela de itens de checklist
checklist_items_table = Table(
    "checklist_items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("checklist_id", Integer, ForeignKey("checklists.id"), nullable=False),
    Column("description", String(255), nullable=False)
)

# Tabela de respostas de checklist por OS
os_checklist_responses_table = Table(
    "os_checklist_responses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("service_order_id", Integer, ForeignKey("service_orders.id"), nullable=False),
    Column("checklist_item_id", Integer, ForeignKey("checklist_items.id"), nullable=False),
    Column("is_checked", Boolean, nullable=False),
    Column("responded_at", TIMESTAMP, default=func.current_timestamp())
)

# Tabela de fotos das OS
os_photos_table = Table(
    "os_photos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("service_order_id", Integer, ForeignKey("service_orders.id"), nullable=False),
    Column("photo_url", Text, nullable=False),
    Column("uploaded_at", TIMESTAMP, default=func.current_timestamp())
)
