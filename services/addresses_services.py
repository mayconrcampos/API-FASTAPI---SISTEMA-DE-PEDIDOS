import requests
from requests.exceptions import ConnectionError
from fastapi import HTTPException, status

from fastapi import status, HTTPException
from models.address import Address, Address_GET, Address_UP, Address_GET_BY_CEP
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List
from sqlmodel import select
from sqlalchemy.orm import selectinload, joinedload


######## SERVICES ADDRESS ###########
class AddressServices:
    @classmethod
    def _get_address_by_cep(cls, url):
        response = requests.get(url)

        resp = response.json()
        
        if "erro" in resp:
            return False
        return resp
    
    @classmethod
    def format_cep(cls, cep: str):
        """Transforma CEP no formato 00000000 em 00000-000"""
        return f'{cep[:5]}-{cep[5:]}'

    @classmethod
    def validate_cep(cls, cep: str):
        try:
            cep = cep.replace("-", "")
            
            if len(cep) != 8:
                raise HTTPException(detail="Campo CEP inválido", status_code=status.HTTP_406_NOT_ACCEPTABLE) 

        except AttributeError as e:
            raise HTTPException(detail=f"AttributeError: {e} - É preciso enviar o CEP", status_code=status.HTTP_400_BAD_REQUEST)
        except TypeError as e:
            raise HTTPException(detail=f"TypeError: {e}", status_code=status.HTTP_400_BAD_REQUEST)
        
        try:
            int(cep)
        except ValueError:
            raise HTTPException(detail="Campo CEP inválido",  status_code=status.HTTP_406_NOT_ACCEPTABLE)
        
        try:
            address = cls._get_address_by_cep(f"https://viacep.com.br/ws/{cep}/json/")
            if not address:
                raise HTTPException(detail="CEP inválido",  status_code=status.HTTP_406_NOT_ACCEPTABLE)
            
            return address
        except ConnectionError:
            raise HTTPException(detail="Falha na API ViaCEP, favor tentar novamente",  status_code=status.HTTP_406_NOT_ACCEPTABLE)
        
    @classmethod
    async def _get_users_by_cep(cls, cep: str, db: AsyncSession):
        if cls.validate_cep(cep):
            try:
                async with db as session:
                    query = select(Address).join(Address.user).options(joinedload(Address.user)).where(Address.postal_code == cls.validate_cep(cep)["cep"])

                    results = await session.execute(query)
                    addresses: List[Address_GET_BY_CEP] = results.scalars().all()

                    if addresses:
                        return addresses
                    raise HTTPException(detail=f"Não existem usuários com cep {cls.format_cep(cep)}.", status_code=status.HTTP_400_BAD_REQUEST)
            
            except SQLAlchemyError as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))


    @classmethod
    async def _create_address(cls, address: Address, db: AsyncSession):
        endereco = cls.validate_cep(address.postal_code)

        new_address: Address = Address(
            user_id=address.user_id,
            description=address.description,
            postal_code=endereco['cep'],
            street=endereco['logradouro'] if endereco['logradouro'] else address.street,
            complement=address.complement,
            neighborhood=endereco['bairro'] if endereco['bairro'] else address.neighborhood,
            city=endereco['localidade'],
            state=endereco['uf']
        )
        try:
            async with db as session:
                session.add(new_address)
                await session.commit()
                await session.close()

                return new_address
        except IntegrityError as e:
            error_message = str(e.args[0]).split('\n')[1]
            if "is not present in table" in error_message:
                raise HTTPException(detail="Usuário não existe", status_code=status.HTTP_400_BAD_REQUEST)
    
    @classmethod
    async def _get_all_addresses(cls, db: AsyncSession):
        try:
            async with db as session:
                query = select(Address).options(joinedload(Address.user))
                result = await session.execute(query) 
                addresses = result.scalars().all()

                if addresses:
                    return addresses
                raise HTTPException(detail="Nenhum endereço cadastrado.", status_code=status.HTTP_404_NOT_FOUND) 
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))


    @classmethod
    async def _get_addresses_by_id_user(cls, user_id: int, db: AsyncSession):
        try:
            async with db as session:
                query_user = select(User).where(User.id == user_id)
                result = await session.execute(query_user)
                user: User = result.scalar_one_or_none()
                if user:
                    query = select(Address).join(User).options(joinedload(Address.user)).where(Address.user_id == user_id)
                    results = await session.execute(query)
                    addresses: List[Address_GET] = results.scalars().all()

                    if addresses:
                        return addresses
                    raise HTTPException(detail="Nenhum endereço cadastrado para este usuário", status_code=status.HTTP_404_NOT_FOUND)
            raise HTTPException(detail="Usuário não encontrado", status_code=status.HTTP_404_NOT_FOUND)

        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _update_address(cls, address_id: int, address: Address_UP, db: AsyncSession):
        try:
            async with db as session:
                query = select(Address).options(selectinload(Address.user)).where(Address.id == address_id)
                result = await session.execute(query)
                address_db: Address = result.scalar_one_or_none()
                address_up = address.dict(exclude_unset=True)

                if address_db:
                    if "postal_code" in address_up:
                        endereço = cls.validate_cep(address_up['postal_code'])
                        address_db.description = address_up['description']
                        address_db.postal_code = endereço['cep']
                        address_db.street = endereço["logradouro"] if endereço['logradouro'] else address_up['street']
                        address_db.complement = address_up["complement"]
                        address_db.neighborhood = endereço["bairro"] if endereço['bairro'] else address_up['neighborhood']
                        address_db.city = endereço['localidade']
                        address_db.state = endereço['uf']

                        session.add(address_db)
                        await session.commit()
                        await session.refresh(address_db)
                    else:
                        for k, v in address_up.items():
                            setattr(address_db, k, v)

                        session.add(address_db)
                        await session.commit()
                        await session.refresh(address_db)    
                    
                    return address_db
            raise HTTPException(detail="Endereço não encontrado", status_code=status.HTTP_404_NOT_FOUND)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _delete_address(cls, id_address: int, db: AsyncSession):
        try:
            async with db as session:
                query = select(Address).where(Address.id == id_address)
                result = await session.execute(query)

                address_delete: Address = result.scalar_one_or_none()
                if address_delete:
                    await session.delete(address_delete)
                    await session.commit()
                    await session.close()

                    return address_delete
                raise HTTPException(detail="Endereço não encontrado", status_code=status.HTTP_404_NOT_FOUND)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))