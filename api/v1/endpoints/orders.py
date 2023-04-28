from fastapi import APIRouter, status, Depends
from models.order import Order, Order_GET, Order_UP
from models.user import User
from models.order_item import OrderItem
from models.product import Product
from core.deps import get_session, get_current_user, get_product, get_order
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from services.orders_items_services import OrderItemServices

router = APIRouter()


@router.get(
        "/", 
        status_code=status.HTTP_200_OK, 
        response_model=List[Order_GET], 
        response_model_exclude={"user": {"password"}},
        description="Listar todos os pedidos cadastrados")
async def get_all_orders(db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await OrderItemServices()._get_all_orders(db=db)
    
@router.get(
        "/{start_date}/{end_date}", 
        response_model=List[Order_GET], 
        response_model_exclude={"user": {"password"}},
        description="Listar pedidos filtrados por data de início e fim e ordenados pelo ID")
async def get_orders_by_date_range(start_date: str, end_date: str, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await OrderItemServices()._get_orders_by_date_range(start_date=start_date, end_date=end_date, db=db)


@router.get(
        "/{id_order}", 
        status_code=status.HTTP_200_OK, 
        response_model=Order_GET, 
        response_model_exclude={"user": {"password"}},
        description="Listar todos os pedidos cadastrados")
async def get_order_by_id(id_order: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await OrderItemServices()._get_order_by_id(id_order=id_order, db=db)


@router.get(
        "/listar/usuario/{id_user}", 
        status_code=status.HTTP_200_OK, 
        response_model=List[Order_GET], 
        response_model_exclude={"user": {"password"}}, 
        description="Listar todos os pedidos de um usuário")
async def get_order_by_user_id(id_user: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await OrderItemServices()._get_order_by_user_id(id_user=id_user, db=db)



@router.post(
        "/", 
        status_code=status.HTTP_201_CREATED, 
        description="Cadastrar novo Pedido", 
        response_model=Order_GET)
async def create_order(order: Order, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await OrderItemServices()._create_order(order=order, db=db)


@router.put(
        "/{order_id}/items/{product_id}", 
        status_code=status.HTTP_201_CREATED, 
        description="Inserir novo item a um pedido cadastrado", 
        response_model=OrderItem)
async def insert_item_to_order(order_id: int, product_id: int, item: OrderItem, order: Order = Depends(get_order) , product: Product = Depends(get_product), db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await OrderItemServices()._insert_item_to_order(order_id=order_id, product_id=product_id, item=item, order=order, db=db)


@router.put(
        "/{order_id}", 
        status_code=status.HTTP_200_OK, 
        description="Atualiza um pedido cadastrado", 
        response_model=Order_GET, 
        response_model_exclude={"user": {"password"}})
async def change_status(order_id: int, order_up: Order_UP, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await OrderItemServices()._change_status(order_id=order_id, order_up=order_up, db=db)
    

@router.put(
        "/{order_id}/item/{product_id}/qtd/{quantity}", 
        status_code=status.HTTP_200_OK, 
        response_model=OrderItem, 
        description="Atualizar quantidade de itens do pedido")
async def update_quantity_items(order_id: int, product_id: int, quantity: int, Order: Order = Depends(get_order), product: Product = Depends(get_product), db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await OrderItemServices()._update_quantity_items(quantity=quantity, Order=Order, product=product, db=db)
    
@router.delete(
        "/delete/by/order/{order_id}/item/{product_id}", 
        status_code=status.HTTP_204_NO_CONTENT, 
        description="Deletar item do pedido")
async def delete_product_order_item(order_id: int, product_id: int, Order: Order = Depends(get_order), product: Product = Depends(get_product), db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await OrderItemServices()._delete_product_order_item(Order=Order, product=product, db=db)


@router.delete(
        "/{id_order}", 
        status_code=status.HTTP_204_NO_CONTENT,
        description="Deletar Pedido pelo id"
        )
async def delete_order(id_order: int, db: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    return await OrderItemServices()._delete_order(id_order=id_order, db=db)