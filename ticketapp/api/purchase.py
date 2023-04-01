import requests
import time
import httpx
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.background import BackgroundTasks
from starlette.requests import Request

from ..db.redis import redis
from ..schemas.ticket_schemas import Order
from ..auth import token
    

router = APIRouter(
    prefix="/order"
)


@router.post("/", status_code=status.HTTP_200_OK)
async def create_order(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: int = Depends(token.get_current_user),
    token_data: dict = Depends(token.get_current_user),
    access_token: str = Depends(token.get_access_token)
):
    # Set the headers with the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    ticket_request = await request.json()
    
        
    # Fetch the ticket from the inventory using its ID
    try:
        async with httpx.AsyncClient() as client:
            req = await client.get(f"http://localhost:8000/ticket/{ticket_request['id']}", headers=headers)
            req.raise_for_status()  # raises an exception if the response status is not successful (i.e., 200-299)
            ticket = req.json()
    except httpx.HTTPError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The ticket with the id:{ticket_request['id']} not found")
    
    # Check if there are enough tickets available for purchase
    if ticket["quantity"] < ticket_request["quantity"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough tickets available",
        )

    # Update the ticket quantity in the inventory by subtracting the purchased quantity
    ticket["quantity"] -= ticket_request["quantity"]
    ticket_data = {
        "name": ticket["name"],
        "description": ticket["description"],
        "price": ticket["price"],
        "quantity": ticket["quantity"],
    }
    req = requests.put(
        f"http://localhost:8000/ticket/{ticket_request['id']}", json=ticket_data, headers=headers
    )

    # Create the order
    order = Order(
        product_id=ticket_request["id"],
        price=ticket["price"],
        fee=0.2 * ticket["price"],
        total=1.2 * ticket["price"],
        quantity=ticket_request["quantity"],
        status="pending",
    )
    order.save()

    # Add a background task to complete the order after 5 seconds
    background_tasks.add_task(completed_order, order)

    return {"message": "Order created Pending", "order": order}

async def completed_order(order: Order):
    time.sleep(20)
    order.status = "completed"
    order.save()
    redis.xadd('completed_order', order.dict(), '*')



    
@router.get("/{pk}")
async def get_order(pk: str):
    order = Order.get(pk)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return {"order": order}
    
