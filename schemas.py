# app/schemas.py
from pydantic import BaseModel

# User creation request
class UserCreate(BaseModel):
    email: str
    username: str
    password: str

# Output model for User
class UserOut(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models

# Bank Account create request
class BankAccountCreate(BaseModel):
    account_number: str
    bank_name: str
    account_type: str
    balance: float

# Output model for Bank Account
class BankAccountOut(BaseModel):
    id: int
    account_number: str
    bank_name: str
    account_type: str
    balance: float
    user_id: int

    class Config:
        orm_mode = True

# Login request
class UserLogin(BaseModel):
    email: str
    password: str
