
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import UsuarioModel
from app.schemas import UsuarioCreate, UsuarioResponse, Token
from app.auth import (
    gerar_hash_senha,
    verificar_senha,
    criar_token_acesso
)


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post(
    "/register",
    response_model=UsuarioResponse
)
def registrar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    usuario_existente = db.query(UsuarioModel).filter(
        UsuarioModel.email == usuario.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="E-mail já cadastrado"
        )

    novo_usuario = UsuarioModel(
        nome=usuario.nome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario


@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.email == form_data.username
    ).first()

    if not usuario or not verificar_senha(
        form_data.password,
        usuario.senha
    ):
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha incorretos"
        )

    token = criar_token_acesso(usuario.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
