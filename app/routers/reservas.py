from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ReservaModel, QuartoModel
from app.schemas import ReservaCreate, ReservaUpdate, ReservaResponse


router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)


@router.post("/", response_model=ReservaResponse)
def criar_reserva(
    reserva: ReservaCreate,
    db: Session = Depends(get_db)
):
    quarto = db.query(QuartoModel).filter(
        QuartoModel.id == reserva.quarto_id
    ).first()

    if not quarto:
        raise HTTPException(
            status_code=404,
            detail="Quarto não encontrado"
        )

    if not quarto.disponivel:
        raise HTTPException(
            status_code=400,
            detail="Quarto não está disponível"
        )

    nova_reserva = ReservaModel(
        hospede=reserva.hospede,
        data_entrada=reserva.data_entrada,
        data_saida=reserva.data_saida,
        quarto_id=reserva.quarto_id
    )

    quarto.disponivel = False

    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)

    return nova_reserva


@router.get("/", response_model=list[ReservaResponse])
def listar_reservas(
    db: Session = Depends(get_db)
):
    return db.query(ReservaModel).all()


@router.get("/{reserva_id}", response_model=ReservaResponse)
def buscar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    reserva = db.query(ReservaModel).filter(
        ReservaModel.id == reserva_id
    ).first()

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva não encontrada"
        )

    return reserva


@router.put("/{reserva_id}", response_model=ReservaResponse)
def atualizar_reserva(
    reserva_id: int,
    dados: ReservaUpdate,
    db: Session = Depends(get_db)
):
    reserva = db.query(ReservaModel).filter(
        ReservaModel.id == reserva_id
    ).first()

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva não encontrada"
        )

    if dados.hospede is not None:
        reserva.hospede = dados.hospede

    if dados.data_entrada is not None:
        reserva.data_entrada = dados.data_entrada

    if dados.data_saida is not None:
        reserva.data_saida = dados.data_saida

    if dados.quarto_id is not None:
        quarto = db.query(QuartoModel).filter(
            QuartoModel.id == dados.quarto_id
        ).first()

        if not quarto:
            raise HTTPException(
                status_code=404,
                detail="Novo quarto não encontrado"
            )

        reserva.quarto_id = dados.quarto_id

    db.commit()
    db.refresh(reserva)

    return reserva


@router.delete("/{reserva_id}")
def excluir_reserva(
    reserva_id: int,
    db: Session = Depends(get_db)
):
    reserva = db.query(ReservaModel).filter(
        ReservaModel.id == reserva_id
    ).first()

    if not reserva:
        raise HTTPException(
            status_code=404,
            detail="Reserva não encontrada"
        )

    quarto = db.query(QuartoModel).filter(
        QuartoModel.id == reserva.quarto_id
    ).first()

    if quarto:
        quarto.disponivel = True

    db.delete(reserva)
    db.commit()

    return {
        "mensagem": "Reserva excluída com sucesso"
    }