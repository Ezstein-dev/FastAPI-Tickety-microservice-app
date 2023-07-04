from ..db.postgres import Base
from sqlalchemy import Column, ForeignKey,Integer, String, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Ticket(Base):
    __tablename__ = "ticket"
    
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False, index=True) #description can contain event location, precaution during event and other necessary information
    price = Column(Float, nullable=False, index=True)
    quantity = Column(Integer, nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    
    
class User(Base):
    __tablename__= "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String, nullable=False) #phone no should be unique

    