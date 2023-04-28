from fastapi import status, HTTPException, Response
from models.order import Order, Order_GET, Order_UP
from models.user import User
from models.address import Address
from models.order_item import OrderItem
from models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import make_transient, selectinload
from sqlmodel import select
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from datetime import datetime


class OrderItemServices:
    @classmethod
    async def _get_all_orders(cls, db: AsyncSession):
        try:
            async with db as session:
                query = select(Order).options(
                    selectinload(Order.user),
                    selectinload(Order.address),
                    selectinload(Order.items)
                    ).order_by(Order.id)

                results = await session.execute(query)
                orders: List[Order] = results.scalars().all()

                if orders:
                    for order in orders:
                        make_transient(order)
                    return orders
                raise HTTPException(detail=f"Não existem Pedidos cadastrados.", status_code=status.HTTP_400_BAD_REQUEST)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _get_orders_by_date_range(cls, start_date: str, end_date: str, db: AsyncSession):
        try:
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

            async with db as session:
                query = select(Order).options(
                    selectinload(Order.user),
                    selectinload(Order.address),
                    selectinload(Order.items)
                    ).filter(Order.order_date >= start_datetime, Order.order_date <= end_datetime).order_by(Order.id)
                result = await session.execute(query)
                orders: List[Order_GET] = result.scalars().all()

                if orders:
                    for order in orders:
                        make_transient(order)
                    return orders
                raise HTTPException(detail="Nenhum pedido encontrado", status_code=status.HTTP_404_NOT_FOUND)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _get_order_by_id(cls, id_order: int, db: AsyncSession):
        try:
            async with db as session:
                query = select(Order).options(
                    selectinload(Order.user),
                    selectinload(Order.address),
                    selectinload(Order.items)
                    ).where(Order.id == id_order)

                results = await session.execute(query)
                order: Order = results.scalar_one_or_none()

                if order:            
                    # make_transient(order)
                    return order
                raise HTTPException(detail=f"Pedido não encontrado.", status_code=status.HTTP_400_BAD_REQUEST)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _get_order_by_user_id(cls, id_user: int, db: AsyncSession):
        try:
            async with db as session:
                query = select(Order).options(
                    selectinload(Order.user),
                    selectinload(Order.address),
                    selectinload(Order.items)
                    ).where(Order.user_id == id_user)

                results = await session.execute(query)
                order: List[Order] = results.scalars().all()

                if order:
                    return order
                raise HTTPException(detail=f"Não existem Pedidos cadastrados para este usuário.", status_code=status.HTTP_400_BAD_REQUEST)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _create_order(cls, order: Order, db: AsyncSession):
        try:
            async with db as session:
                query = select(User).where(User.id == order.user_id).options(selectinload(User.address))
                result = await session.execute(query)
                user: User = result.unique().scalar_one_or_none()
                if user:
                    if user.address:
                        address: Address = user.address[0]
                        new_order: Order = Order(
                            status=order.status, 
                            user=user, 
                            address_id=address.id,
                            address=address
                            )
                        session.add(new_order)
                        await session.commit()
                        await session.refresh(new_order)
                        await session.close()
                        make_transient(new_order)
                        return new_order
                    else:
                        raise HTTPException(detail="Nenhum endereço cadastrado para este usuário", status_code=status.HTTP_404_NOT_FOUND)
                raise HTTPException(detail="Usuário não encontrado", status_code=status.HTTP_404_NOT_FOUND) 

        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _insert_item_to_order(cls, order_id: int, product_id: int, item: OrderItem, order: Order, db: AsyncSession):
        try:
            async with db as session:
                query_product = select(Product).where(Product.id == product_id)
                res = await session.execute(query_product)
                prod: Product = res.scalar_one_or_none()
                if prod:
                    new_item: OrderItem = OrderItem(
                        order_id=order_id,
                        product_id=product_id,
                        price=prod.price * item.quantity,
                        quantity=item.quantity,
                        product=prod,
                        order=order
                    )
                    session.add(new_item)
                    await session.commit()
                    await session.refresh(new_item)
                    await session.close()
                    # make_transient(new_item)
                    # OrderItem_GET.update_forward_refs()
                    return new_item
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _change_status(cls, order_id: int, order_up: Order_UP, db: AsyncSession):
        try:
            async with db as session:
                query = select(Order).options(
                    selectinload(Order.user),
                    selectinload(Order.address),
                    selectinload(Order.items)
                    ).where(Order.id == order_id)
                res = await session.execute(query)
                order: Order = res.scalar_one_or_none()

                if order:
                    order_up: Order_UP = Order_UP(status=order_up.status)
                    order_up = order_up.dict(exclude_unset=True)

                    for k, v in order_up.items():
                        setattr(order, k, v)

                    session.add(order)
                    await session.commit()
                    await session.refresh(order)
                    await session.close()

                    make_transient(order)
                    return order
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _update_quantity_items(cls, quantity: int, Order: Order, product: Product, db: AsyncSession):
        try:
            async with db as session:
                query = select(OrderItem).where(OrderItem.order_id == Order.id).where(OrderItem.product_id == product.id)
                result = await session.execute(query)
                order_item: OrderItem = result.scalar_one_or_none()

                if order_item:
                    order_item.quantity = quantity
                    order_item.price = quantity * product.price
                    session.add(order_item)
                    await session.commit()
                    await session.refresh(order_item)
                    await session.close()

                    return order_item
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))
    
    @classmethod
    async def _delete_product_order_item(cls, Order: Order, product: Product, db: AsyncSession):
        try:
            async with db as session:
                query = select(OrderItem).where(OrderItem.order_id == Order.id).where(OrderItem.product_id == product.id)
                result = await session.execute(query)
                order_item: OrderItem = result.unique().scalar_one_or_none()

                if order_item:
                    await session.delete(order_item)
                    await session.commit()
                    # await session.refresh(order_item)

                    return order_item
                raise HTTPException(detail="Item não encontrado no pedido", status_code=status.HTTP_404_NOT_FOUND)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao processar a requisição: " + str(e))

    @classmethod
    async def _delete_order(cls, id_order: int, db: AsyncSession):
        try:
            async with db as session:
                query = select(Order).where(Order.id == id_order)
                result = await session.execute(query) 
                order: Order = result.scalar_one()

                await session.delete(order)
                await session.commit()

                return Response(status_code=status.HTTP_204_NO_CONTENT)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  detail="Erro ao acessar o banco de dados: " + str(e))
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  detail="Erro ao processar a requisição: " + str(e))