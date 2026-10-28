
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models import UsuarioModel


SECRET_KEY = "chave-secreta-hotel-api"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def verificar_senha(
    senha: str,
    senha_hash: str
):
    return pwd_context.verify(
        senha,
        senha_hash
    )


def gerar_hash_senha(senha: str):
    return pwd_context.hash(senha)


def criar_token_acesso(
    usuario_id: int
):
    expiracao = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados = {
        "sub": str(usuario_id),
        "exp": expiracao
    }

    return jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credenciais_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise credenciais_exception

    except JWTError:
        raise credenciais_exception

    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id == int(usuario_id)
    ).first()

    if usuario is None:
        raise credenciais_exception

    return usuario
