from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr


class User(SQLModel, table=True):
    __tablename__: str = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=256, index=True, nullable=False)
    email: Optional[EmailStr] = Field(unique=True)
    password: str = Field(nullable=False)
    address: List['Address'] = Relationship(back_populates="user")
    orders: List["Order"] = Relationship(back_populates="user")

    class Config:
        orm_mode = True
        exclude = ['password']


class User_UP(SQLModel, table=False):
    __tablename__: str = "users"

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class User_GET(SQLModel, table=False):
    __tablename__: str = "users"

    id: Optional[int]
    name: Optional[str]
    email: Optional[EmailStr]


