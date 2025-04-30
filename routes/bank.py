from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app import crud, database, db_models  # db_models = SQLAlchemy models

# Token settings
SECRET_KEY = "7f1d6a6b028551be1a9d7daba91ef219a34281829e9c35211485cc247207cd15"  # Replace with a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# This scheme is used in route dependencies to extract the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# app/routes/bank.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, models, database

bank_router = APIRouter()

@bank_router.get("/bank-accounts/{user_id}", response_model=list[models.BankAccountOut])
def get_bank_accounts(user_id: int, db: Session = Depends(database.get_db)):
    # Fetch user bank accounts based on the user_id
    return crud.get_user_bank_accounts(db, user_id)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)) -> db_models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    return user
# app/routes/bank.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, models, database  # Make sure all necessary imports are correct

bank_router = APIRouter()

@bank_router.get("/bank-accounts/{user_id}", response_model=list[models.BankAccountOut])
def get_bank_accounts(user_id: int, db: Session = Depends(database.get_db)):
    # Fetch user bank accounts based on the user_id
    return crud.get_user_bank_accounts(db, user_id)
