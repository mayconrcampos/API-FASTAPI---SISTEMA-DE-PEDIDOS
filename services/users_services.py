from models.user import User
from core.security import generate_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound, SQLAlchemyError
from fastapi import HTTPException, status, Response
from typing import List
from sqlmodel import select
from models.user import User, User_GET, User_UP
from fastapi.security import OAuth2PasswordRequestForm
from core.auth import autenticar, generate_access_token
from fastapi.responses import JSONResponse

class UsersServices:
    @staticmethod
    async def _create_usuario(user: User, db: AsyncSession):
        new_user: User = User(
                name=user.name,
                email=user.email,
                password=generate_password_hash(user.password)
            )
        try:
            async with db as session:
                session.add(new_user)
                await session.commit()
                await session.close()

                return new_user
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))

    @staticmethod
    async def _get_usuarios(db: AsyncSession):
        try:
            async with db as session:
                query = select(User)
                result = await session.execute(query)
                usuarios: List[User_GET] = result.scalars().all()

                return usuarios

        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))

    @staticmethod
    async def _get_user_by_id(id_user: int, db: AsyncSession):
        try:
            async with db as session:
                query = select(User).where(User.id == id_user)
                result = await session.execute(query)
                user: User_GET = result.scalar_one()

                if user:
                    return user
        except IntegrityError:
            raise HTTPException(detail="Ocorreu algum erro ao tentar listar usuários.", status_code=status.HTTP_400_BAD_REQUEST)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))

    @staticmethod
    async def _update_user(id_user: int, user_up: User_UP, db: AsyncSession):
        try:
            async with db as session:
                query = select(User).where(User.id == id_user)
                result = await session.execute(query)
                user_db: User_UP = result.scalar_one()

                usuario_up = user_up.dict(exclude_unset=True)

                for key, value in usuario_up.items():
                    if key == "password":
                        setattr(user_db, key, generate_password_hash(value))
                    else:
                        setattr(user_db, key, value)

                session.add(user_db)
                await session.commit()
                await session.refresh(user_db)

                return user_db

        except IntegrityError as e:
            raise HTTPException(detail="Ocorreu algum erro ao tentar listar usuários." + str(e), status_code=status.HTTP_400_BAD_REQUEST)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
        
    @staticmethod
    async def _delete_user(id_user: int, db: AsyncSession):
        try:
            async with db as session:
                query = select(User).where(User.id == id_user)
                result = await session.execute(query) 
                user: User = result.scalar_one()

                await session.delete(user)
                await session.commit()

                return Response(status_code=status.HTTP_204_NO_CONTENT)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))

    ############## SERVICES DE AUTENTICAÇÃO ################
    @staticmethod
    async def _login_user(form_data: OAuth2PasswordRequestForm, db: AsyncSession):
        user = await autenticar(email=form_data.username, senha=form_data.password, db=db)

        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="As credenciais estão incorretas.")
        return JSONResponse(content={"access_token":        generate_access_token(sub=user.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)  