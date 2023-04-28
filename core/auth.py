from jose import jwt 
from models.user import User
from core.configs import settings
from core.security import validar_senha

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException, status, Depends

from pydantic import EmailStr
from typing import Optional

from datetime import datetime, timedelta
from pytz import timezone

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/usuarios/login"
)

async def autenticar(email: EmailStr, senha: str, db: AsyncSession) -> Optional[User]:
    try:
        async with db as session:
            query = select(User).where(User.email == email)
            result = await session.execute(query)
            usuario: User = result.scalar_one()

            if validar_senha(senha=senha, hash_senha=usuario.password):
                return usuario
            return None

    except NoResultFound:
        raise HTTPException(detail="Usuário não encontrado", status_code=status.HTTP_404_NOT_FOUND)


def _criar_token(tipo_token: str, tempo_vida: timedelta, sub: str) -> str:
    payload = {}
    sp = timezone("America/Sao_Paulo")
    expira = datetime.now(tz=sp) + tempo_vida

    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)

def generate_access_token(sub: str) -> str:

    return _criar_token(
        tipo_token="access_token",
        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES),
        sub=sub
    )

def token_expirado(exp: int) -> bool:
    import time
    current_time: int = time.time()

    if current_time > exp:
        return True
    return False
