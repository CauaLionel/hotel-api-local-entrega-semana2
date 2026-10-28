
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import HotelModel, UsuarioModel
from app.schemas import HotelCreate, HotelUpdate, HotelResponse
from app.auth import obter_usuario_atual


router = APIRouter(
    prefix="/hoteis",
    tags=["Hotéis"]
)


@router.post("/", response_model=HotelResponse)
def criar_hotel(
    hotel: HotelCreate,
    db: Session = Depends(get_db),
    usuario: UsuarioModel = Depends(obter_usuario_atual)
):
    novo_hotel = HotelModel(
        nome=hotel.nome,
        localizacao=hotel.localizacao,
        nota=hotel.nota
    )

    db.add(novo_hotel)
    db.commit()
    db.refresh(novo_hotel)

    return novo_hotel


@router.get("/", response_model=list[HotelResponse])
def listar_hoteis(
    db: Session = Depends(get_db)
):
    return db.query(HotelModel).all()


@router.get("/{hotel_id}", response_model=HotelResponse)
def buscar_hotel(
    hotel_id: int,
    db: Session = Depends(get_db)
):
    hotel = db.query(HotelModel).filter(
        HotelModel.id == hotel_id
    ).first()

    if not hotel:
        raise HTTPException(
            status_code=404,
            detail="Hotel não encontrado"
        )

    return hotel


@router.put("/{hotel_id}", response_model=HotelResponse)
def atualizar_hotel(
    hotel_id: int,
    dados: HotelUpdate,
    db: Session = Depends(get_db),
    usuario: UsuarioModel = Depends(obter_usuario_atual)
):
    hotel = db.query(HotelModel).filter(
        HotelModel.id == hotel_id
    ).first()

    if not hotel:
        raise HTTPException(
            status_code=404,
            detail="Hotel não encontrado"
        )

    if dados.nome is not None:
        hotel.nome = dados.nome

    if dados.localizacao is not None:
        hotel.localizacao = dados.localizacao

    if dados.nota is not None:
        hotel.nota = dados.nota

    db.commit()
    db.refresh(hotel)

    return hotel


@router.delete("/{hotel_id}")
def excluir_hotel(
    hotel_id: int,
    db: Session = Depends(get_db),
    usuario: UsuarioModel = Depends(obter_usuario_atual)
):
    hotel = db.query(HotelModel).filter(
        HotelModel.id == hotel_id
    ).first()

    if not hotel:
        raise HTTPException(
            status_code=404,
            detail="Hotel não encontrado"
        )

    db.delete(hotel)
    db.commit()

    return {
        "mensagem": "Hotel excluído com sucesso"
    }
