from pydantic import BaseModel
from typing import Optional


# =========================
# HOTÉIS
# =========================

class HotelBase(BaseModel):
    nome: str
    localizacao: str
    nota: float


class HotelCreate(HotelBase):
    pass


class HotelUpdate(BaseModel):
    nome: Optional[str] = None
    localizacao: Optional[str] = None
    nota: Optional[float] = None


class HotelResponse(HotelBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# QUARTOS
# =========================

class QuartoBase(BaseModel):
    numero: int
    preco: float
    disponivel: bool = True
    hotel_id: int


class QuartoCreate(QuartoBase):
    pass


class QuartoUpdate(BaseModel):
    numero: Optional[int] = None
    preco: Optional[float] = None
    disponivel: Optional[bool] = None


class QuartoResponse(QuartoBase):
    id: int

    class Config:
        from_attributes = True


# =========================
# RESERVAS
# =========================

class ReservaBase(BaseModel):
    hospede: str
    data_entrada: str
    data_saida: str
    quarto_id: int


class ReservaCreate(ReservaBase):
    pass


class ReservaUpdate(BaseModel):
    hospede: Optional[str] = None
    data_entrada: Optional[str] = None
    data_saida: Optional[str] = None
    quarto_id: Optional[int] = None


class ReservaResponse(ReservaBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str        