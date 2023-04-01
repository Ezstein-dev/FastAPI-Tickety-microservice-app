import json
import pytest
from fastapi.testclient import TestClient
from ..api.inventory import app
from ..models.ticket_model import Ticket

client = TestClient(app)


def test_create_ticket():
    # Test creating a new ticket
    ticket_data = {
        "name": "Test Ticket",
        "description": "This is a test ticket",
        "price": 9.99,
        "quantity": 10
    }
    response = client.post("/ticket/", json=ticket_data)
    assert response.status_code == 201
    ticket = response.json()
    assert ticket["name"] == ticket_data["name"]
    assert ticket["description"] == ticket_data["description"]
    assert ticket["price"] == ticket_data["price"]
    assert ticket["quantity"] == ticket_data["quantity"]
    assert ticket["id"] is not None
    return ticket["id"]


def test_update_ticket():
    # Create a new ticket
    ticket_id = test_create_ticket()
    
    # Update the ticket
    updated_ticket_data = {
        "name": "Updated Ticket",
        "description": "This ticket has been updated",
        "price": 19.99,
        "quantity": 5
    }
    response = client.put(f"/ticket/{ticket_id}", json=updated_ticket_data)
    assert response.status_code == 200
    updated_ticket = response.json()
    assert updated_ticket["name"] == updated_ticket_data["name"]
    assert updated_ticket["description"] == updated_ticket_data["description"]
    assert updated_ticket["price"] == updated_ticket_data["price"]
    assert updated_ticket["quantity"] == updated_ticket_data["quantity"]
    
    # Delete the ticket
    response = client.delete(f"/ticket/{ticket_id}")
    assert response.status_code == 204


def test_delete_ticket():
    # Create a new ticket
    ticket_data = {
        "name": "Test Ticket",
        "description": "This is a test ticket",
        "price": 9.99,
        "quantity": 10
    }
    response = client.post("/ticket/", json=ticket_data)
    ticket = response.json()

    # Delete the ticket
    response = client.delete(f"/tickets/{ticket['id']}")
    assert response.status_code == 200
    assert response.json() == {"The ticket with the id:{} hes been deleted".format(ticket['id'])}

    # Try to get the deleted ticket (should return 404)
    response = client.get(f"/tickets/{ticket['id']}")
    assert response.status_code == 404

