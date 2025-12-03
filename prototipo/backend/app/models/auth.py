from sqlalchemy import Table, Column, Integer, String, Boolean, Text, TIMESTAMP, ForeignKey, MetaData
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

metadata = MetaData()

# Tabela de usuários
users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True, nullable=False),
    Column("password_hash", Text, nullable=False),
    Column("name", String(100)),
    Column("email", String(100), unique=True),
    Column("role", String(30), default="tecnico"),
    Column("is_active", Boolean, default=True),
    Column("created_at", TIMESTAMP, default=func.current_timestamp())
)

# Tabela de tokens de autenticação
auth_tokens_table = Table(
    "auth_tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("token", Text, unique=True, nullable=False),
    Column("created_at", TIMESTAMP, default=func.current_timestamp()),
    Column("expires_at", TIMESTAMP),
    Column("is_revoked", Boolean, default=False)
)
