from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
# from models.product import Product
from models.product_category import ProductCategory

class Category(SQLModel, table=True):
    __tablename__ = "categories"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, unique=True)

    products: Optional[List['Product']] = Relationship(back_populates="categories", link_model=ProductCategory)


class Category_UP(SQLModel, table=False):
    __tablename__ = "categories"
    name: Optional[str] = None