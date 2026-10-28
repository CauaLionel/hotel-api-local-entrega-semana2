from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import QuartoModel, HotelModel
from app.schemas import QuartoCreate, QuartoUpdate, QuartoResponse
from app.auth import obter_usuario_atual


router = APIRouter(
    prefix="/quartos",
    tags=["Quartos"]
)


@router.post("/", response_model=QuartoResponse)
def criar_quarto(
    quarto: QuartoCreate,
    db: Session = Depends(get_db),
    usuario_atual=Depends(obter_usuario_atual)
):
    hotel = db.query(HotelModel).filter(
        HotelModel.id == quarto.hotel_id
    ).first()

    if not hotel:
        raise HTTPException(
            status_code=404,
            detail="Hotel não encontrado"
        )

    novo_quarto = QuartoModel(
        numero=quarto.numero,
        preco=quarto.preco,
        disponivel=quarto.disponivel,
        hotel_id=quarto.hotel_id
    )

    db.add(novo_quarto)
    db.commit()
    db.refresh(novo_quarto)

    return novo_quarto


@router.get("/", response_model=list[QuartoResponse])
def listar_quartos(
    db: Session = Depends(get_db)
):
    return db.query(QuartoModel).all()


@router.get("/{quarto_id}", response_model=QuartoResponse)
def buscar_quarto(
    quarto_id: int,
    db: Session = Depends(get_db)
):
    quarto = db.query(QuartoModel).filter(
        QuartoModel.id == quarto_id
    ).first()

    if not quarto:
        raise HTTPException(
            status_code=404,
            detail="Quarto não encontrado"
        )

    return quarto


@router.put("/{quarto_id}", response_model=QuartoResponse)
def atualizar_quarto(
    quarto_id: int,
    dados: QuartoUpdate,
    db: Session = Depends(get_db),
    usuario_atual=Depends(obter_usuario_atual)
):
    quarto = db.query(QuartoModel).filter(
        QuartoModel.id == quarto_id
    ).first()

    if not quarto:
        raise HTTPException(
            status_code=404,
            detail="Quarto não encontrado"
        )

    if dados.numero is not None:
        quarto.numero = dados.numero

    if dados.preco is not None:
        quarto.preco = dados.preco

    if dados.disponivel is not None:
        quarto.disponivel = dados.disponivel

    db.commit()
    db.refresh(quarto)

    return quarto


@router.delete("/{quarto_id}")
def excluir_quarto(
    quarto_id: int,
    db: Session = Depends(get_db),
    usuario_atual=Depends(obter_usuario_atual)
):
    quarto = db.query(QuartoModel).filter(
        QuartoModel.id == quarto_id
    ).first()

    if not quarto:
        raise HTTPException(
            status_code=404,
            detail="Quarto não encontrado"
        )

    db.delete(quarto)
    db.commit()

    return {
        "mensagem": "Quarto excluído com sucesso"
    }