from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class HotelModel(Base):
    __tablename__ = "hoteis"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    localizacao = Column(String)
    nota = Column(Float)

    quartos = relationship("QuartoModel", back_populates="hotel")


class QuartoModel(Base):
    __tablename__ = "quartos"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer)
    preco = Column(Float)
    disponivel = Column(Boolean, default=True)
    hotel_id = Column(Integer, ForeignKey("hoteis.id"))

    hotel = relationship("HotelModel", back_populates="quartos")