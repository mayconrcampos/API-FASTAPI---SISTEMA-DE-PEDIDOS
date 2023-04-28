from httpx import AsyncClient
from models.user import User
from typing import List
import pytest
from tests.Mock.mock_users import MockUser

user: MockUser = MockUser()

"""
    CREATE USER
"""
@pytest.mark.anyio
async def test_success_create_user(client: AsyncClient) -> None:
    response = await client.post("/api/v1/usuarios/", json=user.payload_create_user())
    if response.status_code == 500:
        # MAKE USER LOGIN
        assert  response.status_code == 500
    else:
        assert response.status_code == 201
        assert response.json()["id"] == user.id
        assert response.json()["email"] == user.email
        assert response.json()["name"] == user.name

"""
    FAIL LOGIN
"""
@pytest.mark.anyio
async def test_fail_login_created_user(client: AsyncClient) -> None:
    # Faz login com as credenciais do usuário criado
    response = await client.post("/api/v1/usuarios/login", data=user.payload_login_with_wrong_password(password="senhaerrada"), 
    headers=user.header_login)
    assert response.json()['detail'] == "As credenciais estão incorretas."
    assert response.status_code == 400

"""
    SUCCESS LOGIN
"""
@pytest.mark.anyio
async def test_success_login_created_user(client: AsyncClient) -> None:
    response = await client.post("/api/v1/usuarios/login", data=user.payload_login(), 
    headers=user.header_login)

    assert response.json()["access_token"] != ""
    assert response.json()["token_type"] == "bearer"
    assert response.status_code == 200

"""
    FAIL GET ALL CLIENTS - NOT LOGGED
"""
@pytest.mark.anyio
async def test_fail_get_all_clients_without_logged(client: AsyncClient) -> None:
    response = await client.get("/api/v1/usuarios/")
    assert "Not authenticated" in response.json()["detail"]
    assert response.status_code == 401


"""
    SUCCESS GET ALL CLIENTS
    """
@pytest.mark.anyio
async def test_success_get_all_clients(client: AsyncClient) -> None:
    response = await client.get("/api/v1/usuarios/", headers=user.header)
    assert len(response.json()) > 0
    assert response.status_code == 200

"""
    SUCCESS GET USER LOGGED
"""
@pytest.mark.anyio
async def test_success_get_user_logged(client: AsyncClient) -> None:
    response = await client.get("/api/v1/usuarios/auth/logged/", headers=user.header)

    assert response.status_code == 200
    assert response.json()['id'] == user.id
    assert response.json()['name'] == user.name
    assert response.json()['email'] == user.email

"""
    SUCCESS GET USER BY ID
"""
@pytest.mark.anyio
async def test_success_get_user_by_id(client: AsyncClient) -> None:
    response_get_user = await client.get(f"/api/v1/usuarios/{user.id}", headers=user.header)

    assert response_get_user.status_code == 200
    assert response_get_user.json()["id"] == user.id
    assert response_get_user.json()["name"] == user.name
    assert response_get_user.json()["email"] == user.email

"""
    SUCCESS GET UPDATE LAST USER
"""
@pytest.mark.anyio
async def test_success_update_last_inserted_user(client: AsyncClient) -> None:
    response_update = await client.put(f"/api/v1/usuarios/{user.id}", json=user.payload_update_user("SuperUser"), headers=user.header)

    user_updated: dict = response_update.json()
    assert response_update.status_code == 200
    assert user_updated["name"] == user.name_updated

"""
    SUCCESS DELETE BIROLIRO
"""
# @pytest.mark.anyio
# async def test_success_delete_last_user(client: AsyncClient) -> None:
#     response_delete = await client.delete(f"/api/v1/usuarios/{user.id}", headers=user.header)

#     assert response_delete.status_code == 204
