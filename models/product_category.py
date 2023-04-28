from sqlmodel import SQLModel, Field, ForeignKey
from typing import Optional
from sqlalchemy.orm import relationship

class ProductCategory(SQLModel, table=True):
    __tablename__ = "products_categories"
    product_id: Optional[int] = Field(default=None, foreign_key="products.id", primary_key=True)
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id", primary_key=True)

