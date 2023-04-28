from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from models.product_category import ProductCategory
from models.category import Category
from models.order_item import OrderItem

class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    description: str = Field(nullable=True)
    price: float = Field()

    categories: Optional[List["Category"]] = Relationship(back_populates="products", link_model=ProductCategory)
    orders: Optional[List['OrderItem']] = Relationship(back_populates="product")

class Product_UP(SQLModel, table=False):
    __tablename__ = "products"

    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None


class Product_With_categories(SQLModel, table=False):
    __tablename__ = "products"
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    categories: Optional[List["Category"]] = None
