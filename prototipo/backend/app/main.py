from fastapi import FastAPI
from .routers import users

app = FastAPI()

# Rotas
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "API de Ordens de Serviço - FastAPI 🚀"}