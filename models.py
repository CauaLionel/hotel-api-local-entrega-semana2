from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class HotelModel(Base):
    __tablename__ = "hoteis"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    localizacao = Column(String)
    nota = Column(Float)

    quartos = relationship(
        "QuartoModel",
        back_populates="hotel",
        cascade="all, delete"
    )


class QuartoModel(Base):
    __tablename__ = "quartos"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer)
    preco = Column(Float)
    disponivel = Column(Boolean, default=True)
    hotel_id = Column(Integer, ForeignKey("hoteis.id"))

    hotel = relationship(
        "HotelModel",
        back_populates="quartos"
    )


class ReservaModel(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    hospede = Column(String)
    data_entrada = Column(String)
    data_saida = Column(String)
    quarto_id = Column(
        Integer,
        ForeignKey("quartos.id")
    )

    quarto = relationship("QuartoModel")

class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha = Column(String)