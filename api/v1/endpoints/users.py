from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models.user import User, User_GET, User_UP
from core.deps import get_session, get_current_user
from services.users_services import UsersServices

router = APIRouter()

@router.post(
        "/", 
        status_code=status.HTTP_201_CREATED, 
        response_model=User,
        response_model_exclude=["password"],
        description="Criar novo usuário")
async def create_usuario(user: User, db: AsyncSession = Depends(get_session)):
    return await UsersServices()._create_usuario(user=user, db=db)


@router.get(
        "/", 
        status_code=status.HTTP_200_OK, 
        response_model=List[User_GET],
        description="Listar todos os usuários cadastrados")
async def get_usuarios(db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await UsersServices()._get_usuarios(db=db)


@router.get(
        "/{id_user}", 
        status_code=status.HTTP_200_OK, 
        response_model=User_GET,
        description="Buscar usuário pelo id")
async def get_user_by_id(id_user: int, db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await UsersServices()._get_user_by_id(id_user=id_user, db=db)


@router.put(
        "/{id_user}", 
        status_code=status.HTTP_200_OK, 
        response_model=User_GET,
        description="Atualizar usuário pelo id")
async def update_user(id_user: int, user_up: User_UP, db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await UsersServices()._update_user(id_user=id_user, user_up=user_up, db=db)


@router.delete(
        "/{id_user}", 
        status_code=status.HTTP_204_NO_CONTENT,
        description="Deletar usuário pelo id")
async def delete_user(id_user: int, db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await UsersServices()._delete_user(id_user=id_user, db=db)
        

############# AUTENTICAÇÃO ###############
@router.post("/login", description="Fazer login para obter token de acesso")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    return await UsersServices()._login_user(form_data=form_data, db=db)


@router.get("/auth/logged/", response_model=User_GET, description="Obtém usuário logado pelo token de acesso")
def get_usuario_logado(user_logged: User = Depends(get_current_user)):
    return user_logged