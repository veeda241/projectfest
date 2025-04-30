# auth.py

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

# This line defines the scheme used to extract the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Setting up bcrypt context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key and algorithm to sign the JWT tokens
SECRET_KEY = "7f1d6a6b028551be1a9d7daba91ef219a34281829e9c35211485cc247207cd15"  # Load from .env ideally
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # You can adjust the expiration time

# Hash a password using bcrypt
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify if the given password matches the hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create a JWT access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify the JWT token and decode it
def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # Extract email from token
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
        )


from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "7f1d6a6b028551be1a9d7daba91ef219a34281829e9c35211485cc247207cd15"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import crud, database, models

# Define the token scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user
