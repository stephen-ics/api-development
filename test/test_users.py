from app import schemas
from jose import jwt
import pytest
from app.config import settings

def test_root(client):
    res = client.get('/') 
    assert res.json().get('message') == 'Hello World!!!'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post('/users/', json={'email': 'hellos1234@gmail.com', 'password': 'password123'})

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == 'hellos1234@gmail.com'
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post(
        "/login", json={'email': test_user['email'], 'password': test_user['password']}
    )

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')

    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize('email, password, status_code', [
    ('wrongemail@gmail.com', 'password123', 403),
    ('hellooo@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('hellooo@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):

    res = client.post(
        '/login', json={'email': email, 'password': password}
    )

    assert res.status_code == status_code



                                                                                                                                   
                                                                   