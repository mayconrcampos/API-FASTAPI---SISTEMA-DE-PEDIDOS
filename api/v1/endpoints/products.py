from models.product import Product, Product_With_categories
from models.user import User
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.deps import get_session, get_current_user
from typing import List

from services.products_services import ProductServices

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Product], description="Listar todos os produtos")
async def get_all_products(db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await ProductServices()._get_all_products(db=db)

@router.get("/categorias", status_code=status.HTTP_200_OK, response_model=List[Product_With_categories], description="Listar todos os produtos que possuem categorias associadas")
async def get_all_products_with_categories(db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await ProductServices()._get_all_products_with_categories(db=db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Product,description="Cadastrar novo produto")
async def create_product(product: Product, db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await ProductServices()._create_product(product=product, db=db)

@router.post("/{id_product}/categorias/{id_category}", status_code=status.HTTP_201_CREATED, response_model=Product_With_categories, description="Associar uma categoria existente a um produto")
async def create_category_for_product(id_product: int, id_category: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await ProductServices()._create_category_for_product(id_product=id_product, id_category=id_category, db=db)

@router.get(
        "/{id_product}", 
        status_code=status.HTTP_200_OK, 
        response_model=Product)
async def get_product_By_id(id_product: int, db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await ProductServices()._get_product_By_id(id_product=id_product, db=db)

@router.put(
    "/{id_product}",
    status_code=status.HTTP_200_OK,
    response_model=Product)
async def update_product(id_product: int, product: Product, db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await ProductServices()._update_product(id_product=id_product, product=product, db=db)


@router.delete("/{id_product}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id_product: int, db: AsyncSession = Depends(get_session), user_logged: User = Depends(get_current_user)):
    return await ProductServices()._delete_product(id_product=id_product, db=db)