from fastapi import FastAPI
from .routers import users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir requisições do frontend
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Rotas
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "API de Ordens de Serviço - FastAPI 🚀"}