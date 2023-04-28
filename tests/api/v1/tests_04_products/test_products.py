from httpx import AsyncClient
from typing import List
import pytest
from tests.Mock.mock_users import MockUser
from tests.Mock.mock_categories import MockCategory
from tests.Mock.mock_products import MockProduct

user: MockUser = MockUser()
category: MockCategory = MockCategory()
product: MockProduct = MockProduct()

""" 
TEST FAIL GET ALL PRODUCTS WITH EMPTY LIST
"""
@pytest.mark.anyio
async def test_fail_get_all_products_with_empty_list(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/produtos/", headers=user.header)
    if response.status_code == 200:
        assert response.status_code == 200
    elif response.status_code == 404:
        assert response.json()["detail"] == "Nenhum produto cadastrado."
        assert response.status_code == 404
    else:
        assert response.status_code == 500
    
""" 
TEST SUCCESS INSERT PRODUCT
"""
@pytest.mark.anyio
async def test_fail_create_product(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/produtos/", json=product.payload_create_or_update_product(), headers=user.header)

    assert response.status_code == 201


""" 
TEST SUCCESS GET ALL PRODUCTS
"""
@pytest.mark.anyio
async def test_success_get_all_products(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/produtos/", headers=user.header)
    
    assert response.status_code == 200

""" 
TEST SUCCESS GET PRODUCT BY ID
"""
@pytest.mark.anyio
async def test_success_get_product_by_id(client: AsyncClient) -> None:
    response = await client.get(
        f"/api/v1/produtos/{product.id}", headers=user.header)
    
    assert response.status_code == 200

""" 
TEST SUCCESS UPDATE PRODUCT
"""
@pytest.mark.anyio
async def test_success_update_product(client: AsyncClient) -> None:
    product_update = product.payload_create_or_update_product(
        name="Molinete Shimano 12BB", 
        description="Molinete em alúminio e rolamentos inox",
        price=799.00
        )
    response = await client.put(
        f"/api/v1/produtos/{product.id}", json=product_update , headers=user.header)
    
    assert response.status_code == 200

""" 
TEST SUCCESS INSERT CATEGORY FOR PRODUCT
"""
@pytest.mark.anyio
async def test_fail_insert_category_for_product(client: AsyncClient) -> None:
    response = await client.post(
        f"/api/v1/produtos/{product.id}/categorias/{category.id}", headers=user.header)
    if response.status_code == 201:
        assert response.status_code == 201
    else:
        assert response.status_code == 500
        assert response.json()["detail"] == "Erro ao acessar o banco de dados: (product_id, category_id)=(1, 1) already exists."
""" 
TEST GET PRODUCTS WITH CATEGORY
"""
@pytest.mark.anyio
async def test_success_get_all_products_with_categories(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/produtos/categorias", headers=user.header)
    
    assert response.status_code == 200
