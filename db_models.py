from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from app.database import engine  # Import engine from database.py

# Initialize Base here to avoid circular imports
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True)
    bank_name = Column(String)
    account_type = Column(String)
    balance = Column(Float)

# Create tables by connecting Base to the engine
Base.metadata.create_all(bind=engine)

