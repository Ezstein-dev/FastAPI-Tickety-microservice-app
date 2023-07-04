import json
import pytest
from fastapi.testclient import TestClient
from jose import jwt
from ..api.main import app2
from ..models.ticket_model import *
from ..schemas.ticket_schemas import *
from ..config.settings import *


def test_user_create(client):
    user_data = {
        "email": "ezsdev@gmail.com",
        "password": "password234",
        "phone_number": "4638373837"
    }
    response = client.post("/users/", json=user_data)
    new_user = UserOut(**response.json())
    assert new_user.email == "ezsdev@gmail.com"
    assert response.status_code == 201
    
def test_user_login(client, test_user):
    user_data = {
        "username": test_user['email'],
        "password": test_user["password"],
    }
    response = client.post("/login", data=user_data)
    login_response = Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: int = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200
    
@pytest.mark.parametrize("email, password, status_code",[
    ("ezsdev@gmail.com", "wrongpassword", 403),
    ("wrongemail", "password234", 403),
    (None, "password234", 422),
    ("wrongemail", None, 422)
])
def test_invalid_credentials(client, test_user, email, password, status_code):
    response = client.post("/login", data={"username": email, "password": password})
    assert response.status_code == status_code