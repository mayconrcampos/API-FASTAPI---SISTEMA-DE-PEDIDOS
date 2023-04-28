from fastapi import APIRouter
from api.v1.endpoints import users, addresses, products, categories, orders

api_router = APIRouter()

api_router.include_router(users.router, prefix="/usuarios", tags=["Usuários"])
api_router.include_router(addresses.router, prefix="/enderecos", tags=["Endereços"])
api_router.include_router(products.router, prefix="/produtos", tags=["Produtos"])
api_router.include_router(categories.router, prefix="/categorias", tags=["Categorias"])
api_router.include_router(orders.router, prefix="/pedidos", tags=["Pedidos"])