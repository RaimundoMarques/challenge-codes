from fastapi import FastAPI
from .routers import users, auth, orders
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema de Ordens de Serviço",
    description="API para gerenciamento de ordens de serviço",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir requisições do frontend
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Rotas
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {
        "message": "API de Ordens de Serviço - FastAPI 🚀",
        "version": "1.0.0",
        "docs": "/docs"
    }