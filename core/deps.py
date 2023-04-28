from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from sqlmodel import SQLModel, select
from core.database import Session, Session_Test
from core.auth import oauth2_schema, token_expirado
from core.configs import settings
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from models.user import User
from models.product import Product
from models.order import Order
from jose import jwt, JWTError
from sqlalchemy.orm import make_transient, joinedload, selectinload, load_only

class TokenData(SQLModel, table=False):
    username: Optional[int] = None


async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()

async def get_session_test() -> Generator:
    session: AsyncSession = Session_Test()

    try:
        yield session
    finally:
        await session.close()

async def get_current_user(db: Session = Depends(get_session), token: str = Depends(oauth2_schema)) -> User:
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        if token_expirado(exp=payload.get("exp")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado. Favor refazer login.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        username: int = payload.get("sub")

        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credential_exception
    
    try:    
        async with db as session:
            query = select(User).where(User.id == token_data.username)
            result = await session.execute(query)
            usuario: User = result.scalar_one()

            return usuario

    except NoResultFound:
        raise HTTPException(detail="Houve um problema com autenticação.", status_code=status.HTTP_404_NOT_FOUND)



async def get_product(product_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        product = await session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
        return product

async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return user

async def get_order(order_id: int, db: AsyncSession = Depends(get_session)):
    try:
        async with db as session:
            # Adicione o load_only aqui para carregar apenas o id do usuário
            query = select(Order).options(joinedload(Order.user)).where(Order.id == order_id)
            result = await session.execute(query)
            order: Order = result.scalar_one_or_none()

            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
            await session.refresh(order)
            return order
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))

            