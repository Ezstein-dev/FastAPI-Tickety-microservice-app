import json
import pytest
from fastapi.testclient import TestClient
from ..api.main import app1
from ..models.ticket_model import *


def test_create_ticket(authorized_client):
    # Test creating a new ticket
    ticket_data = {
        "name": "Test Ticket",
        "description": "This is a test ticket",
        "price": 9.99,
        "quantity": 10
    }
    response = authorized_client.post("/ticket/", json=ticket_data)
    assert response.status_code == 201
    ticket = response.json()
    assert ticket["name"] == ticket_data["name"]
    assert ticket["description"] == ticket_data["description"]
    assert ticket["price"] == ticket_data["price"]
    assert ticket["quantity"] == ticket_data["quantity"]
    assert ticket["id"] is not None


def test_update_ticket(authorized_client, create_ticket_instance):
    # Update the ticket
    updated_ticket_data = {
        "name": "Updated Ticket",
        "description": "This ticket has been updated",
        "price": 19.99,
        "quantity": 5
    }
    response = authorized_client.put(f"/ticket/{create_ticket_instance['id']}", json=updated_ticket_data)
    assert response.status_code == 200
    updated_ticket = response.json()
    assert updated_ticket["name"] == updated_ticket_data["name"]
    assert updated_ticket["description"] == updated_ticket_data["description"]
    assert updated_ticket["price"] == updated_ticket_data["price"]
    assert updated_ticket["quantity"] == updated_ticket_data["quantity"]
    
    # Delete the ticket
    response = authorized_client.delete(f"/ticket/{create_ticket_instance['id']}")
    assert response.status_code == 204


def test_delete_ticket(authorized_client, test_user, create_ticket_instance):
    # Delete the ticket
    response = authorized_client.delete(f"/ticket/{create_ticket_instance['id']}")
    assert response.status_code == 204
    
    # Try to get the deleted ticket (should return 404)
    response = authorized_client.get(f"/tickets/{create_ticket_instance['id']}")
    assert response.status_code == 404

