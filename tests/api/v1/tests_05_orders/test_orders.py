from httpx import AsyncClient
from typing import List
import pytest
from tests.Mock.mock_users import MockUser
from tests.Mock.mock_categories import MockCategory
from tests.Mock.mock_products import MockProduct
from tests.Mock.mock_order import MockOrderItem
from tests.Mock.mock_address import MockAddress
from datetime import datetime

user: MockUser = MockUser()
category: MockCategory = MockCategory()
product: MockProduct = MockProduct()
order: MockOrderItem = MockOrderItem()
address: MockAddress = MockAddress()

""" 
TEST SUCCESS INSERT ORDER
"""
@pytest.mark.anyio
async def test_success_insert_order(client: AsyncClient) -> None:
    payload = order.payload_insert_or_update_order() 
    response = await client.post(
        "/api/v1/pedidos/", 
        json=payload, 
        headers=user.header)
    
    assert response.status_code == 201

""" 
TEST SUCCESS INSERT ORDER ITEM
"""
@pytest.mark.anyio
async def test_success_insert_order_item(client: AsyncClient) -> None:
    payload = order.payload_insert_or_update_order_item_quantity(quantity=50) 
    response = await client.put(
        f"/api/v1/pedidos/{order.id}/items/{product.id}", 
        json=payload,
        headers=user.header)
    if response.status_code == 201:
        assert response.status_code == 201
    else:
        assert response.status_code == 500
        assert "already exists" in response.json()["detail"]

""" 
TEST SUCCESS UPDATE ORDER ITEM QUANTITY
"""
@pytest.mark.anyio
async def test_success_update_order_item_quantity(client: AsyncClient) -> None:
    quantity: int = order.payload_insert_or_update_order_item_quantity(quantity=75)["quantity"]
    response = await client.put(
        f"/api/v1/pedidos/{order.id}/item/{product.id}/qtd/{quantity}",  
        headers=user.header)
    
    assert response.status_code == 200

""" 
TEST SUCCESS UPDATE ORDER STATUS
"""
@pytest.mark.anyio
async def test_success_update_order_status(client: AsyncClient) -> None:
    payload: int = order.payload_update_status(status="Pago")
    response = await client.put(
        f"/api/v1/pedidos/{order.id}",  
        json=payload,
        headers=user.header)
    
    assert response.status_code == 200

""" 
TESTE SUCCESS GET ORDER BY DATE RANGE
"""
@pytest.mark.anyio
async def test_success_get_order_by_date_Range(client: AsyncClient) -> None:
    day = datetime.today().day + 1
    month = datetime.today().month
    year = datetime.today().year
    ini_date = f"{year}-{month}-01"
    end_date = f"{year}-{month}-{day}"
    
    response = await client.get(
        f"/api/v1/pedidos/{ini_date}/{end_date}", headers=user.header)

    assert response.status_code == 200
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["status"] == "Pago"
    assert response.json()[0]["order_date"]
    assert response.json()[0]["user"]["id"] == user.id
    assert response.json()[0]['user']["email"] == user.email
    assert response.json()[0]["user"]["name"] == "SuperUser"
    assert response.json()[0]["address"]["id"] == address.id
    assert response.json()[0]["address"]["user_id"] == address.user_id
    assert response.json()[0]["address"]["description"] == "Terra da baleia Franca"
    assert response.json()[0]["address"]["postal_code"] == address.postal_code
    assert response.json()[0]["address"]["street"] == address.street
    assert response.json()[0]["address"]["complement"] == address.complement
    assert response.json()[0]["address"]["neighborhood"] == address.neighborhood
    assert response.json()[0]["address"]["city"] == address.city
    assert response.json()[0]["address"]["state"] == address.state
    assert response.json()[0]["items"][0]["id"] == order.id
    assert response.json()[0]["items"][0]["product_id"] == product.id
    assert response.json()[0]["items"][0]["price"] == 59925.0
    assert response.json()[0]["items"][0]["quantity"] == 75


""" 
TEST GET ALL ORDERS
"""
@pytest.mark.anyio
async def test_success_get_all_orders(client: AsyncClient) -> None:
    response = await client.get(
        f"/api/v1/pedidos/", headers=user.header)

    assert response.status_code == 200

""" 
TEST GET ORDER BY ID
"""
@pytest.mark.anyio
async def test_success_get_order_by_id(client: AsyncClient) -> None:
    response = await client.get(
        f"/api/v1/pedidos/{order.id}", headers=user.header)

    assert response.status_code == 200

""" 
TEST GET ORDER BY USER ID
"""
@pytest.mark.anyio
async def test_success_get_order_by_user_id(client: AsyncClient) -> None:
    response = await client.get(
        f"/api/v1/pedidos/listar/usuario/{user.id}", headers=user.header)

    assert response.status_code == 200
    

""" 
CLEANING DATA BY DB
"""

""" 
TESTE SUCCESS DELETE ORDER ITEM
"""
# @pytest.mark.anyio
# async def test_success_delete_order_item(client: AsyncClient) -> None:
#     response = await client.delete(
#         f"/api/v1/pedidos/delete/by/order/{order.id}/item/{product.id}", headers=user.header)

#     assert response.status_code == 204

""" 
TEST SUCCESS DELETE ORDER
"""
# @pytest.mark.anyio
# async def test_success_delete_order(client: AsyncClient) -> None:
#     response = await client.delete(
#         f"/api/v1/pedidos/{order.id}", headers=user.header)

#     assert response.status_code == 204

""" 
TEST SUCCESS DELETE CATEGORY
"""
# @pytest.mark.anyio
# async def test_success_delete_category(client: AsyncClient) -> None:
#     response = await client.delete(
#         f"/api/v1/categorias/{category.id}", headers=user.header)

#     assert response.status_code == 204

""" 
# TEST SUCCESS DELETE PRODUCT
# """
# @pytest.mark.anyio
# async def test_success_delete_product(client: AsyncClient) -> None:
#     response = await client.delete(
#         f"/api/v1/produtos/{product.id}", headers=user.header)

#     assert response.status_code == 204


""" 
TEST SUCCESS DELETE ADDRESS
"""
# @pytest.mark.anyio
# async def test_success_delete_address(client: AsyncClient) -> None:
#     response = await client.delete(
#         f"/api/v1/enderecos/{address.id}", headers=user.header)

#     assert response.status_code == 204

""" 
TEST SUCCESS DELETE USER
"""
# @pytest.mark.anyio
# async def test_success_delete_user(client: AsyncClient) -> None:
#     response = await client.delete(
#         f"/api/v1/usuarios/{user.id}", headers=user.header)

#     assert response.status_code == 204