from fastapi import status, HTTPException
from models.category import Category, Category_UP
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlmodel import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class CategoryServices:
    @classmethod
    async def _get_all_categories(cls, db: AsyncSession):
        try:
            async with db as session:
                query = select(Category)
                results = await session.execute(query)
                categories: List[Category] = results.scalars().all()

                if categories:
                    return categories
            
                raise HTTPException(detail="Nenhuma categoria cadastrada.", status_code=status.HTTP_404_NOT_FOUND)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _get_category_By_id(cls, id_category: int, db: AsyncSession):
        try:
            async with db as session:
                query = select(Category).where(Category.id == id_category)
                result = await session.execute(query)
                category: Category = result.scalar_one_or_none()

                if category:
                    return category
                raise HTTPException(detail="Categoria não encontrada.", status_code=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            raise HTTPException(detail="Houve um erro ao listar categorias de produtos.", status_code=status.HTTP_400_BAD_REQUEST)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _create_category(cls, category: Category, db: AsyncSession):
        try:
            new_category: Category = Category(
                name=category.name
            )
            async with db as session:
                session.add(new_category)
                await session.commit()
                await session.close()

                return new_category
              
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _update_category(cls, id_category: int, category: Category_UP, db: AsyncSession):
        try:
            async with db as session:
                query = select(Category).where(Category.id == id_category)
                result = await session.execute(query)
                category_db: Category = result.scalar_one_or_none()

                if category_db:
                    category_update = category.dict()

                    for k, v in category_update.items():
                         setattr(category_db, k, v)
                    
                    session.add(category_db)
                    await session.commit()
                    await session.close()

                    return category_db
                raise HTTPException(detail="Categoria não encontrada.", status_code=status.HTTP_404_NOT_FOUND)
        
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _delete_category(cls, id_category: int, db: AsyncSession):
        try:
            async with db as session:
                query = select(Category).where(Category.id == id_category)
                result = await session.execute(query)
                category: Category = result.scalar_one_or_none()

                if category:
                    await session.delete(category)
                    await session.commit()
                    await session.close()

                    return category
                raise HTTPException(detail="Categoria não encontrada.", status_code=status.HTTP_404_NOT_FOUND) 
         
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))