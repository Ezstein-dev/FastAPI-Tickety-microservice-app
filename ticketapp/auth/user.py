from typing import List

from ..db.postgres import get_db
from fastapi import Depends, APIRouter, HTTPException, Response, status
from sqlalchemy.orm import Session

from ..auth import token, utils, middleware
from ..models import ticket_model
from ..schemas import ticket_schemas

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=ticket_schemas.UserOut
)
def create_user(user: ticket_schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = ticket_model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=ticket_schemas.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(token.get_current_user),
):
    user = db.query(ticket_model.User).filter(ticket_model.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with the id: {id} does not exist",
        )
    return user


@router.get("/", response_model=List[ticket_schemas.UserOut])
def get_all_users(
    db: Session = Depends(get_db), current_user: int = Depends(token.get_current_user)
):
    users = db.query(ticket_model.User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No user on the platform currently",
        )
    return users


@router.put("/{id}")
def update_user_password(
    id: int,
    user_password: ticket_schemas.UserPassword,
    db: Session = Depends(get_db),
    current_user: int = Depends(token.get_current_user),
):
    user = db.query(ticket_model.User).filter(ticket_model.User.id == id).first()
    
    if not utils.verify(user_password.old_password, user.password): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    
    if user_password.old_password == user_password.new_password1:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You can't use your old password",
        )
        
    if user_password.new_password1 != user_password.new_password2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )

    hashed_password = utils.hash(user_password.new_password1)
    user.password = hashed_password
    db.commit()
    db.refresh(user)
    return {"detail": "Your password has been changed"}


@router.delete("/{id}")
def delete_user_account(
    id: int, db: Session = Depends(get_db), current_user: int = Depends(token.get_current_user)
):
    user_query = db.query(ticket_model.User).filter(ticket_model.User.id == id)
    
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"User with id:{id} does not exist")
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                        detail="Not authorized to perform requested action")
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    