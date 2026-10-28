from fastapi import FastAPI

from database import engine, Base
import models

from app.routers import hoteis, quartos, reservas, auth


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API Hoteleira",
    description="API para gerenciamento de hotéis, quartos e reservas",
    version="1.0.0"
)


app.include_router(hoteis.router)
app.include_router(quartos.router)
app.include_router(reservas.router)
app.include_router(auth.router)
@app.get("/")
def home():
    return {
        "mensagem": "API Hoteleira funcionando com sucesso!"
    }