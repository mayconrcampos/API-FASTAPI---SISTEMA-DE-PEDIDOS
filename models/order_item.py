from typing import Optional
from sqlmodel import SQLModel, Field, ForeignKey, Relationship
from typing import List
# from models.product import Product
# from models.order import Order

class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: Optional[int] = Field(default=None, foreign_key="orders.id")
    product_id: Optional[int] = Field(default=None, foreign_key="products.id")
    price: Optional[float] = Field(default=None)
    quantity: int

    order: Optional['Order'] = Relationship(back_populates="items")
    product: Optional["Product"] = Relationship(back_populates="orders")

    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "product": self.product  # inclui informações sobre o produto relacionado
        }

class OrderItem_GET(SQLModel, table=False):
    __tablename__ = "order_items"

    id: Optional[int] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    order: Optional['Order'] = None
    product: Optional["Product"] = Relationship(back_populates="orders")