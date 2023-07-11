from app import schemas
from .database import client, session

def test_root(client):
    res = client.get('/') 
    assert res.json().get('message') == 'Hello World!!!'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post('/users/', json={'email': 'hellos1234@gmail.com', 'password': 'password123'})

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == 'hellos1234@gmail.com'
    assert res.status_code == 201