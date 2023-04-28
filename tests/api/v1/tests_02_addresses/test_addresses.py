from httpx import AsyncClient
from models.user import User
from typing import List
import pytest
from httpx import AsyncClient
from tests.Mock.mock_users import MockUser
from tests.Mock.mock_address import MockAddress

user = MockUser()
address = MockAddress()


"""
CREATE ADDRESS WITHOUT LOGGED
"""
@pytest.mark.anyio
async def test_fail_create_address_without_logged(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/enderecos/", 
        json=address.payload_create_address(id=user.id))
    
    assert response.json()["detail"] == "Not authenticated"

""" 
CREATE ADDRESS WITH WRONG CEP
"""
@pytest.mark.anyio
async def test_fail_create_address_with_wrong_cep(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/enderecos/", 
        json=address.payload_create_address_wrong_CEP(id=user.id, cep="88780-@@@"), 
        headers=user.header)
    
    assert response.json()["detail"] == "Campo CEP inválido"

""" 
SUCCESS CREATE ADDRESS
"""
@pytest.mark.anyio
async def test_success_create_address(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/enderecos/", 
        json=address.payload_create_address(id=user.id), 
        headers=user.header)

    assert response.status_code == 201

@pytest.mark.anyio
async def test_success_update_address(client: AsyncClient) -> None:
    response = await client.put(
        f"/api/v1/enderecos/{address.id}", 
        json=address.payload_update_address(
        description="Terra da baleia Franca",
        postal_code="88780-000",
        street="Av Renato Ramos da Silva",
        complement="Nº 3013 - AP05",
        neighborhood="Vila Nova"
        ), 
        headers=user.header)
    assert response.status_code == 200

""" 
GET USER BY CEP
"""
@pytest.mark.anyio
async def test_success_get_user_by_cep(client: AsyncClient) -> None:
    response = await client.get(
        f"/api/v1/enderecos/user/cep/{address.postal_code}", 
        headers=user.header)
    
    assert response.status_code == 200
    assert len(response.json()) > 0

""" 
GET ADDRESS BY USER
"""
@pytest.mark.anyio
async def test_success_address_by_user(client: AsyncClient) -> None:
    response = await client.get(
        f"/api/v1/enderecos/user/{user.id}", 
        headers=user.header)
    
    assert response.status_code == 200
    assert len(response.json()) > 0

""" 
GET ALL ADDRESSES
"""
@pytest.mark.anyio
async def test_success_get_all_addresses(client: AsyncClient) -> None:
    response = await client.get(
        f"/api/v1/enderecos/", 
        headers=user.header)
    assert response.status_code == 200
    assert len(response.json()) > 0

""" 
DELETE ADDRESS BY ID
"""
# @pytest.mark.anyio
# async def test_success_delete_address_by_id(client: AsyncClient) -> None:
#     response = await client.delete(
#         f"/api/v1/enderecos/{address.id}", 
#         headers=user.header)
    
#     assert response.status_code == 204
    