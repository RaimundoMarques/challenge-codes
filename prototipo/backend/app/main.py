from fastapi import FastAPI
from .models import database

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API de Ordens de Serviço - FastAPI 🚀"}
