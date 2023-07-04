from datetime import datetime
from typing import List, Optional

from ..db.redis import redis
from pydantic import BaseModel, EmailStr, conint
from redis_om import HashModel


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserPassword(BaseModel):
    old_password: str
    new_password1: str
    new_password2: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class TicketCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


class TicketOut(TicketCreate):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Ticket(TicketOut):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        exclude = ["created_at"]
        
class TicketQuantity(BaseModel):
    quantity: int

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None