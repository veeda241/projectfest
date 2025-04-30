# app/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base  # Import Base from database.py

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Relationship to TaxRecord
    tax_records = relationship("TaxRecord", back_populates="user")


class TaxRecord(Base):
    __tablename__ = 'tax_records'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tax_paid = Column(Float)

    # Relationship back to User
    user = relationship("User", back_populates="tax_records")

class BankAccount(Base):
    __tablename__ = 'bank_accounts'

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True)
    bank_name = Column(String)
    account_type = Column(String)
    balance = Column(Float)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="bank_accounts")

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ... SQLAlchemy models above ...

# Pydantic models
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # For Pydantic v2
# app/models.py
from pydantic import BaseModel

class BankAccountOut(BaseModel):
    id: int
    account_number: str
    bank_name: str
    account_type: str
    balance: float

    class Config:
        from_attributes = True  # Use this for Pydantic v2+
class TaxRecordOut(BaseModel):
    id: int
    user_id: int
    tax_paid: float

    class Config:
        from_attributes = True  # Needed for SQLAlchemy -> Pydantic conversion
from pydantic import BaseModel

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class BankAccountOut(BaseModel):
    id: int
    account_number: str
    bank_name: str
    account_type: str
    balance: float
    user_id: int

    class Config:
        from_attributes = True

class TaxRecordOut(BaseModel):
    id: int
    user_id: int
    tax_paid: float

    class Config:
        from_attributes = True
