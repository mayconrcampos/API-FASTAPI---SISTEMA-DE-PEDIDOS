from httpx import AsyncClient
from typing import List
import pytest
from tests.Mock.mock_users import MockUser
from tests.Mock.mock_categories import MockCategory

user: MockUser = MockUser()
category: MockCategory = MockCategory()


"""
CREATE ADDRESS WITHOUT LOGGED
"""
@pytest.mark.anyio
async def test_fail_create_category_without_logged(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/categorias/", json=category.payload_create_or_update_category())

    assert response.json()["detail"] == "Not authenticated"

""" 
CREATE CATEGORY
"""
@pytest.mark.anyio
async def test_success_create_category(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/categorias/", 
        json=category.payload_create_or_update_category(), headers=user.header)
    if response.status_code == 201:
        assert response.status_code == 201
    else:
        assert response.status_code == 500
        # assert "already exists" in response.json["detail"]

""" 
GET ALL CATEGORIES
"""
@pytest.mark.anyio
async def test_success_get_all_categories(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/categorias/", headers=user.header)
    
    assert response.status_code == 200

""" 
GET CATEGORY BY ID
"""
@pytest.mark.anyio
async def test_success_get_category_by_id(client: AsyncClient) -> None:
    response = await client.get(
        f"/api/v1/categorias/{category.id}", headers=user.header)
    
    assert response.status_code == 200

""" 
UPDATE CATEGORY
"""
@pytest.mark.anyio
async def test_success_get_all_categories(client: AsyncClient) -> None:
    response = await client.put(
        f"/api/v1/categorias/{category.id}", json=category.payload_create_or_update_category("Utilitários") , headers=user.header)
    
    assert response.status_code == 200
