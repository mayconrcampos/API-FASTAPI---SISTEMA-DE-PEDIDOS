from fastapi import APIRouter, status, Depends
from models.category import Category, Category_UP
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.deps import get_session, get_current_user

from services.categories_services import CategoryServices

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Category])
async def get_all_categories(db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await CategoryServices()._get_all_categories(db=db)


@router.get("/{id_category}", status_code=status.HTTP_200_OK, response_model=Category)
async def get_category_By_id(id_category: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await CategoryServices()._get_category_By_id(id_category=id_category, db=db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create_category(category: Category, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await CategoryServices()._create_category(category=category, db=db)

@router.put("/{id_category}", status_code=status.HTTP_200_OK, response_model=Category)
async def update_category(id_category: int, category: Category_UP, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await CategoryServices()._update_category(id_category=id_category, category=category, db=db)

@router.delete("/{id_category}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id_category: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await CategoryServices()._delete_category(id_category=id_category, db=db)