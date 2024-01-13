from pytest import mark
from httpx import AsyncClient
from app.tests.mock_schemas import user1, book1


@mark.anyio
async def test_book_list_not_member(client: AsyncClient, refresh_db):
    # USER CREATION
    response = await client.post('/api/users/register/', json=user1.model_dump())
    assert response.status_code == 201

    # USER LOGIN
    response = await client.post('/api/users/login/', json=user1.model_dump())
    assert response.status_code == 200
    assert list(response.json().keys()) == ['access_token', "token_type"]
    assert response.json()['token_type'] == "bearer"
    access_token = response.json()['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = await client.get('/api/books/List/', headers=headers)
    assert response.status_code == 403
    assert response.json()['detail'] == 'User does not have an active membership'


@mark.anyio
async def test_book_list_member(client: AsyncClient, refresh_db):
    # USER LOGIN
    response = await client.post('/api/users/login/', json=user1.model_dump())
    assert response.status_code == 200

    assert list(response.json().keys()) == ['access_token', "token_type"]
    assert response.json()['token_type'] == "bearer"
    access_token = response.json()['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # User Membership
    response = await client.post('/api/memberships/create/', headers=headers)
    assert response.status_code == 201

    response = await client.get('/api/books/List/', headers=headers)
    assert response.status_code == 404
    assert response.json()['detail'] == 'No books found'
