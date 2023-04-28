from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, ForeignKey
from models.order_item import OrderItem
from enum import Enum
from models.user import User
from models.address import Address

class StatusField(Enum):
    PENDENTE: str = "Pendente"
    PAGO: str = "Pago"
    ENVIADO: str = "Enviado"
    ENTREGUE: str = "Entregue"
    CANCELADO: str = "Cancelado"

    def to_dict(self):
        return {
            "PENDENTE": self.PENDENTE,
            "PAGO": self.PAGO,
            "ENVIADO": self.ENVIADO,
            "ENTREGUE": self.ENTREGUE,
            "CANCELADO": self.CANCELADO
        }
    

class Order(SQLModel, table=True):
    __tablename__ = "orders"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", sa_column=ForeignKey("users.id"))
    address_id: Optional[int] = Field(default=None, foreign_key="addresses.id", sa_column=ForeignKey("addresses.id"))
    status: Optional[StatusField] = Field(default="Pendente")
    order_date: Optional[datetime] = Field(default=datetime.now())

    user: Optional['User'] = Relationship(back_populates="orders")
    address: Optional['Address'] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")


class Order_GET(SQLModel, table=False):
    id: Optional[int] = None
    status: Optional[StatusField] = None
    order_date: Optional[datetime] = None
    user: Optional["User"] = None
    address: Optional["Address"] = None
    items: Optional[List["OrderItem"]] = None

    class Config:
        orm_mode = True


class Order_UP(SQLModel):
    id: Optional[int] = None
    status: Optional[StatusField] = None
    order_date: Optional[datetime] = None
    user: Optional[User] = None
    address: Optional[Address] = None
    items: Optional[List[OrderItem]] = None

    class Config:
        orm_mode = True
