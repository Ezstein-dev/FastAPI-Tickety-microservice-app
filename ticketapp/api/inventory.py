import json
from typing  import List

from ..db.postgres import get_db
from ..db.redis import redis
from ..auth import token, middleware, user
from fastapi import APIRouter, Depends, HTTPException, status, FastAPI, Response
from ..models import ticket_model
from ..schemas.ticket_schemas import TicketCreate, TicketOut, Ticket, TicketQuantity
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(
    prefix="/ticket"
    )



@router.post("/", response_model=TicketOut, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db), current_user: int = Depends(token.get_current_user)):
    #store it into the database,and the current userID will be the ownerID
    new_ticket = ticket_model.Ticket(owner_id=current_user.id, **ticket.dict())
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    # #storing the same data to the in-memory database (redis)
    # redis.rpush(
    #     "tickets",
    #     json.dumps(
    #         {
    #             "name": ticket.name,
    #             "description": ticket.description,
    #             "price": ticket.price,
    #             "quantity": ticket.quantity,
    #             "owner_id": current_user.id,
    #             "ticket_id": new_ticket.id,
    #         }
    #     ),
    # )
    return new_ticket

@router.get("/", response_model= List[Ticket], status_code=status.HTTP_200_OK)
def get_ticket( db: Session = Depends(get_db), current_user: int = Depends(token.get_current_user)):
    #check for all tickets
    ticket = db.query(ticket_model.Ticket).all()
    #check if ticket exist
    if len(ticket) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No ticket is available",
        )
    return ticket

@router.get("/{id}", response_model= Ticket, status_code=status.HTTP_200_OK)
def get_ticket(id: int, db: Session = Depends(get_db), current_user: int = Depends(token.get_current_user)):
    #check for all tickets
    ticket = db.query(ticket_model.Ticket).filter(ticket_model.Ticket.id == id).first()
    #check if ticket exist
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No ticket with id: {id}",
        )
    return ticket

@router.put("/{id}", response_model=Ticket)
def update_ticket(id: int, updated_ticket: TicketCreate, db: Session = Depends(get_db), current_user: int = Depends(token.get_current_user)):
    ticket_query = db.query(ticket_model.Ticket).filter(ticket_model.Ticket.id == id)
    ticket = ticket_query.first()
    print({"ticket": ticket})
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Ticket with id:{id} does not exist")
    if ticket.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    ticket_query.update(updated_ticket.dict(), synchronize_session=False)
    db.commit()
    return ticket


@router.delete("/{id}")
def delete_ticket(id: int, db: Session = Depends(get_db), current_user: int = Depends(token.get_current_user)):
    ticket_query = db.query(ticket_model.Ticket).filter(ticket_model.Ticket.id == id)
    ticket = ticket_query.first()
    if ticket == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The ticket with the id:{id} is not available",
        )
    if ticket.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    ticket_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)