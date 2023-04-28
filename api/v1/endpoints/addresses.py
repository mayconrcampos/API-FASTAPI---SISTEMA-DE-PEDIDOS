from fastapi import APIRouter, status, Depends
from models.address import Address, Address_GET, Address_UP, Address_GET_BY_CEP, Address_GET_ALL
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session, get_current_user
from typing import List

from services.addresses_services import AddressServices


router = APIRouter()

@router.get("/user/cep/{cep}", status_code=status.HTTP_200_OK, response_model=List[Address_GET_BY_CEP], response_model_exclude={"user": {"password"}}, description="Listar usuários por CEP")
async def get_users_by_cep(cep: str, db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await AddressServices()._get_users_by_cep(cep=cep, db=db)

@router.post("/", status_code=status.HTTP_201_CREATED, description="Cadastrar novo endereço para um usuário")
async def create_address(address: Address, db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await AddressServices()._create_address(address=address, db=db)

@router.get(
        "/", 
        status_code=status.HTTP_200_OK, 
        response_model=List[Address_GET_ALL], 
        response_model_exclude={"user": {"password"}},
        description="Listar todos os endereços cadastrados")
async def get_all_addresses(db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await AddressServices()._get_all_addresses(db=db)

@router.get(
    "/user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=List[Address_GET],
    response_model_exclude={"user": {"password"}},
    description="Listar endereços cadastrados por id de usuário")
async def get_addresses_by_id_user(user_id: int, db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await AddressServices()._get_addresses_by_id_user(user_id=user_id, db=db)

@router.put(
    "/{address_id}",
     status_code=status.HTTP_200_OK,
     response_model=Address_GET,
     response_model_exclude={"user": {"password"}},
     description="Atualizar endereços por id")
async def update_address(address_id: int, address: Address_UP, db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await AddressServices()._update_address(address_id=address_id, address=address, db=db)
    

@router.delete("/{id_address}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(id_address: int, db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await AddressServices()._delete_address(id_address=id_address, db=db)