from pytest import mark
from httpx import AsyncClient
from app.tests.mock_schemas import user1, user2


@mark.anyio
async def test_healthcheck(client: AsyncClient, refresh_db):
    response = await client.get('/')
    assert response.status_code == 404


@mark.anyio
async def test_user_create(client: AsyncClient, refresh_db):
    response = await client.post('/api/users/register/', json=user1.model_dump())
    assert response.status_code == 201
    assert response.json()['username'] == user1.username
    assert response.json()['is_admin'] is False
    assert response.json()['id'] == 1


@mark.anyio
async def test_user_create_existing(client: AsyncClient, refresh_db):
    response = await client.post('/api/users/register/', json=user1.model_dump())
    assert response.status_code == 400
    assert response.json()['detail'] == 'Username already exists'


@mark.anyio
async def test_user_login(client: AsyncClient, refresh_db):
    response = await client.post('/api/users/login/', json=user1.model_dump())
    assert response.status_code == 200
    assert list(response.json().keys()) == ['access_token', "token_type"]
    assert response.json()['token_type'] == "bearer"


@mark.anyio
async def test_user_wrong_login(client: AsyncClient, refresh_db):
    response = await client.post('/api/users/login/', json=user2.model_dump())
    assert response.json()['detail'] == 'Incorrect username or password'
    assert response.status_code == 401


@mark.anyio
async def test_user_me(client: AsyncClient, refresh_db):
    response = await client.post('/api/users/login/', json=user1.model_dump())
    assert response.status_code == 200
    assert list(response.json().keys()) == ['access_token', "token_type"]
    assert response.json()['token_type'] == "bearer"
    access_token = response.json()['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = await client.post('/api/users/me/', headers=headers)
    assert response.json()['username'] == user1.username
    assert response.json()['is_admin'] is False
    assert response.json()['id'] == 1

