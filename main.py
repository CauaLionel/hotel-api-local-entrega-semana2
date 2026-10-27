from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import engine, Base, get_db
import models

# Cria as tabelas no banco SQLite automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Hoteleira - Semana 2")

# --- SCHEMAS (Pydantic) ---
class HotelCreate(BaseModel):
    nome: str
    localizacao: str
    nota: float

class QuartoCreate(BaseModel):
    numero: int
    preco: float
    hotel_id: int

# --- ROTAS DA API ---

@app.get("/")
def home():
    return {"mensagem": "API Hoteleira funcionando com sucesso!"}

# --- HOTÉIS ---
@app.post("/hoteis", status_code=201)
def criar_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    novo_hotel = models.HotelModel(**hotel.model_dump())
    db.add(novo_hotel)
    db.commit()
    db.refresh(novo_hotel)
    return novo_hotel

@app.get("/hoteis")
def listar_hoteis(db: Session = Depends(get_db)):
    return db.query(models.HotelModel).all()

# --- QUARTOS ---
@app.post("/quartos", status_code=201)
def criar_quarto(quarto: QuartoCreate, db: Session = Depends(get_db)):
    hotel = db.query(models.HotelModel).filter(models.HotelModel.id == quarto.hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel não encontrado")
    
    novo_quarto = models.QuartoModel(**quarto.model_dump())
    db.add(novo_quarto)
    db.commit()
    db.refresh(novo_quarto)
    return novo_quarto

@app.get("/quartos")
def listar_quartos(db: Session = Depends(get_db)):
    return db.query(models.QuartoModel).all()