from models.product import Product, Product_With_categories
from models.category import Category
from models.product_category import ProductCategory
from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from sqlmodel import select
from sqlalchemy.orm import joinedload

class ProductServices:
    @classmethod
    async def _get_all_products(cls, db: AsyncSession):
        try:
            async with db as session:
                query = select(Product)
                result = await session.execute(query)
                products: Product = result.scalars().all()

                if products:
                    return products
                raise HTTPException(detail="Nenhum produto cadastrado.",    status_code=status.HTTP_404_NOT_FOUND) 
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))

    @classmethod
    async def _get_all_products_with_categories(cls, db: AsyncSession):
        try:
            async with db as session:
                query = select(Product).options(joinedload(Product.categories)).join(ProductCategory).join(Category)
                result = await session.execute(query)
                products: List[Product_With_categories] = result.unique().scalars().all()
    
                if products:
                    return products
                raise HTTPException(detail="Nenhum produto cadastrado.", status_code=status.HTTP_404_NOT_FOUND) 
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _create_product(cls, product: Product, db: AsyncSession):
        new_product: Product = Product(
        name=product.name,
        description=product.description,
        price=product.price
        )
        try:
            async with db as session:
                session.add(new_product)
                await session.commit()
                await session.refresh(new_product)
                await session.close()

            return product
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _create_category_for_product(cls, id_product: int, id_category: int, db: AsyncSession):
        try:
            async with db as session:
                query_product = select(Product).where(Product.id == id_product)
                result_product = await session.execute(query_product)
                product: Product = result_product.scalar_one_or_none()

                if product:
                    query_category = select(Category).where(Category.id == id_category)
                    result_category = await session.execute(query_category)
                    category: Category = result_category.scalar_one_or_none()

                    if category:
                        product_category: ProductCategory = ProductCategory(product_id=product.id, category_id=category.id)

                        session.add(product_category)
                        await session.commit()
                        await session.refresh(product_category)
                    
                        query = select(Product).options(joinedload(Product.categories)).where(Product.id == id_product).join(ProductCategory).join(Category)
                        result = await session.execute(query)
                        product: Product_With_categories = result.unique().scalar_one_or_none()
                        return product

                    raise HTTPException(detail="Categoria não encontrada.", status_code=status.HTTP_404_NOT_FOUND)     
                raise HTTPException(detail="Produto não encontrado.", status_code=status.HTTP_404_NOT_FOUND) 
        
        except SQLAlchemyError as e:
            error_message = str(e.args[0]).split('\n')[1].replace("DETAIL:  Key ", "")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + error_message)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _get_product_By_id(cls, id_product: int, db: AsyncSession):
        try:
            async with db as session:
                query = select(Product).where(Product.id == id_product)
                result = await session.execute(query)
                product: Product_With_categories = result.unique().scalar_one_or_none()
                    
                if product:
                    return product
                raise HTTPException(detail="Nenhum produto cadastrado.", status_code=status.HTTP_404_NOT_FOUND) 
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _update_product(cls, id_product: int, product: Product, db: AsyncSession):
        try:
            async with db as session:
                query = select(Product).where(Product.id == id_product)
                result = await session.execute(query)
                product_db: Product = result.scalar_one_or_none()
                if product_db:
                    product_up = product.dict(exclude_unset=True)
                    for k, v in product_up.items():
                        setattr(product_db, k, v)

                    session.add(product_db)
                    await session.commit()
                    await session.close()

                    return product_db
                raise HTTPException(detail="Nenhum produto encontrado.", status_code=status.HTTP_404_NOT_FOUND) 
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _delete_product(cls, id_product: int, db: AsyncSession):
        try:
            async with db as session:
                query = select(Product).where(Product.id == id_product)
                result = await session.execute(query)
                product: Product = result.scalar_one_or_none()

                if product:
                    await session.delete(product)
                    await session.commit()
                    await session.close()
            
                    return product
                raise HTTPException(detail="Produto não encontrado", status_code=status.HTTP_404_NOT_FOUND)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))