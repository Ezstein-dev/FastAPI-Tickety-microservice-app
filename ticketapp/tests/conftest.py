import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..api.main import app1
from ..models.ticket_model import *
from ..schemas.ticket_schemas import *
from ..config.settings import settings
from ..db.postgres import get_db, Base
from ..auth.token import create_access_token



SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
            
    app1.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app1)
        
        
@pytest.fixture
def test_user(client):
    user_data = {
        "email": "ezsdev@gmail.com",
        "password": "password234",
        "phone_number": "4638373837"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"bearer {token}",
    }

    return client

@pytest.fixture
def create_ticket_instance(authorized_client, test_user):
    ticket_data = {
        "name": "Test Ticket",
        "description": "This is a test ticket",
        "price": 9.99,
        "quantity": 10
    }
    response = authorized_client.post("/ticket/", json=ticket_data)
    assert response.status_code == 201
    ticket = response.json()
    return ticket