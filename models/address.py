from sqlmodel import SQLModel, Field, Column, ForeignKey, Integer, Relationship
from typing import Optional, List
from .user import User, User_GET

class Address(SQLModel, table=True):
    __tablename__ = "addresses"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    description: Optional[str] = Field(default= None, max_length=255)
    postal_code: Optional[str] = Field(default=None, max_length=10)
    street: Optional[str] = Field(default=None, max_length=255)
    complement: Optional[str] = Field(max_length=255, nullable=True)
    neighborhood: Optional[str] = Field(default=None, max_length=255)
    city: Optional[str] = Field(default=None, max_length=255)
    state: Optional[str] = Field(default=None, max_length=2)
    user: Optional[User] = Relationship(back_populates="address")
    orders: List["Order"] = Relationship(back_populates="address")

class Address_GET(SQLModel, table=False):
    __tablename__ = "addresses"

    id: Optional[int]
    # user_id: Optional[int]
    description: Optional[str]
    postal_code: Optional[str]
    street: Optional[str]
    complement: Optional[str]
    neighborhood: Optional[str]
    city: Optional[str]
    state: Optional[str]
    user: Optional[User] = None

class Address_GET_ALL(SQLModel, table=False):
    __tablename__ = "addresses"

    id: Optional[int]
    # user_id: Optional[int]
    description: Optional[str]
    postal_code: Optional[str]
    street: Optional[str]
    complement: Optional[str]
    neighborhood: Optional[str]
    city: Optional[str]
    state: Optional[str]
    user: Optional[User] = None


class Address_GET_BY_CEP(SQLModel, table=False):
    __tablename__ = "addresses"

    user: Optional[User]
    # id: Optional[int]
    # description: Optional[str]
    postal_code: Optional[str]
    street: Optional[str]
    # complement: Optional[str]
    # neighborhood: Optional[str]
    city: Optional[str]
    state: Optional[str]

class Address_UP(SQLModel, table=False):
    __tablename__ = "addresses"

    description: Optional[str] = None
    postal_code: Optional[str] = None
    street: Optional[str] = None
    complement: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None